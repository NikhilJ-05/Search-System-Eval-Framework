import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

@dataclass
class EvalConfig:
    # Firecrawl
    firecrawl_keys: list[str] = field(default_factory=list)

    # OpenRouter
    openrouter_keys: list[str] = field(default_factory=list)
    generator_providers: list[str] = field(default_factory=lambda: ["Parasail", "Together", "DeepInfra"])
    p1_providers: list[str] = field(default_factory=lambda: ["Baidu", "GMICloud", "Fireworks"])
    p2_providers: list[str] = field(default_factory=lambda: ["Baidu", "GMICloud", "Fireworks"])
    improvement_agent_providers: list[str] = field(default_factory=lambda: ["StreamLake", "Novita"])

    # Qdrant
    qdrant_url: str = ""
    qdrant_key: str = ""
    qdrant_collection: str = "firecrawl_eval"

    # Models (OpenRouter slugs)
    generator_model: str = "minimax/minimax-m3"
    p1_model: str = "deepseek/deepseek-v4-flash"
    p2_model: str = "deepseek/deepseek-v4-flash"

    improvement_agent_model: str = "z-ai/glm-5.2"

    # LLM Settings
    llm_read_timeout_s: int = 3600
    judge_max_retries: int = 2

    # Eval settings
    num_test_cases: int = 30
    search_results_per_query: int = 5
    scrape_top_n: int = 5
    pass_threshold: float = 0.65
    dimension_floor: float = 0.40
    sft_gold_score_threshold: float = 0.85

    # Cache settings
    kb_freshness_window_seconds: int = 900
    query_cache_similarity_threshold: float = 0.95
    judge_result_cache_ttl: int = 0
    # Minimum hybrid search score (RRF) for KB content to be reused instead of re-scraping
    kb_content_score_threshold: float = 0.08
    query_cache_eviction_max_age_seconds: int = 3600

    # Concurrency settings

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
        load_dotenv(_env_path, override=True)
        
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

        kwargs = {
            "firecrawl_keys": valid_f_keys,
            "openrouter_keys": valid_or_keys,
            "qdrant_url": os.environ.get("QDRANT_URL", ""),
            "qdrant_key": os.environ.get("QDRANT_API_KEY", ""),
        }
        
        def set_if_present(env_key: str, kwarg_key: str, transform=None):
            val = os.environ.get(env_key)
            if val is not None:
                try:
                    kwargs[kwarg_key] = transform(val) if transform else val
                except ValueError:
                    pass

        def parse_providers(val: str) -> list[str]:
            return [p.strip() for p in val.split(",") if p.strip()]

        set_if_present("GENERATOR_PROVIDERS", "generator_providers", parse_providers)
        set_if_present("P1_PROVIDERS", "p1_providers", parse_providers)
        set_if_present("P2_PROVIDERS", "p2_providers", parse_providers)
        set_if_present("IMPROVEMENT_AGENT_PROVIDERS", "improvement_agent_providers", parse_providers)

        set_if_present("QDRANT_COLLECTION_NAME", "qdrant_collection")
        set_if_present("GENERATOR_MODEL", "generator_model")
        set_if_present("P1_MODEL", "p1_model")
        set_if_present("P2_MODEL", "p2_model")
        set_if_present("IMPROVEMENT_AGENT_MODEL", "improvement_agent_model")
        
        set_if_present("LLM_READ_TIMEOUT_S", "llm_read_timeout_s", int)
        set_if_present("JUDGE_MAX_RETRIES", "judge_max_retries", int)
        set_if_present("NUM_TEST_CASES", "num_test_cases", int)
        set_if_present("SEARCH_RESULTS_PER_QUERY", "search_results_per_query", int)
        set_if_present("SCRAPE_TOP_N", "scrape_top_n", int)
        
        set_if_present("KB_FRESHNESS_WINDOW", "kb_freshness_window_seconds", int)
        set_if_present("QUERY_CACHE_THRESHOLD", "query_cache_similarity_threshold", float)
        set_if_present("JUDGE_RESULT_TTL", "judge_result_cache_ttl", int)
        
        set_if_present("PASS_THRESHOLD", "pass_threshold", float)
        set_if_present("DIMENSION_FLOOR", "dimension_floor", float)
        set_if_present("SFT_GOLD_THRESHOLD", "sft_gold_score_threshold", float)
        set_if_present("KB_CONTENT_SCORE_THRESHOLD", "kb_content_score_threshold", float)
        set_if_present("QUERY_CACHE_EVICTION_MAX_AGE", "query_cache_eviction_max_age_seconds", int)
        set_if_present("CACHE_VARIANT_MIN_HISTORY", "cache_variant_min_history", int)

        def _parse_archetype_weights(raw: str) -> dict:
            if not raw:
                return None
            result = {}
            for pair in raw.split(","):
                k, _, v = pair.strip().partition(":")
                if k and v:
                    result[k.strip()] = float(v.strip())
            return result

        archetype_env = os.environ.get("ARCHETYPE_WEIGHTS")
        if archetype_env:
            parsed = _parse_archetype_weights(archetype_env)
            if parsed:
                kwargs["archetype_weights"] = parsed

        return cls(**kwargs)
