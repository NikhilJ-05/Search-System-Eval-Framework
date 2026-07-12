import asyncio
import json
import time
import logging
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from contextlib import asynccontextmanager
import os

from config import EvalConfig
from pipeline.orchestrator import Orchestrator, sse_queue_var
from pipeline.store import PipelineStore
from search_ir.qdrant_store import QdrantStore
from clients.embedder import EmbedderClient
from search_ir.retriever import Retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await qdrant.init_collection()
    await qdrant.init_query_cache_collection()
    await embedder.warmup()
    yield

app = FastAPI(title="Firecrawl Eval Dashboard", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

config = EvalConfig.from_env()
store = PipelineStore()

# Global instances for quick read
qdrant = QdrantStore(config)
embedder = EmbedderClient()
retriever = Retriever(qdrant, embedder)

# Store queues for active runs
active_queues = {}



@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/app.js")
async def serve_js():
    with open(os.path.join(STATIC_DIR, "app.js"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), media_type="application/javascript")
        
@app.get("/style.css")
async def serve_css():
    with open(os.path.join(STATIC_DIR, "style.css"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), media_type="text/css")

@app.get("/api/runs")
async def list_runs():
    return await asyncio.to_thread(store.list_runs_with_meta)

@app.get("/api/runs/{run_id}")
async def get_run(run_id: str):
    data = await asyncio.to_thread(store._get_full_run, run_id)
    if data is None:
        return JSONResponse(status_code=404, content={"detail": "Run not found"})
        
    meta = await asyncio.to_thread(store.get_run_status, run_id) or {}
    config = data.get("run_meta", {})
    
    dimensions = []
    results = data.get("eval_results", [])
    if results:
        for r in results:
            if "dimension_evals" in r and r["dimension_evals"]:
                dimensions = [{"name": d["dimension_name"], "weight": d.get("weight", 0), "description": ""} for d in r["dimension_evals"]]
                break
                
    data["metadata"] = {
        "status": meta.get("status", data.get("status")),
        "overall_score": meta.get("overall_score"),
        "config": config,
        "dimensions": dimensions,
        "duration": meta.get("duration_s")
    }
    return data

@app.get("/api/runs/{run_id}/status")
async def get_run_status(run_id: str):
    data = await asyncio.to_thread(store.get_run_status, run_id)
    if data is None:
        return JSONResponse(status_code=404, content={"detail": "Run meta not found"})
    return data

@app.get("/api/runs/{run_id}/dimensions")
async def get_run_dimensions(run_id: str):
    data = await asyncio.to_thread(store._get_full_run, run_id)
    if data is None:
        return JSONResponse(status_code=404, content={"detail": "Run not found"})
    
    # Extract dimensions from the first test case evaluation
    results = data.get("eval_results", [])
    if not results:
        return []
    
    # Find the first result with dimension_evals
    for r in results:
        if "dimension_evals" in r and r["dimension_evals"]:
            return [{"name": d["dimension_name"], "weight": d.get("weight", 0)} for d in r["dimension_evals"]]
            
    return []

@app.get("/api/runs/{run_id}/live")
async def get_run_live(run_id: str):
    data = await asyncio.to_thread(store._get_full_run, run_id)
    if data is None:
        return JSONResponse(status_code=404, content={"detail": "Run not found"})
    return data

@app.get("/api/runs/{run_id}/report")
async def get_report(run_id: str):
    """Serve the generated markdown report for a run."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path_new = os.path.join(base_dir, "outputs", "runs", run_id, "report.md")
    report_path_old = os.path.join(base_dir, "outputs", "reports", f"report_{run_id}.md")
    path = report_path_new if os.path.exists(report_path_new) else report_path_old
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"detail": "Report not found"})
    with open(path, "r", encoding="utf-8") as f:
        return {"markdown": f.read()}

@app.get("/api/runs/{run_id}/logs")
async def get_run_logs(run_id: str):
    """Serve the raw session.log for a specific run."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "outputs", "runs", run_id, "session.log")
    if not os.path.exists(path):
        return PlainTextResponse("No session log found for this run.", status_code=404)
    with open(path, "r", encoding="utf-8") as f:
        return PlainTextResponse(f.read())

@app.get("/api/runs/{run_id}/tc_report/{tc_id}")
async def get_tc_report(run_id: str, tc_id: str):
    """Serve the individual markdown report for a specific test case in a run."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "outputs", "runs", run_id, "tc_reports", f"{tc_id}.md")
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"detail": "Test case report not found"})
    with open(path, "r", encoding="utf-8") as f:
        return {"markdown": f.read()}

@app.get("/api/runs/{run_id}/test-cases")
async def get_run_test_cases(run_id: str):
    data = await asyncio.to_thread(store._get_full_run, run_id)
    if data is None:
        return JSONResponse(status_code=404, content={"detail": "Run not found"})
    return data.get("test_cases", [])

@app.post("/api/runs")
async def start_run(background_tasks: BackgroundTasks):
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    q = asyncio.Queue(maxsize=500)
    active_queues[run_id] = q
    
    async def _cleanup_queue_after_timeout():
        await asyncio.sleep(7200)
        active_queues.pop(run_id, None)
        
    asyncio.create_task(_cleanup_queue_after_timeout())
    
    async def run_pipeline_task():
        # ContextVar requires running within context
        token = sse_queue_var.set(q)
        try:
            orchestrator = Orchestrator(config)
            await asyncio.shield(orchestrator.run_pipeline(run_id))
        finally:
            sse_queue_var.reset(token)
            
    background_tasks.add_task(run_pipeline_task)
    return {"run_id": run_id}

@app.get("/api/runs/{run_id}/stream")
async def stream_run(request: Request, run_id: str):
    q = active_queues.get(run_id)
    if not q:
        return JSONResponse(status_code=404, content={"detail": "Run stream not found"})
        
    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(q.get(), timeout=1.0)
                    yield json.dumps(event)
                    if event.get("type") in ("run_complete", "run_error"):
                        if run_id in active_queues:
                            del active_queues[run_id]
                        break
                except asyncio.TimeoutError:
                    yield json.dumps({"type": "ping", "time": time.time()})
        finally:
            pass
                
    return EventSourceResponse(event_generator())

@app.get("/api/kb/search")
async def search_kb(q: str):
    results = await retriever.search(q, limit=10)
    return results

@app.get("/api/kb/stats")
async def get_kb_stats():
    qdrant_stats = await qdrant.get_collection_stats()
    points = qdrant_stats.get("points_count", 0)
    
    unique_urls = set()
    try:
        scroll_res, _ = await qdrant.client.scroll(
            collection_name=config.qdrant_collection,
            limit=10000,
            with_payload=["url"],
            with_vectors=False
        )
        for p in scroll_res:
            if p.payload and "url" in p.payload:
                unique_urls.add(p.payload["url"])
    except Exception:
        pass

    return {
        "points_count": points,
        "vectors_count": qdrant_stats.get("vectors_count", 0),
        "unique_urls": len(unique_urls),
        "deduped_count": 0,
        "status": qdrant_stats.get("status", "ok")
    }

@app.get("/api/kb/recent")
async def get_recent_kb():
    try:
        scroll_res, _ = await qdrant.client.scroll(
            collection_name=config.qdrant_collection,
            limit=2000,
            with_payload=True,
            with_vectors=False
        )
        docs = {}
        for p in scroll_res:
            if not p.payload: continue
            url = p.payload.get("url")
            if not url: continue
            if url not in docs:
                docs[url] = {
                    "url": url,
                    "chunks": [],
                    "timestamp": p.payload.get("scrape_timestamp", 0)
                }
            docs[url]["chunks"].append({
                "idx": p.payload.get("chunk_index", 0),
                "content": p.payload.get("content", "")
            })
            docs[url]["timestamp"] = max(docs[url]["timestamp"], p.payload.get("scrape_timestamp", 0))
            
        result = []
        for doc in docs.values():
            doc["chunks"].sort(key=lambda x: x["idx"])
            stitched = "\n".join([c["content"] for c in doc["chunks"]])
            result.append({
                "url": doc["url"],
                "content": stitched,
                "timestamp": doc["timestamp"]
            })
            
        result.sort(key=lambda x: x["timestamp"], reverse=True)
        return result[:20]
    except Exception as e:
        logger.error(f"Error fetching recent kb: {e}")
        return []

@app.get("/api/rl/signals/{run_id}")
async def get_rl_signals(run_id: str):
    def load_signals():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rl_dir = os.path.join(base_dir, "outputs", "runs", run_id, "rl_signals")
        old_dir = os.path.join(base_dir, "outputs", "rl_signals")
        
        dpo_pairs = []
        rewards = []
        taxonomy = []
        
        dpo_p = os.path.join(rl_dir, "dpo_pairs.jsonl")
        if not os.path.exists(dpo_p): dpo_p = os.path.join(old_dir, f"dpo_pairs_{run_id}.jsonl")
        if os.path.exists(dpo_p):
            with open(dpo_p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip(): dpo_pairs.append(json.loads(line))
                    
        rew_p = os.path.join(rl_dir, "rewards.jsonl")
        if not os.path.exists(rew_p): rew_p = os.path.join(old_dir, f"rewards_{run_id}.jsonl")
        if os.path.exists(rew_p):
            with open(rew_p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip(): rewards.append(json.loads(line))
                    
        tax_p = os.path.join(rl_dir, "taxonomy.json")
        if not os.path.exists(tax_p): tax_p = os.path.join(old_dir, f"taxonomy_{run_id}.json")
        if os.path.exists(tax_p):
            with open(tax_p, "r", encoding="utf-8") as f:
                taxonomy = json.load(f)
                
        # Load additional rich details from run.json if present
        tc_diagnoses = []
        improvement_analysis = {}
        run_file = os.path.join(base_dir, "outputs", "runs", run_id, "run.json")
        if os.path.exists(run_file):
            try:
                with open(run_file, "r", encoding="utf-8") as f:
                    run_data = json.load(f)
                    tc_diagnoses = run_data.get("tc_diagnoses", [])
                    improvement_analysis = run_data.get("improvement_analysis", {})
            except Exception as e:
                logger.error(f"Error loading run.json for RL signals: {e}")

        return {
            "dpo_pairs": dpo_pairs,
            "reward_signals": rewards,
            "taxonomy": taxonomy,
            "tc_diagnoses": tc_diagnoses,
            "improvement_analysis": improvement_analysis
        }
    
    return await asyncio.to_thread(load_signals)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
