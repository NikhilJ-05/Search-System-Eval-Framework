import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

@dataclass
class EvalConfig:
    # Firecrawl
    firecrawl_keys: list[str] = field(default_factory=list)

    # OpenRouter
    openrouter_keys: list[str] = field(default_factory=list)
    generator_providers: list[str] = field(default_factory=lambda: ["deepseek"])
    judge_providers: list[str] = field(default_factory=lambda: ["wafer", "gmicloud", "baidu"])
    improvement_agent_providers: list[str] = field(default_factory=lambda: ["deepseek"])

    # Qdrant
    qdrant_url: str = ""
    qdrant_key: str = ""
    qdrant_collection: str = "firecrawl_eval"

    # Models (OpenRouter slugs)
    generator_model: str = "deepseek/deepseek-v4-pro"
    judge_model: str = "deepseek/deepseek-v4-flash"
    improvement_agent_model: str = "deepseek/deepseek-v4-pro"

    # Eval settings
    num_test_cases: int = 30
    batch_size: int = 1
    search_results_per_query: int = 5
    scrape_top_n: int = 5
    pass_threshold: float = 0.7

    # Cache settings
    kb_freshness_window_seconds: int = 600
    query_cache_similarity_threshold: float = 0.82
    judge_result_cache_ttl: int = 0
    # Minimum hybrid search score (RRF) for KB content to be reused instead of re-scraping
    kb_content_score_threshold: float = 0.08

    # Concurrency settings
    max_concurrent_tcs: int = 10

    # Scoring weights
    coverage_weight: float = 0.25
    ranking_weight: float = 0.35
    scrape_weight: float = 0.40

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
        valid_gen_provs = [p.strip() for p in gen_provs.split(",") if p.strip()] if gen_provs is not None else ["deepseek"]
        
        jdg_provs = os.environ.get("JUDGE_PROVIDERS")
        valid_jdg_provs = [p.strip() for p in jdg_provs.split(",") if p.strip()] if jdg_provs is not None else ["wafer", "gmicloud", "baidu"]

        imp_provs = os.environ.get("IMPROVEMENT_AGENT_PROVIDERS")
        valid_imp_provs = [p.strip() for p in imp_provs.split(",") if p.strip()] if imp_provs is not None else ["deepseek"]

        return cls(
            firecrawl_keys=valid_f_keys,
            openrouter_keys=valid_or_keys,
            generator_providers=valid_gen_provs,
            judge_providers=valid_jdg_provs,
            improvement_agent_providers=valid_imp_provs,
            qdrant_url=os.environ.get("QDRANT_URL", ""),
            qdrant_key=os.environ.get("QDRANT_API_KEY", ""),
            qdrant_collection=os.environ.get("QDRANT_COLLECTION_NAME", "firecrawl_eval"),
            generator_model=os.environ.get("GENERATOR_MODEL", "deepseek/deepseek-v4-pro"),
            judge_model=os.environ.get("JUDGE_MODEL", "deepseek/deepseek-v4-flash"),
            improvement_agent_model=os.environ.get("IMPROVEMENT_AGENT_MODEL", "deepseek/deepseek-v4-pro"),
            num_test_cases=int(os.environ.get("NUM_TEST_CASES", "30")),
            batch_size=int(os.environ.get("BATCH_SIZE", "1")),
            kb_freshness_window_seconds=int(os.environ.get("KB_FRESHNESS_WINDOW", "600")),
            query_cache_similarity_threshold=float(os.environ.get("QUERY_CACHE_THRESHOLD", "0.82")),
            judge_result_cache_ttl=int(os.environ.get("JUDGE_RESULT_TTL", "0")),
            max_concurrent_tcs=int(os.environ.get("MAX_CONCURRENT_TCS", "10")),
            pass_threshold=float(os.environ.get("PASS_THRESHOLD", "0.7")),
            kb_content_score_threshold=float(os.environ.get("KB_CONTENT_SCORE_THRESHOLD", "0.08"))
        )
