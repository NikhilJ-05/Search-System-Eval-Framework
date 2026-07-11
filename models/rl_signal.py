from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class DPOVariant:
    url: str
    content_snippet: str
    firecrawl_rank: int
    judge_score: float

@dataclass
class DPOPair:
    query: str
    test_case_id: str
    chosen: DPOVariant
    rejected: DPOVariant
    preference_rationale: str
    dimension_context: str = ""

@dataclass
class RewardComponents:
    relevance: float
    completeness: float
    freshness: float
    markdown_quality: float
    authority: float = 0.0

@dataclass
class Trajectory:
    search_rank: int
    ideal_rank: int
    rank_delta: int

@dataclass
class RewardSignal:
    query: str
    test_case_id: str
    url: str
    reward_components: RewardComponents
    composite_reward: float
    trajectory: Trajectory
    diagnostic_notes: str = ""

@dataclass
class TCMicroPattern:
    """Per-TC failure/improvement pattern from diagnostic LLM."""
    test_case_id: str
    pattern_type: str
    affected_dimension: str
    severity: str
    description: str
    suggested_fix: str

@dataclass
class ImprovementPattern:
    issue: str
    frequency: str
    description: str
    suggested_fix: str
    affected_queries: List[str] = field(default_factory=list)
    affected_urls: List[str] = field(default_factory=list)
    severity: str = "medium"
    affected_tcs: List[str] = field(default_factory=list)

@dataclass
class ListwiseRankingExample:
    """Full ideal ordering of URLs for one query, derived from LLM quality annotations."""
    query: str
    test_case_id: str
    intent: str
    difficulty: str
    ideal_ranking: List[str]           # Ordered list of URLs, best first
    url_quality_scores: Dict[str, float]  # url -> quality score (0.0-1.0)
    url_quality_notes: Dict[str, str]     # url -> short note
    firecrawl_ranking: List[str]          # Original FC order for comparison
    source: str                           # always "judge_quality_annotations"
    confidence: str                       # "high" | "medium" | "low"

@dataclass
class ContrastiveFailPair:
    """A training pair derived from a triggered contrastive fail check on a rubric dimension."""
    query: str
    test_case_id: str
    dimension: str
    bad_state: Dict[str, Any]    # {"url", "rank", "page_type", "domain_type", "snippet"}
    good_state: Dict[str, Any]   # {"url", "rank", "page_type", "domain_type", "snippet"}
    failure_explanation: str     # DimensionEval.contrastive_fail_explanation
    judge_score: float
    failure_level: str           # "L1" | "L2"

@dataclass
class QueryReformulationPair:
    """An original failing/weak query paired with an LLM-suggested better formulation."""
    test_case_id: str
    original_query: str
    reformulated_query: str
    chaos_archetype: str         # e.g. "temporal_ambiguity"
    intent: str
    failing_dimensions: List[str]
    expected_coverage_delta: str  # e.g. "+0.15 coverage" - qualitative LLM estimate
    rationale: str

@dataclass
class SFTGoldExample:
    """A high-scoring TC used as a supervised positive training example."""
    query: str
    test_case_id: str
    intent: str
    difficulty: str
    chaos_archetype: str
    overall_score: float
    gold_urls: List[str]          # Ordered by ideal rank (from quality annotations or FC order)
    key_claims_covered: List[str] # Union of key_claims from all top-ranked document profiles
    dimension_scores: Dict[str, float]  # dimension_name -> score
    rubric_dimensions: List[Dict[str, Any]]  # Full rubric for context

@dataclass
class ScrapeQualityLabel:
    """Per-URL scrape quality label derived from judge's structure profile + fidelity score."""
    url: str
    test_case_id: str
    quality_label: str            # "excellent" | "good" | "poor" | "unusable"
    fidelity_score: float
    issues: List[str]             # e.g. ["table_flattened", "truncated", "nav_noise_dominant"]
    noise_ratio: float            # nav_link_ratio from structure profile
    word_count: int
    has_tables: bool
    tables_preserved: bool        # True if table_count > 0 AND fidelity_score >= 0.7
    appears_truncated: bool
    boilerplate_pattern_count: int
    content_completeness: str     # From LLM content profile
    domain_type: str
