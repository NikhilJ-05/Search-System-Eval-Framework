import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

@dataclass
class EvalConfig:
    # Firecrawl
    firecrawl_keys: list[str] = field(default_factory=list)

    # OpenRouter
    openrouter_keys: list[str] = field(default_factory=list)
    generator_providers: list[str] = field(default_factory=list)
    judge_providers: list[str] = field(default_factory=lambda: ["wafer", "gmicloud", "baidu"])
    improvement_agent_providers: list[str] = field(default_factory=list)

    # Qdrant
    qdrant_url: str = ""
    qdrant_key: str = ""
    qdrant_collection: str = "firecrawl_eval"

    # Models (OpenRouter slugs)
    generator_model: str = "minimax/minimax-m3"
    judge_model: str = "deepseek/deepseek-v4-flash"
    extraction_model: str = ""
    improvement_agent_model: str = "qwen/qwen3.7-plus"

    # Eval settings
    num_test_cases: int = 30
    search_results_per_query: int = 5
    scrape_top_n: int = 5
    pass_threshold: float = 0.65
    dimension_floor: float = 0.40
    sft_gold_score_threshold: float = 0.85

    # Cache settings
    kb_freshness_window_seconds: int = 600
    query_cache_similarity_threshold: float = 0.82
    judge_result_cache_ttl: int = 0
    # Minimum hybrid search score (RRF) for KB content to be reused instead of re-scraping
    kb_content_score_threshold: float = 0.38
    query_cache_eviction_max_age_seconds: int = 3600

    # Concurrency settings
    max_concurrent_tcs: int = 10

    # Scoring weights
    coverage_weight: float = 0.30
    ranking_weight: float = 0.30
    scrape_weight: float = 0.40

    # Archetype weights (must sum to 1.0)
    archetype_weights: dict = field(default_factory=lambda: {
        "none": 0.30,
        "over_decomposed": 0.10,
        "keyword_stuffed": 0.10,
        "reformulation_drift": 0.12,
        "multi_hop_compressed": 0.12,
        "temporal_ambiguity": 0.13,
        "copy_paste_artifact": 0.13,
    })
    cache_variant_min_history: int = 5

    @classmethod
    def from_env(cls) -> "EvalConfig":
        _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        load_dotenv(_env_path)
        
        # Load Firecrawl keys
        f_keys = [
            os.environ.get(f"FIRECRAWL_API_KEY_{i}") for i in range(1, 6)
        ]
        valid_f_keys = [k for k in f_keys if k]
        
        # Load OpenRouter keys
        or_keys = [
            os.environ.get(f"OPENROUTER_KEY_{i}") for i in range(1, 6)
        ]
        valid_or_keys = [k for k in or_keys if k]

        # Load generator and judge providers
        gen_provs = os.environ.get("GENERATOR_PROVIDERS")
        valid_gen_provs = [p.strip() for p in gen_provs.split(",") if p.strip()] if gen_provs is not None else []
        
        jdg_provs = os.environ.get("JUDGE_PROVIDERS")
        valid_jdg_provs = [p.strip() for p in jdg_provs.split(",") if p.strip()] if jdg_provs is not None else ["wafer", "gmicloud", "baidu"]

        imp_provs = os.environ.get("IMPROVEMENT_AGENT_PROVIDERS")
        valid_imp_provs = [p.strip() for p in imp_provs.split(",") if p.strip()] if imp_provs is not None else []

        return cls(
            firecrawl_keys=valid_f_keys,
            openrouter_keys=valid_or_keys,
            generator_providers=valid_gen_provs,
            judge_providers=valid_jdg_provs,
            improvement_agent_providers=valid_imp_provs,
            qdrant_url=os.environ.get("QDRANT_URL", ""),
            qdrant_key=os.environ.get("QDRANT_API_KEY", ""),
            qdrant_collection=os.environ.get("QDRANT_COLLECTION_NAME", "firecrawl_eval"),
            generator_model=os.environ.get("GENERATOR_MODEL", "minimax/minimax-m3"),
            judge_model=os.environ.get("JUDGE_MODEL", "deepseek/deepseek-v4-flash"),
            extraction_model=os.environ.get("EXTRACTION_MODEL", ""),
            improvement_agent_model=os.environ.get("IMPROVEMENT_AGENT_MODEL", "qwen/qwen3.7-plus"),
            num_test_cases=int(os.environ.get("NUM_TEST_CASES", "30")),
            search_results_per_query=int(os.environ.get("SEARCH_RESULTS_PER_QUERY", "5")),
            scrape_top_n=int(os.environ.get("SCRAPE_TOP_N", "5")),
            kb_freshness_window_seconds=int(os.environ.get("KB_FRESHNESS_WINDOW", "600")),
            query_cache_similarity_threshold=float(os.environ.get("QUERY_CACHE_THRESHOLD", "0.82")),
            judge_result_cache_ttl=int(os.environ.get("JUDGE_RESULT_TTL", "0")),
            max_concurrent_tcs=int(os.environ.get("MAX_CONCURRENT_TCS", "10")),
            pass_threshold=float(os.environ.get("PASS_THRESHOLD", "0.65")),
            dimension_floor=float(os.environ.get("DIMENSION_FLOOR", "0.40")),
            sft_gold_score_threshold=float(os.environ.get("SFT_GOLD_THRESHOLD", "0.85")),
            kb_content_score_threshold=float(os.environ.get("KB_CONTENT_SCORE_THRESHOLD", "0.38")),
            query_cache_eviction_max_age_seconds=int(os.environ.get("QUERY_CACHE_EVICTION_MAX_AGE", "3600")),
            coverage_weight=float(os.environ.get("COVERAGE_WEIGHT", "0.30")),
            ranking_weight=float(os.environ.get("RANKING_WEIGHT", "0.30")),
            scrape_weight=float(os.environ.get("SCRAPE_WEIGHT", "0.40")),
            cache_variant_min_history=int(os.environ.get("CACHE_VARIANT_MIN_HISTORY", "5"))
        )
