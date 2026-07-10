import asyncio
import itertools
import time
import logging
from typing import List, Tuple, Dict, Any, Optional
try:
    from firecrawl import Firecrawl
except ImportError:
    from firecrawl import FirecrawlApp as Firecrawl
from config import EvalConfig
from models.eval_result import FirecrawlSearchResult

logger = logging.getLogger(__name__)

class FirecrawlClientPool:
    def __init__(self, config: EvalConfig):
        keys = config.firecrawl_keys
        if not keys:
            logger.warning("[FirecrawlPool] No FIRECRAWL_API_KEY_* found.")
            keys = ["dummy"]
        logger.info(f"[FirecrawlPool] Initialized with {len(keys)} API key(s).")
        self._clients = [Firecrawl(api_key=k) for k in keys]
        self._in_flight: Dict[int, int] = {i: 0 for i in range(len(self._clients))}
        self._cooldowns: Dict[int, float] = {}
        self._lock = asyncio.Lock()  # protect _in_flight + _cooldowns under concurrency

    def _next_available_slot(self) -> Tuple[int, Firecrawl, float]:
        now = time.time()
        best_idx = -1
        best_inflight = float('inf')
        best_sleep = 0.0

        for idx in range(len(self._clients)):
            sleep_time = max(0.0, self._cooldowns.get(idx, 0) - now)
            if sleep_time == 0.0:
                inflight = self._in_flight.get(idx, 0)
                if inflight < best_inflight:
                    best_idx = idx
                    best_inflight = inflight
                    best_sleep = 0.0

        if best_idx == -1:
            min_cooldown = float('inf')
            for idx in range(len(self._clients)):
                cooldown_val = self._cooldowns.get(idx, 0.0)
                if cooldown_val < min_cooldown:
                    min_cooldown = cooldown_val
                    best_idx = idx
                    best_sleep = max(0.0, cooldown_val - now)
                elif cooldown_val == min_cooldown:
                    if self._in_flight.get(idx, 0) < self._in_flight.get(best_idx, 0):
                        best_idx = idx
                        best_sleep = max(0.0, cooldown_val - now)

        self._in_flight[best_idx] = self._in_flight.get(best_idx, 0) + 1
        return best_idx, self._clients[best_idx], best_sleep

    async def _execute_with_retry(self, func, *args, **kwargs):
        max_attempts = len(self._clients) * 3 + 1
        for attempt in range(max_attempts):
            async with self._lock:
                idx, client, sleep_time = self._next_available_slot()
            if sleep_time > 0:
                logger.warning(
                    f"[FirecrawlPool] All slots on cooldown, sleeping {sleep_time:.1f}s..."
                )
                await asyncio.sleep(sleep_time)
            logger.debug(
                f"[FirecrawlPool] Executing in thread — slot={idx} attempt={attempt+1}/{max_attempts}"
            )
            t0 = time.time()
            try:
                result = await asyncio.to_thread(func, client, *args, **kwargs)
                elapsed = (time.time() - t0) * 1000
                logger.debug(f"[FirecrawlPool] Thread call done in {elapsed:.0f}ms")
                return result
            except Exception as e:
                elapsed = (time.time() - t0) * 1000
                err_str = str(e).lower()
                logger.error(
                    f"[FirecrawlPool] Exception after {elapsed:.0f}ms (slot={idx}, attempt={attempt+1}): "
                    f"{type(e).__name__}: {e}"
                )
                if "rate limit" in err_str or "429" in err_str:
                    cooldown = 10 + (attempt * 2)
                    async with self._lock:
                        self._cooldowns[idx] = time.time() + cooldown
                    logger.warning(f"[FirecrawlPool] Rate limited. Cooling slot {idx} for {cooldown}s.")
                    continue
                raise
            finally:
                async with self._lock:
                    self._in_flight[idx] = max(0, self._in_flight.get(idx, 1) - 1)
        raise RuntimeError("All slots exhausted due to rate limits.")

    async def search(self, query: str, limit: int = 5) -> Tuple[List[FirecrawlSearchResult], float]:
        logger.info(f"[FirecrawlPool] search() query={repr(query[:80])} limit={limit}")
        t0 = time.time()

        def do_search(client, q):
            logger.debug(f"[FirecrawlPool][thread] Calling client.search({repr(q[:60])}, limit={limit})")
            return client.search(q, limit=limit)

        result = await self._execute_with_retry(do_search, query)
        duration = (time.time() - t0) * 1000
        logger.info(f"[FirecrawlPool] search() raw result type={type(result).__name__} in {duration:.0f}ms")

        # Log raw structure for debugging
        if hasattr(result, "model_dump"):
            logger.debug(f"[FirecrawlPool] Raw search result (model_dump keys): {list(result.model_dump().keys())}")
        elif isinstance(result, dict):
            logger.debug(f"[FirecrawlPool] Raw search result (dict keys): {list(result.keys())}")
        elif isinstance(result, list):
            logger.debug(f"[FirecrawlPool] Raw search result is list, len={len(result)}")

        # Convert Pydantic models to dict if needed
        res_dict = result
        if hasattr(result, "model_dump"):
            res_dict = result.model_dump()
        elif hasattr(result, "dict"):
            res_dict = result.dict()
        elif not isinstance(result, dict):
            try:
                res_dict = dict(result)
            except Exception:
                pass

        # Firecrawl search returns a dict with 'web', or 'data' containing 'web', or 'data' array
        if isinstance(res_dict, dict) and "web" in res_dict:
            items = res_dict["web"]
            logger.debug(f"[FirecrawlPool] Parsed via 'web' key → {len(items)} items")
        elif isinstance(res_dict, dict) and "data" in res_dict:
            if isinstance(res_dict["data"], dict) and "web" in res_dict["data"]:
                items = res_dict["data"]["web"]
                logger.debug(f"[FirecrawlPool] Parsed via 'data.web' key → {len(items)} items")
            else:
                items = res_dict["data"] if isinstance(res_dict["data"], list) else []
                logger.debug(f"[FirecrawlPool] Parsed via 'data' key → {len(items)} items")
        elif isinstance(res_dict, list):
            items = res_dict
            logger.debug(f"[FirecrawlPool] Parsed as list → {len(items)} items")
        else:
            items = []
            logger.warning(f"[FirecrawlPool] Could not parse search result structure. res_dict type={type(res_dict).__name__}")
            if isinstance(res_dict, dict):
                logger.warning(f"[FirecrawlPool] Keys available: {list(res_dict.keys())}")

        formatted_results = []
        for i, item in enumerate(items):
            if isinstance(item, dict):
                formatted_results.append(
                    FirecrawlSearchResult(
                        query=query,
                        firecrawl_rank=i + 1,
                        url=item.get("url", ""),
                        title=item.get("title", ""),
                        snippet=item.get("description", ""),
                        search_latency_ms=duration
                    )
                )
            else:
                logger.debug(f"[FirecrawlPool] Skipping non-dict item at index {i}: type={type(item).__name__}")

        logger.info(f"[FirecrawlPool] search() → {len(formatted_results)} formatted results")
        return formatted_results, duration

    async def scrape(self, url: str) -> Tuple[Optional[str], float, str]:
        logger.info(f"[FirecrawlPool] scrape() url={url}")
        t0 = time.time()

        def do_scrape(client, u):
            logger.debug(f"[FirecrawlPool][thread] Calling client.scrape({u})")
            try:
                return client.scrape(u, formats=['markdown'])
            except (AttributeError, TypeError) as e:
                logger.debug(f"[FirecrawlPool][thread] client.scrape failed ({e}), falling back to scrape_url")
                return client.scrape_url(u, params={'formats': ['markdown']})

        try:
            result = await self._execute_with_retry(do_scrape, url)
            duration = (time.time() - t0) * 1000
            logger.info(f"[FirecrawlPool] scrape() raw result type={type(result).__name__} in {duration:.0f}ms")

            # Convert Pydantic models to dict if needed
            res_dict = result
            if hasattr(result, "model_dump"):
                res_dict = result.model_dump()
                logger.debug(f"[FirecrawlPool] scrape model_dump keys: {list(res_dict.keys())}")
            elif hasattr(result, "dict"):
                res_dict = result.dict()
            elif not isinstance(result, dict):
                try:
                    res_dict = dict(result)
                except Exception:
                    pass

            if isinstance(res_dict, dict):
                logger.debug(f"[FirecrawlPool] scrape dict keys: {list(res_dict.keys())}")

            # The SDK returns a dict with 'markdown' or similar
            markdown_content = None
            if isinstance(res_dict, dict):
                if "markdown" in res_dict:
                    markdown_content = res_dict["markdown"]
                    logger.debug(f"[FirecrawlPool] Got markdown via 'markdown' key, len={len(markdown_content or '')}")
                elif "data" in res_dict and isinstance(res_dict["data"], dict):
                    markdown_content = res_dict["data"].get("markdown")
                    logger.debug(f"[FirecrawlPool] Got markdown via 'data.markdown' key, len={len(markdown_content or '')}")
                else:
                    logger.warning(f"[FirecrawlPool] No markdown key found. Available keys: {list(res_dict.keys())}")

            if markdown_content:
                logger.info(f"[FirecrawlPool] scrape() → success, {len(markdown_content)} chars")
                return markdown_content, duration, "success"
            logger.warning(f"[FirecrawlPool] scrape() → empty_content for {url}")
            return None, duration, "empty_content"

        except Exception as e:
            duration = (time.time() - t0) * 1000
            logger.error(f"[FirecrawlPool] scrape() → error after {duration:.0f}ms: {type(e).__name__}: {e}")
            return None, duration, f"error: {str(e)}"
