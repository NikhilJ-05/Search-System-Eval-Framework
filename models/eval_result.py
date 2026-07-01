from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .test_case import TestCase

@dataclass
class FirecrawlSearchResult:
    query: str
    firecrawl_rank: int
    url: str
    title: str
    snippet: str
    full_markdown: Optional[str] = None
    scrape_latency_ms: float = 0.0
    search_latency_ms: float = 0.0
    content_length: int = 0
    status: str = "success"
    
    # Cache metadata
    query_cache_status: str = ""
    scrape_cache_status: str = ""
    cache_similarity: float = 0.0
    content_drift: Optional[Dict[str, Any]] = None
    kb_meta: Optional[Dict[str, Any]] = None

@dataclass
class CoverageEval:
    must_mention_hits: List[str]
    must_mention_misses: List[str]
    recall_score: float
    total_relevant_found: int
    min_expected: int
    coverage_passed: bool
    reasoning: str

@dataclass
class RankingEval:
    firecrawl_ranking: List[int]
    llm_ideal_ranking: List[int]
    ndcg_at_5: float
    ranking_reasoning: str
    improvement_suggestions: List[str]

@dataclass
class ScrapeIssue:
    type: str
    severity: str
    detail: str

@dataclass
class ScrapeQualityEval:
    url: str
    noise_score: float
    structure_score: float
    completeness_score: float
    overall_markdown_quality: float
    issues_found: List[ScrapeIssue]
    reasoning: str

@dataclass
class EvalResult:
    test_case_id: str
    coverage: CoverageEval
    ranking: RankingEval
    scrape_quality: Dict[str, ScrapeQualityEval]  # keyed by url
    overall_score: float

    def to_dict(self) -> dict:
        import dataclasses
        return dataclasses.asdict(self)
