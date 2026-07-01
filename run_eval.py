import asyncio
import logging
import argparse
from config import EvalConfig
from pipeline.orchestrator import Orchestrator, sse_queue_var

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    parser = argparse.ArgumentParser(description="Run Firecrawl Eval Pipeline")
    parser.add_argument("--calibrate-only", action="store_true", help="Run only judge calibration")
    args = parser.parse_args()

    config = EvalConfig.from_env()
    
    if args.calibrate_only:
        from eval.calibration import JudgeCalibration
        from eval.judge import Judge
        from clients.openrouter import OpenRouterClientPool
        
        or_pool = OpenRouterClientPool(config)
        judge = Judge(config, or_pool)
        calib = JudgeCalibration()
        await calib.run_calibration(judge)
        await or_pool.aclose()
        return

    q = asyncio.Queue()
    
    async def drain_queue():
        while True:
            try:
                event = await asyncio.wait_for(q.get(), timeout=1.0)
                if event.get("type") in ("run_complete", "run_error"):
                    break
            except asyncio.TimeoutError:
                pass
            except Exception:
                break
                
    drain_task = asyncio.create_task(drain_queue())
    
    token = sse_queue_var.set(q)
    try:
        orch = Orchestrator(config)
        await orch.run_pipeline()
    finally:
        sse_queue_var.reset(token)
        await drain_task

if __name__ == "__main__":
    asyncio.run(main())
