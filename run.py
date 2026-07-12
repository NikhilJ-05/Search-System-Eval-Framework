"""
run.py — Single entry point for the EvalOS Framework pipeline.

Usage:
  python run.py                     # Start the web dashboard and open browser
  python run.py --cli               # Full pipeline run in terminal
  python run.py --cli --cases 5     # Quick test with only 5 test cases
"""
import asyncio
import argparse
import logging
import sys
import os
import threading
import time
import webbrowser

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
    logger.info("  EvalOS Framework — Full Pipeline Run")
    logger.info("=" * 60)
    logger.info(f"  Generator model : {config.generator_model}")
    logger.info(f"  P1 model        : {config.p1_model}")
    logger.info(f"  P2 model        : {config.p2_model}")
    logger.info(f"  Test cases      : {config.num_test_cases}")
    logger.info(f"  Generator prov  : {config.generator_providers or 'any'}")
    logger.info(f"  P1 prov         : {config.p1_providers or 'any'}")
    logger.info(f"  P2 prov         : {config.p2_providers or 'any'}")
    logger.info(f"  Qdrant URL      : {config.qdrant_url or 'not configured'}")
    logger.info("=" * 60)

    # Wire up an asyncio queue and drain it to print SSE events to stdout
    q = asyncio.Queue()

    async def drain_events():
        while True:
            try:
                ev = await asyncio.wait_for(q.get(), timeout=2.0)
                t = ev.get("type", "")

                if t == "run_start":
                    logger.info(f"Run started: {ev['run_id']}")
                elif t == "config":
                    logger.info(f"Config: {ev['config']}")
                elif t == "stage_start":
                    logger.info(f"Stage started: {ev['stage']} for TC {ev.get('tc_id', '')}")
                elif t == "dimension_scored":
                    logger.info(f"    [Score] TC {ev['tc_id']} - {ev['dimension']}: {ev['score']:.3f}")
                elif t == "diagnosis":
                    logger.info(f"    [Diagnosis] Triggered for TC {ev['tc_id']} (score: {ev['overall']:.3f})")
                elif t == "tc_complete":
                    logger.info(f"    [TC Complete] {ev['tc_id']}  overall={ev['overall']:.3f}")
                elif t == "phase_progress":
                    pct = (ev.get("current", 0) / max(1, ev.get("total", 1))) * 100
                    logger.info(f"Progress: Phase {ev['phase']} - {pct:.1f}%")
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



def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

def run_server():
    import uvicorn
    logger.info("Starting EvalOS Framework Dashboard at http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

def main():
    parser = argparse.ArgumentParser(description="EvalOS Framework")
    parser.add_argument("--cli", action="store_true",
                        help="Run the pipeline in CLI mode (no web server)")
    parser.add_argument("--cases", type=int, default=None,
                        help="Override NUM_TEST_CASES for this run (e.g. --cases 5 for a quick test)")
    args = parser.parse_args()

    if args.cli:
        asyncio.run(run_pipeline(num_cases=args.cases))
    else:
        run_server()

if __name__ == "__main__":
    main()
