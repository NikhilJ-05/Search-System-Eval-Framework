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
