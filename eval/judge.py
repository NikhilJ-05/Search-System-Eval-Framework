import json
import logging
import asyncio
import hashlib
import os
import time
from typing import Dict, Any, Tuple
from models.test_case import TestCase
from models.eval_result import FirecrawlSearchResult, CoverageEval, RankingEval, ScrapeQualityEval, ScrapeIssue, EvalResult
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)

class Judge:
    def __init__(self, config: EvalConfig, or_pool: OpenRouterClientPool):
        self.config = config
        self.or_pool = or_pool
        self.model = config.judge_model
        self._judge_cache: Dict[str, EvalResult] = {}

    def _parse_json(self, clean_response: str) -> dict:
        clean_response = clean_response.strip()
        if not clean_response:
            return {}

        # Strategy 1: Try direct parse first
        try:
            return json.loads(clean_response)
        except Exception:
            pass

        # Strategy 2: Extract outermost {...}
        first_brace = clean_response.find('{')
        last_brace = clean_response.rfind('}')
        if first_brace != -1 and last_brace > first_brace:
            try:
                return json.loads(clean_response[first_brace:last_brace+1])
            except Exception:
                pass

        # Strategy 3: Code fence block
        import re
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', clean_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except Exception:
                pass

        logger.error(f"[Judge] Failed to parse JSON from response. First 300 chars: {clean_response[:300]}")
        raise ValueError(f"Could not parse valid JSON object from response: {clean_response[:200]}")

    async def _eval_coverage(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> CoverageEval:
        # Include scraped markdown (first 2000 chars) so coverage isn't limited to the 500-char snippet.
        # Government portals and PDFs often contain must_mention terms deep in the body, not the snippet.
        MAX_MD_PREVIEW = 2000
        results_data = [
            {
                "title": r.title,
                "snippet": r.snippet[:500] if r.snippet else "",
                "content_preview": r.full_markdown[:MAX_MD_PREVIEW] if r.full_markdown else ""
            }
            for r in search_results
        ]
        system_prompt = """You are a Coverage Judge. Keep your reasoning extremely concise (1-2 sentences max).
Evaluate search coverage based on must_mention and should_mention items.
For each item in must_mention, search through the result title, snippet, AND content_preview (first part of scraped page body). Quote the exact text where you found each item. If not found in any field, explain what's missing.
Output JSON:
{
  "reasoning": "string explanation quoting evidence",
  "must_mention_hits": ["found item"],
  "must_mention_misses": ["missing item"],
  "recall_score": 0.0 to 1.0,
  "total_relevant_found": integer,
  "min_expected": integer,
  "coverage_passed": boolean
}"""
        prompt = f"Test Case:\nMust mention: {test_case.expected_coverage.must_mention}\nShould mention: {test_case.expected_coverage.should_mention}\nMin expected: {test_case.expected_coverage.min_relevant_results}\n\nResults:\n{json.dumps(results_data)}"
        
        raw_response = await self.or_pool.generate(
            prompt=prompt,
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"},
            system_prompt=system_prompt,
            max_tokens=16000,
            providers=self.config.judge_providers
        )
        data = self._parse_json(raw_response)
        return CoverageEval(
            reasoning=data.get("reasoning", ""),
            must_mention_hits=data.get("must_mention_hits", []),
            must_mention_misses=data.get("must_mention_misses", []),
            recall_score=float(data.get("recall_score", 0.0)),
            total_relevant_found=int(data.get("total_relevant_found", 0)),
            min_expected=int(data.get("min_expected", test_case.expected_coverage.min_relevant_results)),
            coverage_passed=bool(data.get("coverage_passed", False)),
        )

    async def _eval_ranking(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> RankingEval:
        results_data = [{"rank": r.firecrawl_rank, "url": r.url, "title": r.title, "snippet": r.snippet[:300] if r.snippet else ""} for r in search_results]
        system_prompt = """You are a Ranking Judge. Keep your reasoning extremely concise (1-2 sentences max explaining the order).
Given the query intent and ranking signals, what is the ideal ordering? Use expected_source_priority as your primary guide. Output the ideal ranking as a permutation of indices [1..N]. Explain each swap.
Output JSON:
{
  "ranking_reasoning": "string explaining each swap based on source priority",
  "firecrawl_ranking": [1, 2, 3],
  "llm_ideal_ranking": [2, 1, 3],
  "ndcg_at_5": 0.0 to 1.0,
  "improvement_suggestions": ["suggestion"]
}"""
        prompt = f"Query: {test_case.query}\nRanking signals: {test_case.expected_ranking.ranking_signals}\nSource Priority: {test_case.expected_ranking.expected_source_priority}\nRationale: {test_case.expected_ranking.ideal_ranking_rationale}\n\nResults:\n{json.dumps(results_data)}"
        
        raw_response = await self.or_pool.generate(
            prompt=prompt,
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"},
            system_prompt=system_prompt,
            max_tokens=16000,
            providers=self.config.judge_providers
        )
        data = self._parse_json(raw_response)
        return RankingEval(
            ranking_reasoning=data.get("ranking_reasoning", ""),
            firecrawl_ranking=data.get("firecrawl_ranking", list(range(1, len(search_results) + 1))),
            llm_ideal_ranking=data.get("llm_ideal_ranking", list(range(1, len(search_results) + 1))),
            ndcg_at_5=float(data.get("ndcg_at_5", 0.0)),
            improvement_suggestions=data.get("improvement_suggestions", []),
        )

    async def _eval_scrape(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> Dict[str, ScrapeQualityEval]:
        MAX_MD_PER_URL = 8000
        results_data = []
        for r in search_results:
            if not r.full_markdown: continue
            results_data.append({
                "url": r.url,
                "scraped_markdown": r.full_markdown[:MAX_MD_PER_URL],
                "markdown_length": len(r.full_markdown)
            })
            
        system_prompt = """You are a Scrape Quality Judge.
For each URL, read the full markdown and answer these specific questions:
1. ELEMENTS: For each expected_element, is it present and properly formatted? Quote it.
2. NOISE: For each noise_risk, did it leak into the markdown? Quote it.
3. STRUCTURE: Are headings, code blocks, tables, and lists properly preserved?
4. COMPLETENESS: Does the content appear truncated?
Output JSON mapping URL to scrape quality:
{
  "url_1": {
    "url": "url_1",
    "reasoning": "string with specific quotes",
    "noise_score": 0.0 to 1.0,
    "structure_score": 0.0 to 1.0,
    "completeness_score": 0.0 to 1.0,
    "overall_markdown_quality": 0.0 to 1.0,
    "issues_found": [
      {"type": "missing_element", "severity": "high", "detail": "Table missing"}
    ]
  }
}"""
        prompt = f"Query: {test_case.query}\nExpected Elements: {test_case.expected_scrape_challenges.expected_elements}\nNoise Risks: {test_case.expected_scrape_challenges.noise_risks}\n\nResults:\n{json.dumps(results_data)}"
        
        if not results_data:
            return {}
            
        raw_response = await self.or_pool.generate(
            prompt=prompt,
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"},
            system_prompt=system_prompt,
            max_tokens=16000,
            providers=self.config.judge_providers
        )
        data = self._parse_json(raw_response)

        # Normalize: LLM sometimes returns a list [{url: ..., ...}] instead of a dict {url: {...}}
        if isinstance(data, list):
            data = {item["url"]: item for item in data if isinstance(item, dict) and "url" in item}

        scrape_quality = {}
        for url, sq_data in data.items():
            if not isinstance(sq_data, dict):
                logger.warning(f"[Judge] Unexpected scrape data type for url {url}: {type(sq_data)}")
                continue
            raw_issues = sq_data.get("issues_found", [])
            issues = []
            for i in raw_issues:
                if isinstance(i, dict):
                    issues.append(ScrapeIssue(
                        type=i.get("type", "unknown"),
                        severity=i.get("severity", "medium"),
                        detail=i.get("detail", ""),
                    ))
            scrape_quality[url] = ScrapeQualityEval(
                url=sq_data.get("url", url),
                reasoning=sq_data.get("reasoning", ""),
                noise_score=float(sq_data.get("noise_score", 0.0)),
                structure_score=float(sq_data.get("structure_score", 1.0)),
                completeness_score=float(sq_data.get("completeness_score", 1.0)),
                overall_markdown_quality=float(sq_data.get("overall_markdown_quality", 0.5)),
                issues_found=issues,
            )
        return scrape_quality

    def _get_disk_cache_path(self) -> str:
        cache_dir = os.path.join(APP_DIR, "outputs", "data")
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, "judge_cache.json")

    def _load_disk_cache(self, key: str) -> EvalResult:
        if self.config.judge_result_cache_ttl <= 0:
            return None
        path = self._get_disk_cache_path()
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            entry = data.get(key)
            if entry and (time.time() - entry.get("timestamp", 0)) < self.config.judge_result_cache_ttl:
                return EvalResult.from_dict(entry["eval_result"])
        except Exception as e:
            logger.warning(f"Failed to load judge disk cache: {e}")
        return None

    def _save_disk_cache(self, key: str, res: EvalResult):
        if self.config.judge_result_cache_ttl <= 0:
            return
        path = self._get_disk_cache_path()
        data = {}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        data[key] = {
            "timestamp": time.time(),
            "eval_result": res.to_dict()
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
            logger.warning(f"Failed to save judge disk cache: {e}")

    async def evaluate(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> EvalResult:
        logger.info(f"Evaluating tc: {test_case.id} with concurrent passes")
        
        # Compute deterministic cache key
        cache_str = f"{test_case.query}|{sorted([r.url for r in search_results])}|{sorted(test_case.expected_coverage.must_mention)}"
        cache_key = hashlib.sha256(cache_str.encode("utf-8")).hexdigest()

        if cache_key in self._judge_cache:
            logger.info(f"[Judge] In-memory cache hit for {test_case.id}")
            return self._judge_cache[cache_key]

        disk_cached = self._load_disk_cache(cache_key)
        if disk_cached:
            logger.info(f"[Judge] Disk TTL cache hit for {test_case.id}")
            self._judge_cache[cache_key] = disk_cached
            return disk_cached

        try:
            coverage, ranking, scrape_quality = await asyncio.gather(
                self._eval_coverage(test_case, search_results),
                self._eval_ranking(test_case, search_results),
                self._eval_scrape(test_case, search_results)
            )
            
            avg_scrape_quality = sum(sq.overall_markdown_quality for sq in scrape_quality.values()) / max(1, len(scrape_quality))
            overall = (
                self.config.coverage_weight * coverage.recall_score +
                self.config.ranking_weight * ranking.ndcg_at_5 +
                self.config.scrape_weight * avg_scrape_quality
            )
            
            # Sanity check
            all_scores = [coverage.recall_score, ranking.ndcg_at_5] + [sq.overall_markdown_quality for sq in scrape_quality.values()]
            if all_scores and (all(s == 1.0 for s in all_scores) or all(s == 0.0 for s in all_scores)):
                logger.warning(f"[Judge] SUSPICIOUS: All scores for TC {test_case.id} are exactly {all_scores[0]}. Model might be defaulting.")
            
            res = EvalResult(
                test_case_id=test_case.id,
                coverage=coverage,
                ranking=ranking,
                scrape_quality=scrape_quality,
                overall_score=overall
            )
            self._judge_cache[cache_key] = res
            self._save_disk_cache(cache_key, res)
            return res
        except Exception as e:
            logger.error(f"Judge failed on {test_case.id}: {e}")
            raise
