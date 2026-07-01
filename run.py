"""
run.py — Single entry point for the Firecrawl Eval Showcase pipeline.

Usage:
  python run.py                     # Start the web dashboard (FastAPI + SSE)
  python run.py --cli               # Full pipeline run in terminal
  python run.py --cli --cases 5     # Quick test with only 5 test cases
  python run.py --calibrate-only    # Only run judge calibration pre-flight
"""
import asyncio
import argparse
import logging
import sys
import os

# ── pretty logging ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("run")

# ── suppress noisy deps ────────────────────────────────────────────────────────
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("qdrant_client").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("FlagEmbedding").setLevel(logging.INFO)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("sse_starlette").setLevel(logging.WARNING)
logging.getLogger("sse_starlette.sse").setLevel(logging.WARNING)
logging.getLogger("firecrawl").setLevel(logging.WARNING)
logging.getLogger("datasets").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

async def run_pipeline(num_cases: int = None):
    from config import EvalConfig
    from pipeline.orchestrator import Orchestrator, sse_queue_var

    config = EvalConfig.from_env()
    if num_cases:
        config.num_test_cases = num_cases

    logger.info("=" * 60)
    logger.info("  Firecrawl Eval Showcase — Full Pipeline Run")
    logger.info("=" * 60)
    logger.info(f"  Generator model : {config.generator_model}")
    logger.info(f"  Judge model     : {config.judge_model}")
    logger.info(f"  Test cases      : {config.num_test_cases}")
    logger.info(f"  Generator prov  : {config.generator_providers or 'any'}")
    logger.info(f"  Judge prov      : {config.judge_providers or 'any'}")
    logger.info(f"  Qdrant URL      : {config.qdrant_url or 'not configured'}")
    logger.info("=" * 60)

    # Wire up an asyncio queue and drain it to print SSE events to stdout
    q = asyncio.Queue()

    async def drain_events():
        phases = {
            "calibration":           "[1/7] Calibration",
            "test_generation":       "[2/7] Test Generation",
            "retrieval_comparison":  "[5/7] Retrieval Comparison",
            "rl_signals":            "[6/7] RL Signal Generation",
            "report":                "[7/7] Building Report",
        }
        while True:
            try:
                ev = await asyncio.wait_for(q.get(), timeout=2.0)
                t = ev.get("type", "")

                if t == "run_start":
                    logger.info(f"Run started: {ev['run_id']}")
                elif t == "phase_start":
                    label = phases.get(ev["phase"], ev["phase"])
                    msg   = ev.get("message", "")
                    logger.info(f"{label}  {msg}")
                elif t == "test_case_created":
                    logger.info(f"    [TC] {ev['tc_id']}  \"{ev['query'][:60]}\"")
                elif t == "firecrawl_search_done":
                    logger.info(f"    [FC Search]  {ev['tc_id']}  {ev['result_count']} results  {ev['latency_ms']:.0f}ms")
                elif t == "firecrawl_scrape_done":
                    status_icon = "OK" if ev["status"] == "success" else "!!"
                    logger.info(f"    [Scrape {status_icon}]  {ev['tc_id']}  {ev['url'][:60]}")
                elif t == "judge_scored":
                    logger.info(
                        f"    [Judge]  {ev['tc_id']}  "
                        f"cov={ev['coverage']:.2f}  rnk={ev['ranking']:.2f}  "
                        f"scr={ev.get('scrape', 0):.2f}  overall={ev['overall']:.2f}"
                    )
                elif t == "indexed":
                    logger.info(f"    [Index]  {ev['tc_id']}  indexed to Qdrant")
                elif t == "phase_complete":
                    logger.info(f"    Phase complete: {ev['phase']}  {ev}")
                elif t == "run_complete":
                    logger.info("=" * 60)
                    logger.info(f"  Run complete: {ev['run_id']}")
                    logger.info(f"  Overall score: {ev['overall_score']:.3f}")
                    logger.info("=" * 60)
                    break
                elif t == "run_error":
                    logger.error(f"Pipeline error: {ev['error']}")
                    break
            except asyncio.TimeoutError:
                pass  # still running

    token = sse_queue_var.set(q)
    drain_task = asyncio.create_task(drain_events())
    try:
        orch = Orchestrator(config)
        run_id = await orch.run_pipeline()
    finally:
        sse_queue_var.reset(token)
        await drain_task

async def run_calibration_only():
    from config import EvalConfig
    from clients.openrouter import OpenRouterClientPool
    from eval.judge import Judge
    from eval.calibration import JudgeCalibration

    config = EvalConfig.from_env()
    or_pool = OpenRouterClientPool(config)
    judge = Judge(config, or_pool)
    calib = JudgeCalibration()
    try:
        result = await calib.run_calibration(judge)
        logger.info(f"Calibration result: {'PASSED' if result else 'FAILED'}")
    finally:
        await or_pool.aclose()

def run_server():
    import uvicorn
    logger.info("Starting Firecrawl Eval Dashboard at http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

def main():
    parser = argparse.ArgumentParser(description="Firecrawl Eval Showcase")
    parser.add_argument("--cli", action="store_true",
                        help="Run the pipeline in CLI mode (no web server)")
    parser.add_argument("--calibrate-only", action="store_true",
                        help="Run only judge calibration pre-flight check")
    parser.add_argument("--cases", type=int, default=None,
                        help="Override NUM_TEST_CASES for this run (e.g. --cases 5 for a quick test)")
    args = parser.parse_args()

    if args.cli:
        asyncio.run(run_pipeline(num_cases=args.cases))
    elif args.calibrate_only:
        asyncio.run(run_calibration_only())
    else:
        run_server()

if __name__ == "__main__":
    main()
