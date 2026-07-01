from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

VALID_INTENTS = [
    "factual_lookup",        # Single-answer factual question
    "comparative_research",  # Comparing multiple options
    "tutorial_howto",        # Step-by-step instructions
    "data_extraction",       # Extracting structured data (tables, lists)
    "navigational",          # Finding a specific known page
    "exploratory",           # Open-ended research
    "real_time",             # Time-sensitive current information
]

@dataclass
class TestCaseExpectedCoverage:
    must_mention: List[str]
    should_mention: List[str]
    min_relevant_results: int

@dataclass
class TestCaseExpectedRanking:
    ranking_signals: List[str]
    ideal_ranking_rationale: str
    expected_source_priority: List[str]

@dataclass
class TestCaseExpectedScrapeChallenges:
    likely_page_types: List[str]
    expected_elements: List[str]
    noise_risks: List[str]

@dataclass
class TestCase:
    id: str
    query: str
    intent: str              # Must be from VALID_INTENTS
    difficulty: str
    category: str
    expected_coverage: TestCaseExpectedCoverage
    expected_ranking: TestCaseExpectedRanking
    expected_scrape_challenges: TestCaseExpectedScrapeChallenges
    cache_intent: str = "novel"

    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        return cls(
            id=data["id"],
            query=data["query"],
            intent=data["intent"],
            difficulty=data["difficulty"],
            category=data["category"],
            expected_coverage=TestCaseExpectedCoverage(**data["expected_coverage"]),
            expected_ranking=TestCaseExpectedRanking(**data["expected_ranking"]),
            expected_scrape_challenges=TestCaseExpectedScrapeChallenges(**data["expected_scrape_challenges"]),
            cache_intent=data.get("cache_intent", "novel")
        )
