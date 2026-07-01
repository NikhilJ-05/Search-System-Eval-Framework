import logging
import json
import math
import os
import asyncio
from typing import List
from models.eval_result import EvalResult, FirecrawlSearchResult
from models.rl_signal import DPOPair, DPOVariant, RewardSignal, RewardComponents, Trajectory, ImprovementPattern
from models.test_case import TestCase

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

class SignalGenerator:
    def __init__(self):
        self.patterns = []

    def generate_signals(self, eval_results: List[EvalResult], search_results_dict: dict, test_cases: List[TestCase] = None) -> tuple:
        logger.info("Generating RL signals from eval results...")
        dpo_pairs = []
        reward_signals = []
        patterns = []

        tc_map = {tc.id: tc for tc in test_cases} if test_cases else {}

        for eval_res in eval_results:
            tc_id = eval_res.test_case_id
            search_res = search_results_dict.get(tc_id, [])
            
            # Simple heuristic for DPO pair generation based on judge's ideal ranking
            ideal_rank = eval_res.ranking.llm_ideal_ranking
            fc_rank = eval_res.ranking.firecrawl_ranking
            
            # Map url to its ideal rank position
            url_to_ideal_rank = {}
            for ideal_pos_0indexed, tc_index_1indexed in enumerate(ideal_rank):
                if 1 <= tc_index_1indexed <= len(search_res):
                    url = search_res[tc_index_1indexed - 1].url
                    url_to_ideal_rank[url] = ideal_pos_0indexed + 1

            # Find a disagreement where ideal says X is better than Y, but FC said Y is better than X
            if len(ideal_rank) >= 2 and len(fc_rank) >= 2 and len(search_res) >= max(ideal_rank + fc_rank):
                try:
                    if ideal_rank[0] != fc_rank[0]:
                        chosen_idx = ideal_rank[0] - 1
                        rejected_idx = fc_rank[0] - 1
                        
                        chosen_res = search_res[chosen_idx]
                        rejected_res = search_res[rejected_idx]
                        
                        chosen_sq = eval_res.scrape_quality.get(chosen_res.url)
                        rejected_sq = eval_res.scrape_quality.get(rejected_res.url)
                        
                        chosen_sq_val = chosen_sq.overall_markdown_quality if chosen_sq else 1.0
                        rejected_sq_val = rejected_sq.overall_markdown_quality if rejected_sq else 0.7
                        
                        rejected_score = eval_res.overall_score * (rejected_sq_val / max(0.01, chosen_sq_val))
                        rejected_score = min(rejected_score, eval_res.overall_score * 0.9) # cap at 90% of chosen
                        
                        dpo_pairs.append(
                            DPOPair(
                                query=chosen_res.query,
                                chosen=DPOVariant(
                                    url=chosen_res.url,
                                    content_snippet=chosen_res.full_markdown[:500] if chosen_res.full_markdown else "",
                                    firecrawl_rank=fc_rank[0],
                                    judge_score=eval_res.overall_score
                                ),
                                rejected=DPOVariant(
                                    url=rejected_res.url,
                                    content_snippet=rejected_res.full_markdown[:500] if rejected_res.full_markdown else "",
                                    firecrawl_rank=rejected_res.firecrawl_rank,  # FIX: was incorrectly using chosen_res
                                    judge_score=rejected_score
                                ),
                                preference_rationale=eval_res.ranking.ranking_reasoning
                            )
                        )
                except Exception as e:
                    logger.warning(f"Failed to generate DPO for tc {tc_id}: {e}")

            # Reward signals
            for sr in search_res:
                sq = eval_res.scrape_quality.get(sr.url)
                if sq:
                    ideal_pos = url_to_ideal_rank.get(sr.url, sr.firecrawl_rank)

                    # Freshness: exponential decay from kb_meta age (10-min half-life).
                    # Falls back to 1.0 if no KB metadata (live scrape = maximally fresh).
                    kb_meta = getattr(sr, "kb_meta", None)
                    if kb_meta and kb_meta.get("age_s") is not None:
                        freshness = max(0.1, math.exp(-kb_meta["age_s"] / 600.0))
                    else:
                        freshness = 1.0

                    relevance = eval_res.coverage.recall_score
                    completeness = sq.completeness_score
                    markdown_quality = sq.overall_markdown_quality

                    # Weighted composite: relevance 35%, markdown quality 30%, completeness 20%, freshness 15%
                    composite = (
                        0.35 * relevance
                        + 0.30 * markdown_quality
                        + 0.20 * completeness
                        + 0.15 * freshness
                    )

                    reward_signals.append(
                        RewardSignal(
                            query=sr.query,
                            url=sr.url,
                            reward_components=RewardComponents(
                                relevance=relevance,
                                completeness=completeness,
                                freshness=freshness,
                                markdown_quality=markdown_quality
                            ),
                            composite_reward=round(composite, 4),
                            trajectory=Trajectory(
                                search_rank=sr.firecrawl_rank,
                                ideal_rank=ideal_pos,
                                rank_delta=ideal_pos - sr.firecrawl_rank
                            )
                        )
                    )

        # Dynamic patterns grouped by category + intent
        group_scores = {}
        for res in eval_results:
            tc = tc_map.get(res.test_case_id)
            if not tc: continue
            key = (tc.category, tc.intent)
            if key not in group_scores:
                group_scores[key] = []
            group_scores[key].append(res)
            
        for (category, intent), results in group_scores.items():
            avg_score = sum(r.overall_score for r in results) / len(results)
            # If the group has sub-par performance, generate a targeted pattern
            if avg_score < 0.8:
                # Find most common scrape issue in this group
                issue_freqs = {}
                for r in results:
                    for sq in r.scrape_quality.values():
                        for issue in sq.issues_found:
                            issue_freqs[issue.type] = issue_freqs.get(issue.type, 0) + 1
                most_common_issue = "markdown_fidelity"
                if issue_freqs:
                    most_common_issue = max(issue_freqs.items(), key=lambda x: x[1])[0]
                    
                patterns.append(
                    ImprovementPattern(
                        issue=f"{category}_{intent}_{most_common_issue}",
                        frequency=f"{len(results)} queries",
                        description=f"Performance bottleneck on intent '{intent}' in category '{category}' with common issue: '{most_common_issue}' (Avg score: {avg_score:.2f})",
                        suggested_fix=f"Add custom extraction selectors and metadata tags to mitigate '{most_common_issue}'"
                    )
                )
                
        # Default fallback pattern if no failing groups
        if not patterns:
            patterns.append(
                ImprovementPattern(
                    issue="general_stability",
                    frequency="All TCs passed",
                    description="Evaluation pipeline overall score is stable.",
                    suggested_fix="Maintain current selector configurations."
                )
            )

        self.patterns = patterns
        return dpo_pairs, reward_signals, patterns

    def update_patterns(self, enhanced_patterns: List[dict]):
        if enhanced_patterns:
            self.patterns = enhanced_patterns

    def save_signals(self, dpo_pairs: List[DPOPair], reward_signals: List[RewardSignal], patterns: List[ImprovementPattern], run_id: str):
        out_dir = os.path.join(APP_DIR, "outputs", "runs", run_id, "rl_signals")
        os.makedirs(out_dir, exist_ok=True)
        
        # Save DPO pairs
        import dataclasses
        dpo_path = os.path.join(out_dir, "dpo_pairs.jsonl")
        with open(dpo_path, 'w', encoding='utf-8') as f:
            for pair in dpo_pairs:
                f.write(json.dumps(dataclasses.asdict(pair)) + '\n')
                
        # Save rewards
        reward_path = os.path.join(out_dir, "rewards.jsonl")
        with open(reward_path, 'w', encoding='utf-8') as f:
            for rw in reward_signals:
                f.write(json.dumps(dataclasses.asdict(rw)) + '\n')
                
        # Save taxonomy
        tax_path = os.path.join(out_dir, "taxonomy.json")
        with open(tax_path, 'w', encoding='utf-8') as f:
            # Handle both dataclasses and dicts
            out_patterns = [dataclasses.asdict(p) if dataclasses.is_dataclass(p) else p for p in patterns]
            json.dump(out_patterns, f, indent=2)
            
        logger.info(f"Saved RL signals to {out_dir}")

    async def save_signals_async(self, *args, **kwargs):
        await asyncio.to_thread(self.save_signals, *args, **kwargs)
