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
    chosen: DPOVariant
    rejected: DPOVariant
    preference_rationale: str

@dataclass
class RewardComponents:
    relevance: float
    completeness: float
    freshness: float
    markdown_quality: float

@dataclass
class Trajectory:
    search_rank: int
    ideal_rank: int
    rank_delta: int

@dataclass
class RewardSignal:
    query: str
    url: str
    reward_components: RewardComponents
    composite_reward: float
    trajectory: Trajectory

@dataclass
class ImprovementPattern:
    issue: str
    frequency: str
    description: str
    suggested_fix: str
    affected_queries: List[str] = field(default_factory=list)
    affected_urls: List[str] = field(default_factory=list)
