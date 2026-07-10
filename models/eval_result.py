from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

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
class CriteriaCheck:
    """One condition from the rubric criteria, and whether it was met."""
    condition: str
    status: str         # "MET" | "PARTIALLY_MET" | "NOT_MET"
    evidence: str       # Quote from document profile supporting this classification

@dataclass
class DimensionEval:
    """Result of evaluating ONE rubric dimension. Produced by the judge."""
    dimension_name: str
    weight: float                              # From the rubric
    
    # 5-step CoT output
    evidence_found: List[str]                  # Step 1: quotes from profiles
    criteria_checklist: List[CriteriaCheck]    # Step 2: per-condition status
    contrastive_fail_triggered: bool           # Step 3: did the failure pattern match?
    contrastive_fail_explanation: str          # Step 3: why/why not
    assigned_level: str                        # Step 4: "L1" through "L5"
    level_justification: str                   # Step 4: why this level, not adjacent
    score: float                               # Step 5: precise score within level range
    reasoning: str                             # Summary sentence

@dataclass
class EvalResult:
    """Complete evaluation result for a test case. Replaces old hardcoded 3-axis model."""
    test_case_id: str
    dimension_evals: List[DimensionEval]       # One per rubric dimension
    overall_score: float                       # Weighted sum using rubric weights
    
    # Document profiles used for this evaluation (for auditability)
    document_profiles: Optional[List[Dict[str, Any]]] = None
    
    # Sanity check warnings (from bias detection)
    warnings: List[str] = field(default_factory=list)
    
    # Dedup signal
    result_diversity: Optional[Dict[str, Any]] = None

    def passes(self, overall_threshold: float = 0.65, dimension_floor: float = 0.40) -> bool:
        """Hybrid pass check: overall score AND no dimension below floor."""
        if self.overall_score < overall_threshold:
            return False
        for de in self.dimension_evals:
            if de.score < dimension_floor:
                return False
        return True
    
    @property
    def floor_failures(self) -> List[str]:
        """Return dimension names that fell below the floor."""
        return [de.dimension_name for de in self.dimension_evals if de.score < 0.40]

    # ── Backward-compatible convenience properties ──────────────────────

    @property
    def coverage_score(self) -> float:
        """Best-effort coverage score from dimension evals."""
        return self._best_score_for_axis(["coverage", "content", "accuracy", "relevance", "completeness"])

    @property
    def ranking_score(self) -> float:
        """Best-effort ranking score from dimension evals."""
        return self._best_score_for_axis(["ranking", "authority", "source", "ordering", "priority"])

    @property
    def fidelity_score(self) -> float:
        """Best-effort fidelity/scrape quality score from dimension evals."""
        return self._best_score_for_axis(["fidelity", "structure", "scrape", "noise", "formatting"])

    def _best_score_for_axis(self, keywords: List[str]) -> float:
        """Find the dimension eval whose name best matches the given axis keywords."""
        for de in self.dimension_evals:
            if any(kw in de.dimension_name.lower() for kw in keywords):
                return de.score
        return self.overall_score

    def get_dimension(self, name: str) -> Optional[DimensionEval]:
        """Get a specific dimension eval by name."""
        return next((d for d in self.dimension_evals if d.dimension_name == name), None)

    # Lightweight compatibility wrappers during migration across consumers
    @property
    def coverage(self):
        class _CompatCoverage:
            def __init__(self, score, reasoning):
                self.recall_score = score
                self.must_mention_hits = []
                self.must_mention_misses = []
                self.reasoning = reasoning
        dim = self.get_dimension("coverage") or (self.dimension_evals[0] if self.dimension_evals else None)
        reasoning = dim.reasoning if dim else "Evaluated via dynamic rubric dimensions."
        return _CompatCoverage(self.coverage_score, reasoning)

    @property
    def ranking(self):
        class _CompatRanking:
            def __init__(self, score, reasoning):
                self.ndcg_at_5 = score
                self.firecrawl_ranking = [1, 2, 3, 4, 5]
                self.llm_ideal_ranking = [1, 2, 3, 4, 5]
                self.ranking_reasoning = reasoning
                self.improvement_suggestions = []
        dim = self.get_dimension("ranking")
        reasoning = dim.reasoning if dim else "Evaluated via dynamic rubric dimensions."
        return _CompatRanking(self.ranking_score, reasoning)

    @property
    def scrape_quality(self) -> Dict[str, Any]:
        class _CompatScrapeQuality:
            def __init__(self, score, reasoning):
                self.noise_score = score
                self.structure_score = score
                self.completeness_score = score
                self.overall_markdown_quality = score
                self.issues_found = []
                self.reasoning = reasoning
        res = {}
        if self.document_profiles:
            for p in self.document_profiles:
                url = p.get("url", "unknown")
                res[url] = _CompatScrapeQuality(self.fidelity_score, "Evaluated via dynamic rubric dimensions.")
        return res

    def to_dict(self) -> dict:
        import dataclasses
        return dataclasses.asdict(self)
