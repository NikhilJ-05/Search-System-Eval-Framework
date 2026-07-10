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

AGENT_CHAOS_ARCHETYPES = [
    "none",                  # Clean baseline agent query
    "over_decomposed",       # Query overly simplified/narrowed down, losing original intent
    "keyword_stuffed",       # Redundant or excessive keywords diluting search focus
    "reformulation_drift",   # Search query that has drifted from the core intent during retries
    "multi_hop_compressed",  # Multi-step reasoning queries collapsed into a single query
    "temporal_ambiguity",    # Queries with temporal terms (e.g. latest, current) without specific years
    "copy_paste_artifact",   # Queries containing garbage strings, prompt instructions, or tool call parameters
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
class RubricDimension:
    name: str                    # e.g., "coverage", "source_authority", "structural_fidelity"
    weight: float                # Weight of this dimension in overall scoring (sum of weights in rubric = 1.0)
    criteria: str                # High-level description of what a successful response contains
    contrastive_fail: str        # Explicit description/example of what constitutes a failure

@dataclass
class EvalRubric:
    dimensions: List[RubricDimension]
    grading_notes: str           # Meta-guidance/edge case handling for the judge

@dataclass
class TestCase:
    id: str
    query: str
    domain: str
    intent: str                  # Must be from VALID_INTENTS
    difficulty: str              # easy | medium | hard
    chaos_archetype: str         # From AGENT_CHAOS_ARCHETYPES
    cache_relationship: str      # "novel" | "same_source_different_angle" | "rephrased_same_intent" | "subset_of_parent"
    category: str = "Unknown"    # Retained for UI and downstream tool compatibility (mapped from domain)
    parent_case_id: Optional[str] = None
    rubric: Optional[EvalRubric] = None
    
    # Legacy fields retained for temporary backward compatibility during transition
    expected_coverage: Optional[Any] = None
    expected_ranking: Optional[Any] = None
    expected_scrape_challenges: Optional[Any] = None
    cache_intent: str = "novel"

    def __post_init__(self):
        # If rubric is not set but legacy expected fields are populated,
        # generate a fallback rubric dynamically.
        if self.rubric is None:
            dimensions = []
            
            if self.expected_coverage:
                must_m = getattr(self.expected_coverage, "must_mention", [])
                should_m = getattr(self.expected_coverage, "should_mention", [])
                min_r = getattr(self.expected_coverage, "min_relevant_results", 2)
                dimensions.append(RubricDimension(
                    name="coverage",
                    weight=0.25,
                    criteria=f"Must contain: {', '.join(must_m)}. Should contain: {', '.join(should_m)}. Expected min relevant results: {min_r}.",
                    contrastive_fail=f"Fails if any of the core entities ({', '.join(must_m)}) are missing."
                ))
                
            if self.expected_ranking:
                priority = getattr(self.expected_ranking, "expected_source_priority", [])
                rationale = getattr(self.expected_ranking, "ideal_ranking_rationale", "")
                dimensions.append(RubricDimension(
                    name="source_authority",
                    weight=0.35,
                    criteria=f"Should prioritize domains: {', '.join(priority)}. Rationale: {rationale}",
                    contrastive_fail="Fails if lower quality or aggregator websites rank above official sources."
                ))
                
            if self.expected_scrape_challenges:
                elements = getattr(self.expected_scrape_challenges, "expected_elements", [])
                noise = getattr(self.expected_scrape_challenges, "noise_risks", [])
                dimensions.append(RubricDimension(
                    name="structural_fidelity",
                    weight=0.40,
                    criteria=f"Preserve key elements: {', '.join(elements)}. Avoid leakage of: {', '.join(noise)}",
                    contrastive_fail="Fails if layouts/tables are flattened, page is truncated, or noise/navigation dominates."
                ))
                
            if dimensions:
                # Normalize weights to sum to 1.0
                total_w = sum(d.weight for d in dimensions)
                for d in dimensions:
                    d.weight = round(d.weight / total_w, 2)
                diff = round(1.0 - sum(d.weight for d in dimensions[:-1]), 2)
                dimensions[-1].weight = diff
                
                self.rubric = EvalRubric(
                    dimensions=dimensions,
                    grading_notes="Autogenerated fallback rubric from legacy instantiation."
                )

    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        # Handle new format
        if "rubric" in data and data["rubric"] is not None:
            rubric_data = data["rubric"]
            dimensions = [
                RubricDimension(**d) for d in rubric_data.get("dimensions", [])
            ]
            rubric = EvalRubric(
                dimensions=dimensions,
                grading_notes=rubric_data.get("grading_notes", "")
            )
            domain = data.get("domain", data.get("category", "Unknown"))
            category = data.get("category", domain)
            return cls(
                id=data["id"],
                query=data["query"],
                domain=domain,
                intent=data["intent"],
                difficulty=data["difficulty"],
                chaos_archetype=data.get("chaos_archetype", "none"),
                cache_relationship=data.get("cache_relationship", "novel"),
                category=category,
                parent_case_id=data.get("parent_case_id"),
                rubric=rubric,
                cache_intent=data.get("cache_intent", "novel")
            )
        
        # Handle old format (backward compatibility fallback)
        # Create fallback dimensions from old fields
        dimensions = []
        coverage = data.get("expected_coverage", {})
        if coverage:
            must_m = coverage.get("must_mention", [])
            should_m = coverage.get("should_mention", [])
            min_r = coverage.get("min_relevant_results", 2)
            dimensions.append(RubricDimension(
                name="coverage",
                weight=0.25,
                criteria=f"Must contain: {', '.join(must_m)}. Should contain: {', '.join(should_m)}. Expected min relevant results: {min_r}.",
                contrastive_fail=f"Fails if any of the core entities ({', '.join(must_m)}) are missing."
            ))
            
        ranking = data.get("expected_ranking", {})
        if ranking:
            priority = ranking.get("expected_source_priority", [])
            rationale = ranking.get("ideal_ranking_rationale", "")
            dimensions.append(RubricDimension(
                name="source_authority",
                weight=0.35,
                criteria=f"Should prioritize domains: {', '.join(priority)}. Rationale: {rationale}",
                contrastive_fail="Fails if lower quality or aggregator websites rank above official sources."
            ))
            
        scrape = data.get("expected_scrape_challenges", {})
        if scrape:
            elements = scrape.get("expected_elements", [])
            noise = scrape.get("noise_risks", [])
            dimensions.append(RubricDimension(
                name="structural_fidelity",
                weight=0.40,
                criteria=f"Preserve key elements: {', '.join(elements)}. Avoid leakage of: {', '.join(noise)}",
                contrastive_fail="Fails if layouts/tables are flattened, page is truncated, or noise/navigation dominates."
            ))
            
        # Standardize sum of weights if dimensions exist
        if dimensions:
            total_w = sum(d.weight for d in dimensions)
            for d in dimensions:
                d.weight = round(d.weight / total_w, 2)
                
        rubric = EvalRubric(
            dimensions=dimensions,
            grading_notes="Autogenerated legacy rubric fallback."
        )
        
        domain = data.get("category", "Unknown")
        category = data.get("category", domain)
        return cls(
            id=data["id"],
            query=data["query"],
            domain=domain,
            intent=data["intent"],
            difficulty=data["difficulty"],
            chaos_archetype="none",
            cache_relationship=data.get("cache_intent", "novel"),
            category=category,
            parent_case_id=None,
            rubric=rubric,
            expected_coverage=coverage,
            expected_ranking=ranking,
            expected_scrape_challenges=scrape,
            cache_intent=data.get("cache_intent", "novel")
        )

