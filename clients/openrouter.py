import httpx
import asyncio
import itertools
import time
import json
import logging
from typing import List, Tuple, Dict, Any
from config import EvalConfig

logger = logging.getLogger(__name__)

class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, key: str):
        self._key_hint = f"...{key[-6:]}" if key and len(key) > 6 else key
        limits = httpx.Limits(max_connections=50, max_keepalive_connections=20)
        self._http_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://firecrawl.eval",
                "X-Title": "Firecrawl Eval",
            },
            timeout=300.0,
            limits=limits,
        )

    async def generate(
        self,
        prompt: str,
        model: str,
        response_format: dict = None,
        max_tokens: int = None,
        temperature: float = 0.1,
        system_prompt: str = None,
        providers: List[str] = None
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if providers:
            payload["provider"] = {
                "order": providers,
                "allow_fallbacks": False
            }
        if response_format:
            payload["response_format"] = response_format
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        logger.info(
            f"[OpenRouter] → POST /chat/completions | key={self._key_hint} "
            f"model={model} providers={providers} max_tokens={max_tokens} "
            f"prompt_chars={len(prompt)}"
        )
        t0 = time.time()

        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.debug(f"[OpenRouter] attempt={attempt+1}/{max_retries} sending request...")
                response = await self._http_client.post(
                    f"{self.BASE_URL}/chat/completions", json=payload
                )
                elapsed = time.time() - t0
                logger.info(
                    f"[OpenRouter] ← HTTP {response.status_code} in {elapsed:.1f}s "
                    f"(attempt {attempt+1})"
                )

                if response.status_code != 200:
                    logger.error(
                        f"[OpenRouter] Non-200 body: {response.text[:500]}"
                    )
                response.raise_for_status()

                data = response.json()

                # Log usage if available
                usage = data.get("usage", {})
                if usage:
                    logger.info(
                        f"[OpenRouter] usage: prompt_tokens={usage.get('prompt_tokens')} "
                        f"completion_tokens={usage.get('completion_tokens')} "
                        f"total_tokens={usage.get('total_tokens')}"
                    )

                choices = data.get("choices", [])
                if not choices:
                    logger.error(f"[OpenRouter] No choices in response: {json.dumps(data)[:500]}")
                    raise ValueError("No choices returned from LLM.")

                raw = choices[0]["message"].get("content") or ""
                if not raw:
                    logger.error(
                        f"[OpenRouter] Empty content. Full response: {json.dumps(data)[:500]}"
                    )
                    raise ValueError("LLM returned empty content in response.")

                logger.info(
                    f"[OpenRouter] ✓ Got {len(raw)} chars of content "
                    f"(finish_reason={choices[0].get('finish_reason')})"
                )
                logger.debug(f"[OpenRouter] raw[:300]: {raw[:300]}")

                # Strip thinking blocks if model outputs them
                import re
                final_response = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
                return final_response

            except httpx.HTTPStatusError as e:
                elapsed = time.time() - t0
                logger.error(
                    f"[OpenRouter] HTTP {e.response.status_code} after {elapsed:.1f}s: "
                    f"{e.response.text[:300]}"
                )
                if e.response.status_code in (502, 503) and attempt < max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"[OpenRouter] Retrying in {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                raise
            except httpx.TimeoutException as e:
                elapsed = time.time() - t0
                logger.error(
                    f"[OpenRouter] TIMEOUT after {elapsed:.1f}s (attempt {attempt+1}): {e}"
                )
                if attempt < max_retries - 1:
                    logger.warning("[OpenRouter] Retrying after timeout...")
                    continue
                raise
            except Exception as e:
                elapsed = time.time() - t0
                logger.error(
                    f"[OpenRouter] Unexpected error after {elapsed:.1f}s "
                    f"(attempt {attempt+1}): {type(e).__name__}: {e}"
                )
                raise

    async def aclose(self):
        await self._http_client.aclose()


class OpenRouterClientPool:
    def __init__(self, config: EvalConfig):
        keys = config.openrouter_keys
        if not keys:
            logger.warning("[OpenRouterPool] No OPENROUTER_KEY_* found.")
            keys = ["dummy"]
        logger.info(f"[OpenRouterPool] Initialized with {len(keys)} key(s).")
        self._clients = [OpenRouterClient(k) for k in keys]
        self._cycle = itertools.cycle(range(len(self._clients)))
        self._cooldowns: Dict[int, float] = {}
        self._lock = asyncio.Lock()  # protect _cycle + _cooldowns under concurrency

    def _next_available_slot(self) -> Tuple[int, "OpenRouterClient", float]:
        # NOTE: must be called while holding self._lock
        now = time.time()
        for _ in range(len(self._clients)):
            idx = next(self._cycle)
            if now >= self._cooldowns.get(idx, 0):
                return idx, self._clients[idx], 0.0
        
        best_idx = min(self._cooldowns.keys(), key=lambda k: self._cooldowns[k])
        sleep_time = max(0.0, self._cooldowns[best_idx] - now)
        return best_idx, self._clients[best_idx], sleep_time

    async def generate(
        self,
        prompt: str,
        model: str,
        response_format: dict = None,
        max_tokens: int = None,
        temperature: float = 0.1,
        system_prompt: str = None,
        providers: List[str] = None
    ) -> str:
        max_attempts = len(self._clients) * 3 + 1
        logger.info(
            f"[OpenRouterPool] generate() model={model} providers={providers} "
            f"max_attempts={max_attempts}"
        )
        for attempt in range(max_attempts):
            async with self._lock:
                idx, client, sleep_time = self._next_available_slot()
            if sleep_time > 0:
                logger.warning(
                    f"[OpenRouterPool] All slots on cooldown. Sleeping {sleep_time:.1f}s..."
                )
                await asyncio.sleep(sleep_time)
            logger.debug(f"[OpenRouterPool] Using client slot {idx} (attempt {attempt+1})")
            try:
                result = await client.generate(
                    prompt, model=model, response_format=response_format,
                    max_tokens=max_tokens, temperature=temperature, system_prompt=system_prompt,
                    providers=providers
                )
                logger.info(f"[OpenRouterPool] ✓ generate() succeeded on attempt {attempt+1}")
                return result
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    cooldown = 10 + (attempt * 2)
                    async with self._lock:
                        self._cooldowns[idx] = time.time() + cooldown
                    logger.warning(
                        f"[OpenRouterPool] 429 on slot {idx}. Cooling down for {cooldown}s."
                    )
                    continue
                raise
        raise RuntimeError("All slots exhausted due to 429s.")

    async def aclose(self):
        await asyncio.gather(*[c.aclose() for c in self._clients])
