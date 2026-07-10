import asyncio
import time
import logging
import os
import json
import hashlib
import dataclasses
from datetime import datetime
from typing import List, Dict, Tuple
from config import EvalConfig
from clients.openrouter import OpenRouterClientPool
from clients.firecrawl_client import FirecrawlClientPool
from clients.embedder import EmbedderClient
from search_ir.qdrant_store import QdrantStore
from eval.test_generator import TestGenerator
from eval.test_case_history import TestCaseHistory
from eval.judge import Judge
from search_ir.indexer import Indexer, IndexStats
from search_ir.retriever import Retriever
from eval.comparator import RankingComparator
from rl.signal_generator import SignalGenerator
from reports.report_builder import ReportBuilder
from reports.regression import RegressionDetector
from eval.calibration import JudgeCalibration
from eval.improvement_agent import ImprovementAgent
from models.test_case import TestCase
from models.eval_result import FirecrawlSearchResult
import contextvars
from pipeline.store import PipelineStore, RunMetadata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

logger = logging.getLogger(__name__)
sse_queue_var: contextvars.ContextVar[asyncio.Queue] = contextvars.ContextVar('sse_queue', default=None)

class Orchestrator:
    def __init__(self, config: EvalConfig):
        self.config = config
        self.store = PipelineStore()
        self.or_pool = OpenRouterClientPool(config)
        self.fc_pool = FirecrawlClientPool(config)
        self.embedder = EmbedderClient()
        self.qdrant = QdrantStore(config)
        
        self.generator = TestGenerator(config, self.or_pool)
        self.history = TestCaseHistory()
        self.judge = Judge(config, self.or_pool)
        self.indexer = Indexer(self.qdrant, self.embedder)
        self.retriever = Retriever(self.qdrant, self.embedder)
        
        self.comparator = RankingComparator(config, self.or_pool)
        self.signal_gen = SignalGenerator(config)
        self.report_builder = ReportBuilder(config)
        self.regression_detector = RegressionDetector()
        self.improvement_agent = ImprovementAgent(config, self.or_pool)
        self._background_tasks = []
        self.calibration = JudgeCalibration()
        
        self.live_tc_diagnoses = []
        self.live_dpo_pairs = []
        self.live_reward_signals = []
        self.live_micro_patterns = []
        self.live_eval_results = []
        self.live_test_cases = []

    def _emit_event(self, event_data: dict):
        q = sse_queue_var.get()
        if q is not None:
            try:
                q.put_nowait(event_data)
            except Exception as e:
                logger.error(f"Failed to emit SSE event: {e}")

    async def _save_live_run(self, run_id: str, test_cases: list, eval_results: list, tc_diagnoses: list):
        import dataclasses
        run_payload = {
            "run_id": run_id,
            "test_cases": [dataclasses.asdict(tc) for tc in test_cases],
            "eval_results": [r.to_dict() for r in eval_results],
            "tc_diagnoses": [dataclasses.asdict(d) for d in tc_diagnoses],
            "status": "running"
        }
        
        def _write():
            self.store.write_run_atomic(run_id, run_payload)
            
        await asyncio.to_thread(_write)

    def _load_existing_test_cases(self) -> List[TestCase]:
        """Load any previously persisted test cases (for resume support only — not for bulk generation)."""
        data_dir = os.path.join(APP_DIR, "outputs", "data")
        tc_file = os.path.join(data_dir, "test_cases.json")
        if os.path.exists(tc_file):
            try:
                with open(tc_file, "r", encoding="utf-8") as f:
                    raw_list = json.load(f)
                    tcs = [TestCase.from_dict(d) for d in raw_list]
                logger.info(f"[Orchestrator] Loaded {len(tcs)} existing test cases for history.")
                return tcs
            except Exception as e:
                logger.warning(f"[Orchestrator] Could not load existing test cases: {e}")
        return []

    async def _persist_test_cases_async(self, test_cases: List[TestCase]) -> None:
        """Persist the accumulated test case list so a crashed run can be resumed."""
        data_dir = os.path.join(APP_DIR, "outputs", "data")
        os.makedirs(data_dir, exist_ok=True)
        tc_file = os.path.join(data_dir, "test_cases.json")
        def _write():
            with open(tc_file, "w", encoding="utf-8") as f:
                json.dump([dataclasses.asdict(tc) for tc in test_cases], f, indent=2)
        try:
            await asyncio.to_thread(_write)
        except Exception as e:
            logger.warning(f"[Orchestrator] Failed to save test cases: {e}")

    async def _fetch_previous_urls(self) -> List[str]:
        """Fetch URLs already indexed in the KB so the generator can avoid them."""
        try:
            scroll_res, _ = await self.qdrant.client.scroll(
                collection_name=self.qdrant.config.qdrant_collection,
                limit=100,
                with_payload=True
            )
            return list({p.payload.get("url") for p in scroll_res if p.payload and p.payload.get("url")})
        except Exception as e:
            logger.debug(f"[Orchestrator] Could not fetch previous URLs from KB: {e}")
            return []

    async def _process_tc(
        self,
        tc: TestCase,
        tc_idx: int,
        total_in_batch: int,
        round_idx: int,
        search_results_dict: dict,
        eval_results: list,
        semaphore: asyncio.Semaphore
    ) -> Optional[IndexStats]:
        """Process a single test case with caching."""
        async with semaphore:
            logger.info(f"[Pipeline R{round_idx}] ─── TC {tc_idx+1}/{total_in_batch}: {tc.id} | query={repr(tc.query[:60])}")
            self._emit_event({
                "type": "tc_processing", 
                "tc_id": tc.id,
                "query": tc.query,
                "intent": getattr(tc, "intent", "unknown"),
                "difficulty": getattr(tc, "difficulty", "unknown"),
                "chaos_archetype": getattr(tc, "chaos_archetype", "none")
            })
            tc_new_entries = []

            # Layer 1: Query Cache
            cached_query, query_dense_vec, query_sparse_vec = await self.retriever.find_similar_query(
                tc.query, 
                threshold=self.config.query_cache_similarity_threshold,
                max_age_seconds=self.config.kb_freshness_window_seconds * 10
            )
            
            if cached_query:
                logger.info(f"[Pipeline] [{tc.id}] QUERY CACHE HIT (sim={cached_query['similarity']:.2f})")
                fc_results = cached_query["results"]
                for r in fc_results:
                    r.query_cache_status = "hit"
                    r.cache_similarity = cached_query["similarity"]
                self._emit_event({"type": "query_cache_hit", "tc_id": tc.id, "similarity": cached_query["similarity"]})
            else:
                logger.info(f"[Pipeline] [{tc.id}] SEARCH (Query Cache Miss)")
                fc_results, search_lat = await self.fc_pool.search(tc.query, limit=self.config.search_results_per_query)
                for r in fc_results:
                    r.query_cache_status = "miss"
                
                # Save to query cache in background
                asyncio.create_task(self.retriever.store_search_results(tc.query, fc_results, precomputed_dense_vec=query_dense_vec))
                self._emit_event({"type": "firecrawl_search_done", "tc_id": tc.id, "result_count": len(fc_results), "latency_ms": search_lat})

            # Layer 2: KB Hybrid Content Search (BM25 + Vector semantic per URL)
            # For each URL Firecrawl returned, check the KB using the actual query — not just
            # "does this URL exist?" but "does the KB have query-relevant content for this URL?"
            top_results = fc_results[:self.config.scrape_top_n]
            if top_results:
                top_urls = [r.url for r in top_results]
                logger.info(
                    f"[Pipeline] [{tc.id}] KB HYBRID SEARCH for {len(top_urls)} URLs "
                    f"(threshold={self.config.kb_content_score_threshold})"
                )

                # Single async batch: runs dense+sparse RRF per URL concurrently
                kb_coverage = await self.retriever.get_kb_coverage_for_urls(
                    query=tc.query,
                    urls=top_urls,
                    score_threshold=self.config.kb_content_score_threshold,
                    precomputed_dense_vec=query_dense_vec,
                    precomputed_sparse_vec=query_sparse_vec
                )

                scrape_tasks = []
                for res in top_results:
                    kb_entry = kb_coverage.get(res.url)

                    if kb_entry:
                        # Freshness check
                        age = time.time() - kb_entry.get("scrape_timestamp", 0)
                        if age < self.config.kb_freshness_window_seconds:
                            logger.info(
                                f"[Pipeline] [{tc.id}] KB SEMANTIC HIT  {res.url} "
                                f"(score={kb_entry['score']:.3f}, {kb_entry['num_chunks']} chunks, age={age:.0f}s)"
                            )
                            res.full_markdown = kb_entry["content"]
                            res.scrape_cache_status = "kb_semantic_hit"
                            res.kb_meta = {
                                "age_s": age,
                                "content_hash": kb_entry["content_hash"],
                                "kb_score": kb_entry["score"],
                                "num_chunks": kb_entry["num_chunks"]
                            }
                            self._emit_event({
                                "type": "firecrawl_scrape_done",
                                "tc_id": tc.id, "url": res.url,
                                "status": f"kb_semantic_hit(score={kb_entry['score']:.2f})"
                            })
                            continue
                        else:
                            logger.info(
                                f"[Pipeline] [{tc.id}] KB SEMANTIC STALE {res.url} "
                                f"(age={age:.0f}s). Re-scraping."
                            )
                            res.scrape_cache_status = "stale"
                            res.kb_meta = {"old_hash": kb_entry["content_hash"]}
                    else:
                        logger.info(f"[Pipeline] [{tc.id}] KB SEMANTIC MISS {res.url}. Will scrape.")
                        res.scrape_cache_status = "miss"

                    scrape_tasks.append((res, self.fc_pool.scrape(res.url)))

                if scrape_tasks:
                    results_to_update, tasks = zip(*scrape_tasks)
                    outputs = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for res, output in zip(results_to_update, outputs):
                        if isinstance(output, Exception):
                            logger.error(f"[Pipeline] [{tc.id}] Scrape error {res.url}: {output}")
                            res.full_markdown = None
                            res.status = f"error: {output}"
                        else:
                            md, scrape_lat, status = output
                            res.full_markdown = md
                            res.scrape_latency_ms = scrape_lat
                            res.status = status
                            logger.info(f"[Pipeline] [{tc.id}] Scraped {res.url}: {status}, {len(md) if md else 0} chars")
                            
                            if md:
                                tc_new_entries.append((res.url, md, tc.query))
                                
                                if res.scrape_cache_status == "stale":
                                    new_hash = hashlib.sha256(md.encode()).hexdigest()
                                    res.content_drift = {
                                        "changed": new_hash != res.kb_meta["old_hash"],
                                        "old_hash": res.kb_meta["old_hash"],
                                        "new_hash": new_hash
                                    }
                                    
                        self._emit_event({"type": "firecrawl_scrape_done", "tc_id": tc.id, "url": res.url, "status": res.status})

            # Fire indexing immediately — runs in background while LLM calls proceed
            indexing_task = None
            if tc_new_entries:
                logger.info(f"[Pipeline] [{tc.id}] Launching background indexing for {len(tc_new_entries)} doc(s)...")
                indexing_task = asyncio.create_task(
                    self.indexer.index_batch_deduped(tc_new_entries)
                )

            search_results_dict[tc.id] = fc_results

            # Judge
            logger.info(f"[Pipeline] [{tc.id}] JUDGE...")
            eval_res = await self.judge.evaluate(tc, fc_results)
            eval_results.append(eval_res)
            logger.info(
                f"[Pipeline] [{tc.id}] Judge: overall={eval_res.overall_score:.3f} "
                f"cov={eval_res.coverage_score:.3f} rnk={eval_res.ranking_score:.3f} "
                f"dims={len(eval_res.dimension_evals)}"
            )

            # Kick off live diagnostic analysis and reporting in the background
            task = asyncio.create_task(self._post_judge_pipeline(tc, eval_res, fc_results, self.current_run_id))
            self._background_tasks.append(task)

            # Persist successfully processed test case to the test case history store
            self.history.append(tc)

            self._emit_event({
                "type": "judge_scored",
                "tc_id": tc.id,
                "overall": eval_res.overall_score,
                "dimension_scores": [
                    {
                        "name": d.dimension_name,
                        "weight": d.weight,
                        "score": d.score,
                        "level": d.assigned_level
                    } for d in eval_res.dimension_evals
                ],
                "warnings": eval_res.warnings,
                "has_report": False
            })

            if indexing_task is not None:
                index_stats = await indexing_task
                logger.info(
                    f"[Pipeline] [{tc.id}] Indexing complete: "
                    f"{index_stats.new_indexed} new, {index_stats.deduped} deduped"
                )
                self._emit_event({
                    "type": "indexed",
                    "tc_id": tc.id,
                    "chunks": index_stats.total_chunks,
                    "deduped": index_stats.deduped
                })
                return index_stats
            return None

    async def _post_judge_pipeline(self, tc: TestCase, eval_res: EvalResult, search_results: List[FirecrawlSearchResult], run_id: str):
        """Background chain: diagnosis → RL signals → report."""
        try:
            # Step 1: LLM diagnosis
            diagnosis = await self.improvement_agent.analyze_tc(tc, eval_res, search_results)
            self.live_tc_diagnoses.append(diagnosis)
            
            # Step 2: Programmatic RL signals
            tc_dpo, tc_rewards, tc_pattern = self.signal_gen.generate_tc_signals(
                tc, eval_res, search_results, diagnosis
            )
            if tc_dpo:
                self.live_dpo_pairs.extend(tc_dpo)
            if tc_rewards:
                self.live_reward_signals.extend(tc_rewards)
            if tc_pattern:
                self.live_micro_patterns.append(tc_pattern)
            
            # Step 3: Per-TC report
            await self.report_builder.build_single_tc_report_async(
                run_id, tc, eval_res, search_results, diagnosis, self.config.pass_threshold
            )
            
            # Step 4: Emit SSE + save live state
            self._emit_event({
                "type": "tc_diagnosis_complete", 
                "tc_id": tc.id,
                "passed": getattr(diagnosis, 'passed', False),
                "root_cause_summary": getattr(diagnosis, 'root_cause_summary', ''),
                "failure_dimensions": getattr(diagnosis, 'failure_dimensions', []),
                "micro_pattern": diagnosis.micro_pattern.get("pattern_type") if diagnosis.micro_pattern else None,
                "improvement_actions_count": len(diagnosis.improvement_actions) if hasattr(diagnosis, 'improvement_actions') else 0
            })
            self._emit_event({"type": "tc_report_ready", "tc_id": tc.id})
            
            # Update live lists before saving
            self.live_eval_results = [r for r in self.live_eval_results if r.test_case_id != eval_res.test_case_id] + [eval_res]
            await self._save_live_run(run_id, self.live_test_cases, self.live_eval_results, self.live_tc_diagnoses)
            
        except Exception as e:
            logger.error(f"Post-judge pipeline failed for TC {tc.id}: {e}")

    async def run_pipeline(self, run_id: str = None) -> str:
        if not run_id:
            run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        logger.info(f"Starting pipeline run: {run_id}")
        start_time = time.time()
        
        # Write initial metadata
        initial_meta = RunMetadata(
            run_id=run_id,
            status="running",
            started_at=datetime.now().isoformat(),
            tc_count=self.config.num_test_cases
        )
        self.store.write_run_metadata(run_id, initial_meta)
        
        self._emit_event({
            "type": "run_start", 
            "run_id": run_id,
            "config_snapshot": {
                "num_tcs": self.config.num_test_cases,
                "generator_model": self.config.generator_model,
                "judge_model": self.config.judge_model,
                "pass_threshold": self.config.pass_threshold
            }
        })
        
        try:
            # Init resources concurrently
            await asyncio.gather(
                self.qdrant.init_collection(),
                self.qdrant.init_query_cache_collection(),
                self.embedder.warmup()
            )
            
            # Evict stale query cache entries
            await self.retriever.evict_stale_query_cache(
                max_age_seconds=self.config.query_cache_eviction_max_age_seconds
            )

            # Phase 3.5: Calibration (pre-flight) skipped by request
            logger.info("Skipping judge calibration pre-flight check.")

            # Rolling generation: TCs are generated round-by-round so each round
            # can use the query history + freshly indexed KB from all prior rounds.
            # Load any existing TCs from disk for resume support (already-processed history).
            all_test_cases: List[TestCase] = self._load_existing_test_cases()
            self.current_run_id = run_id
            self.live_test_cases = all_test_cases
            self.live_tc_diagnoses = []
            await self._save_live_run(run_id, all_test_cases, [], [])

            all_eval_results = []
            all_search_results = {}
            round_stats = []

            total_needed = self.config.num_test_cases
            semaphore = asyncio.Semaphore(1)

            for i in range(total_needed):
                # --- Generate TC ---
                logger.info(f"=== Session Progress — generating TC {i+1}/{total_needed} ===")
                self._emit_event({"type": "phase_start", "phase": "test_generation",
                                  "message": f"Generating TC {i+1}/{total_needed}...",
                                  "current": i+1, "total": total_needed, "pct": int(((i+1)/total_needed)*100)})
                self._emit_event({"type": "phase_progress", "phase": "test_generation", "current": i+1, "total": total_needed})

                new_tcs = await self.generator.generate(1)
                if not new_tcs:
                    logger.warning(f"[Orchestrator] Generator returned 0 TCs — stopping early.")
                    break
                tc = new_tcs[0]

                all_test_cases.append(tc)
                self.live_test_cases = all_test_cases
                self._emit_event({"type": "test_case_created", "tc_id": tc.id, "query": tc.query})
                
                # Persist so a restart can resume from where we left off
                await self._persist_test_cases_async(all_test_cases)

                # --- Execute this TC ---
                self._emit_event({"type": "phase_start", "phase": "execution",
                                  "message": f"Executing TC {i+1}/{total_needed}...",
                                  "current": i+1, "total": total_needed})
                self._emit_event({"type": "phase_progress", "phase": "execution", "current": i+1, "total": total_needed})
                
                result = await self._process_tc(tc, i, total_needed, i+1,
                                     all_search_results, all_eval_results, semaphore)
                
                new_indexed = result.new_indexed if result else 0
                deduped = result.deduped if result else 0
                
                self._emit_event({"type": "round_complete", "round": i+1,
                                  "new_indexed": new_indexed, "deduped": deduped})
                round_stats.append({
                    "round": i+1,
                    "tcs_processed": 1,
                    "new_indexed_docs": new_indexed,
                    "deduped_docs": deduped
                })
                logger.info(f"=== Session Progress — {len(all_eval_results)}/{total_needed} TCs complete ===")

            # Wait for all background diagnostics/reports to finish before proceeding to RL Signals
            if self._background_tasks:
                logger.info(f"[Pipeline] Waiting for {len(self._background_tasks)} background diagnostic tasks to complete...")
                await asyncio.gather(*self._background_tasks, return_exceptions=True)
                self._background_tasks.clear()

            # Phase 6: Aggregate per-TC micro-patterns into run-level taxonomy
            self._emit_event({"type": "phase_start", "phase": "rl_signals"})
            patterns = self.signal_gen.aggregate_patterns(
                self.live_micro_patterns, all_eval_results, all_test_cases
            )
            self._emit_event({"type": "phase_complete", "phase": "rl_signals", "dpo_pairs": len(self.live_dpo_pairs)})

            # tc_diagnoses is now completely populated from background tasks
            tc_diagnoses = self.live_tc_diagnoses
            tc_report_paths = [
                os.path.join(APP_DIR, "outputs", "runs", run_id, "reports", "tc_reports", f"{tc.id}.md")
                for tc in all_test_cases
            ]

            # Phase 6.5: Improvement Analysis (Level 2 Synthesis)
            self._emit_event({"type": "phase_start", "phase": "improvement_analysis"})
            cache_analytics = {}
            retrieval_comparison = {"kb_rankings": {}}
            improvement_analysis = await self.improvement_agent.analyze(
                all_test_cases, all_eval_results, all_search_results,
                cache_analytics, retrieval_comparison, tc_diagnoses
            )
            
            # Feed enhanced patterns back into RL signals
            self.signal_gen.update_patterns(improvement_analysis.enhanced_patterns)
            await self.signal_gen.save_signals_async(self.live_dpo_pairs, self.live_reward_signals, self.signal_gen.patterns, run_id)

            # Final round indexing is already complete since we gather and await all _process_tc tasks per round
            pass

            # Phase 5: Kick off Full Retrieval Comparison asynchronously against newly indexed KB
            self._emit_event({"type": "phase_start", "phase": "retrieval_comparison"})
            kb_results = await asyncio.gather(*[self.retriever.search(tc.query, limit=5) for tc in all_test_cases], return_exceptions=True)
            kb_rankings = {}
            for tc, kbres in zip(all_test_cases, kb_results):
                if isinstance(kbres, Exception):
                    kb_rankings[tc.id] = []
                else:
                    kb_rankings[tc.id] = [r["url"] for r in kbres]

            # Phase 7: Report & Regression
            self._emit_event({"type": "phase_start", "phase": "report"})
            reg_data = self.regression_detector.detect(run_id, all_eval_results)
            rl_summary = {
                "dpo_pairs": len(self.live_dpo_pairs),
                "reward_signals": len(self.live_reward_signals),
                "patterns": self.signal_gen.patterns
            }
            
            # Pass everything to report builder (using async thread wrapper)
            report_path = await self.report_builder.build_markdown_async(
                run_id=run_id, 
                test_cases=all_test_cases, 
                eval_results=all_eval_results, 
                search_results_dict=all_search_results, 
                rl_summary=rl_summary, 
                reg_data=reg_data,
                round_stats=round_stats,
                kb_rankings=kb_rankings,
                comparator=self.comparator,
                improvement_analysis=improvement_analysis,
                tc_diagnoses=tc_diagnoses
            )
            
            # Persist results asynchronously in dedicated run folder
            run_payload = {
                "run_id": run_id,
                "test_cases": [dataclasses.asdict(tc) for tc in all_test_cases],
                "eval_results": [r.to_dict() for r in all_eval_results],
                "tc_diagnoses": [dataclasses.asdict(d) for d in tc_diagnoses],
                "improvement_analysis": dataclasses.asdict(improvement_analysis),
                "regression": reg_data,
                "report_path": report_path,
                "tc_report_paths": tc_report_paths,
                "status": "completed"
            }
            
            duration_s = time.time() - start_time
            overall_score = sum(e.overall_score for e in all_eval_results) / max(1, len(all_eval_results))
            
            final_meta = RunMetadata(
                run_id=run_id,
                status="completed",
                overall_score=overall_score,
                tc_count=len(all_test_cases),
                started_at=initial_meta.started_at,
                finished_at=datetime.now().isoformat(),
                duration_s=duration_s
            )
            
            def _write_run():
                self.store.write_run_atomic(run_id, run_payload)
                self.store.write_run_metadata(run_id, final_meta)
                
            await asyncio.to_thread(_write_run)
            
            self._emit_event({
                "type": "run_complete", 
                "run_id": run_id, 
                "overall_score": overall_score,
                "pass_rate": sum(1 for e in all_eval_results if e.passes(self.config.pass_threshold)) / max(1, len(all_eval_results)),
                "total_tcs": len(all_test_cases),
                "duration_s": duration_s,
                "report_path": report_path
            })
            logger.info(f"Pipeline complete. Report: {report_path}")
            
        except asyncio.CancelledError:
            logger.warning(f"Pipeline {run_id} cancelled by client. Shield should protect it, but handling gracefully.")
            
            error_meta = RunMetadata(run_id=run_id, status="cancelled", started_at=getattr(initial_meta, "started_at", None))
            self.store.write_run_metadata(run_id, error_meta)
            self._emit_event({"type": "run_error", "error": "Cancelled by client"})
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            
            error_meta = RunMetadata(run_id=run_id, status="error", started_at=getattr(initial_meta, "started_at", None))
            self.store.write_run_metadata(run_id, error_meta)
            self._emit_event({"type": "run_error", "error": str(e)})
        finally:
            await self.or_pool.aclose()
            
        return run_id
