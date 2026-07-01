import asyncio
import time
import logging
import os
import json
import dataclasses
from datetime import datetime
from typing import List, Dict, Tuple
from config import EvalConfig
from clients.openrouter import OpenRouterClientPool
from clients.firecrawl_client import FirecrawlClientPool
from clients.embedder import EmbedderClient
from search_ir.qdrant_store import QdrantStore
from eval.test_generator import TestGenerator
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

logger = logging.getLogger(__name__)
sse_queue_var: contextvars.ContextVar[asyncio.Queue] = contextvars.ContextVar('sse_queue', default=None)

class Orchestrator:
    def __init__(self, config: EvalConfig):
        self.config = config
        self.or_pool = OpenRouterClientPool(config)
        self.fc_pool = FirecrawlClientPool(config)
        self.embedder = EmbedderClient()
        self.qdrant = QdrantStore(config)
        
        self.generator = TestGenerator(config, self.or_pool)
        self.judge = Judge(config, self.or_pool)
        self.indexer = Indexer(self.qdrant, self.embedder)
        self.retriever = Retriever(self.qdrant, self.embedder)
        self.comparator = RankingComparator()
        self.signal_gen = SignalGenerator()
        self.report_builder = ReportBuilder()
        self.regression = RegressionDetector()
        self.calibration = JudgeCalibration()
        self.improvement_agent = ImprovementAgent(config, self.or_pool)

    def _emit_event(self, event_data: dict):
        q = sse_queue_var.get()
        if q is not None:
            try:
                q.put_nowait(event_data)
            except Exception as e:
                logger.error(f"Failed to emit SSE event: {e}")

    async def _save_live_run(self, run_id: str, test_cases: list, eval_results: list, tc_diagnoses: list):
        run_dir = os.path.join(APP_DIR, "outputs", "runs", run_id)
        os.makedirs(run_dir, exist_ok=True)
        run_file_path = os.path.join(run_dir, "run.json")
        import dataclasses
        run_payload = {
            "run_id": run_id,
            "test_cases": [dataclasses.asdict(tc) for tc in test_cases],
            "eval_results": [r.to_dict() for r in eval_results],
            "tc_diagnoses": [dataclasses.asdict(d) for d in tc_diagnoses],
            "status": "running"
        }
        def _write():
            with open(run_file_path, "w", encoding="utf-8") as f:
                json.dump(run_payload, f, indent=2)
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
            self._emit_event({"type": "tc_processing", "tc_id": tc.id})
            tc_new_entries = []

            # Layer 1: Query Cache
            cached_query, query_dense_vec = await self.retriever.find_similar_query(
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
                
                # Save to query cache
                await self.retriever.store_search_results(tc.query, fc_results, precomputed_dense_vec=query_dense_vec)
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
                    score_threshold=self.config.kb_content_score_threshold
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
                                    import hashlib
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
                f"cov={eval_res.coverage.recall_score:.3f} rnk={eval_res.ranking.ndcg_at_5:.3f}"
            )

            logger.info(f"[Pipeline] [{tc.id}] Running live diagnostic analysis...")
            diag = await self.improvement_agent.analyze_tc(tc, eval_res, fc_results)
            if hasattr(self, 'live_tc_diagnoses'):
                self.live_tc_diagnoses.append(diag)

            if hasattr(self, 'current_run_id') and self.current_run_id:
                await self.report_builder.build_single_tc_report_async(
                    self.current_run_id, tc, eval_res, fc_results, diag, self.config.pass_threshold
                )
                await self._save_live_run(self.current_run_id, getattr(self, 'live_test_cases', []), eval_results, getattr(self, 'live_tc_diagnoses', []))

            self._emit_event({
                "type": "judge_scored",
                "tc_id": tc.id,
                "coverage": eval_res.coverage.recall_score,
                "ranking": eval_res.ranking.ndcg_at_5,
                "scrape": sum(sq.overall_markdown_quality for sq in eval_res.scrape_quality.values()) / max(1, len(eval_res.scrape_quality)),
                "overall": eval_res.overall_score,
                "has_report": True
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

    async def run_pipeline(self, run_id: str = None) -> str:
        if not run_id:
            run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        logger.info(f"Starting pipeline run: {run_id}")
        self._emit_event({"type": "run_start", "run_id": run_id})
        
        try:
            # Init resources concurrently
            await asyncio.gather(
                self.qdrant.init_collection(),
                self.qdrant.init_query_cache_collection(),
                self.embedder.warmup()
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
            batch_size = self.config.batch_size

            max_concurrent = min(
                len(self.fc_pool._clients) if hasattr(self.fc_pool, '_clients') else 10,
                len(self.or_pool._clients) if hasattr(self.or_pool, '_clients') else 10,
                batch_size,
                self.config.max_concurrent_tcs
            )
            semaphore = asyncio.Semaphore(max_concurrent)

            r_num = 0
            while len(all_eval_results) < total_needed:
                r_num += 1
                remaining = total_needed - len(all_eval_results)
                this_batch = min(batch_size, remaining)

                # --- Generate TCs for this round using full accumulated history ---
                previous_queries = [tc.query for tc in all_test_cases]
                previous_urls = await self._fetch_previous_urls()

                logger.info(f"=== ROUND {r_num} — generating {this_batch} TC(s) "
                            f"(history: {len(previous_queries)} queries, {len(previous_urls)} KB URLs) ===")
                self._emit_event({"type": "phase_start", "phase": "test_generation",
                                  "message": f"Round {r_num}: Generating {this_batch} test case(s)..."})

                new_tcs = await self.generator.generate(this_batch, previous_queries, previous_urls)
                if not new_tcs:
                    logger.warning(f"[Orchestrator] Round {r_num}: Generator returned 0 TCs — stopping early.")
                    break

                all_test_cases.extend(new_tcs)
                self.live_test_cases = all_test_cases
                for tc in new_tcs:
                    self._emit_event({"type": "test_case_created", "tc_id": tc.id, "query": tc.query})
                # Persist so a restart can resume from where we left off
                await self._persist_test_cases_async(all_test_cases)

                # --- Execute this round ---
                self._emit_event({"type": "phase_start", "phase": "execution",
                                  "message": f"Round {r_num}: Executing {len(new_tcs)} test case(s)..."})
                tc_tasks = [
                    self._process_tc(tc, idx, len(new_tcs), r_num,
                                     all_search_results, all_eval_results, semaphore)
                    for idx, tc in enumerate(new_tcs)
                ]
                # gather() here waits for ALL processing (including indexing) to finish
                # before the next round generates new TCs — ensuring the KB is fully
                # up-to-date when history-based variants are created.
                results = await asyncio.gather(*tc_tasks)

                round_new_indexed = sum(s.new_indexed for s in results if s)
                round_deduped = sum(s.deduped for s in results if s)
                self._emit_event({"type": "round_complete", "round": r_num,
                                  "new_indexed": round_new_indexed, "deduped": round_deduped})
                round_stats.append({
                    "round": r_num,
                    "tcs_processed": len(new_tcs),
                    "new_indexed_docs": round_new_indexed,
                    "deduped_docs": round_deduped
                })
                logger.info(f"=== ROUND {r_num} complete — {len(all_eval_results)}/{total_needed} TCs done ===")

            # Phase 6: RL Signals (independent of indexing)
            self._emit_event({"type": "phase_start", "phase": "rl_signals"})
            dpo_pairs, reward_signals, patterns = self.signal_gen.generate_signals(all_eval_results, all_search_results, all_test_cases)
            self._emit_event({"type": "phase_complete", "phase": "rl_signals", "dpo_pairs": len(dpo_pairs)})

            # Level 1: Use per-TC diagnoses already computed live during execution
            self._emit_event({"type": "phase_start", "phase": "tc_diagnostics", "message": "Finalizing individual test case diagnoses..."})
            tc_diagnoses = getattr(self, 'live_tc_diagnoses', [])
            if len(tc_diagnoses) < len(all_eval_results):
                tc_diag_tasks = []
                tc_map = {tc.id: tc for tc in all_test_cases}
                for res in all_eval_results:
                    tc = tc_map[res.test_case_id]
                    if not any(d.tc_id == tc.id for d in tc_diagnoses):
                        tc_diag_tasks.append(self.improvement_agent.analyze_tc(tc, res, all_search_results.get(tc.id, [])))
                if tc_diag_tasks:
                    tc_diagnoses.extend(await asyncio.gather(*tc_diag_tasks))

            # Generate per-TC individual markdown reports in parallel (independent of indexing)
            tc_report_paths = await self.report_builder.build_tc_reports_async(
                run_id=run_id,
                test_cases=all_test_cases,
                eval_results=all_eval_results,
                search_results_dict=all_search_results,
                tc_diagnoses=tc_diagnoses,
                pass_threshold=self.config.pass_threshold
            )

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
            await self.signal_gen.save_signals_async(dpo_pairs, reward_signals, self.signal_gen.patterns, run_id)

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
            reg_data = self.regression.detect(run_id, all_eval_results)
            rl_summary = {
                "dpo_pairs": len(dpo_pairs),
                "reward_signals": len(reward_signals),
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
            run_dir = os.path.join(APP_DIR, "outputs", "runs", run_id)
            os.makedirs(run_dir, exist_ok=True)
            run_file_path = os.path.join(run_dir, "run.json")
            run_payload = {
                "run_id": run_id,
                "test_cases": [dataclasses.asdict(tc) for tc in all_test_cases],
                "eval_results": [r.to_dict() for r in all_eval_results],
                "tc_diagnoses": [dataclasses.asdict(d) for d in tc_diagnoses],
                "improvement_analysis": dataclasses.asdict(improvement_analysis),
                "regression": reg_data,
                "report_path": report_path,
                "tc_report_paths": tc_report_paths
            }
            def _write_run():
                with open(run_file_path, "w", encoding="utf-8") as f:
                    json.dump(run_payload, f, indent=2)
            await asyncio.to_thread(_write_run)
            
            overall_score = sum(e.overall_score for e in all_eval_results) / max(1, len(all_eval_results))
            self._emit_event({"type": "run_complete", "run_id": run_id, "overall_score": overall_score})
            logger.info(f"Pipeline complete. Report: {report_path}")
            
        except asyncio.CancelledError:
            logger.warning(f"Pipeline {run_id} cancelled by client. Shield should protect it, but handling gracefully.")
            self._emit_event({"type": "run_error", "error": "Cancelled by client"})
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self._emit_event({"type": "run_error", "error": str(e)})
        finally:
            await self.or_pool.aclose()
            
        return run_id
