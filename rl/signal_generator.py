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

    def generate_tc_signals(
        self,
        tc: TestCase,
        eval_result: EvalResult,
        search_results: List[FirecrawlSearchResult],
        diagnosis: Any
    ) -> tuple:
        logger.info(f"Generating RL signals for TC {tc.id}...")
        dpo_pairs = []
        reward_signals = []
        tc_pattern = None

        # Build url quality scores from LLM diagnosis
        url_quality = {}
        for ann in getattr(diagnosis, "url_quality_annotations", []):
            url_quality[ann.get("url")] = ann.get("quality_score", 0.5)

        sorted_by_quality = sorted(
            search_results,
            key=lambda r: url_quality.get(r.url, 0.5),
            reverse=True
        )

        url_to_ideal_rank = {r.url: i + 1 for i, r in enumerate(sorted_by_quality)}

        # DPO Pair
        if len(sorted_by_quality) >= 2 and len(search_results) >= 2:
            try:
                best_res = sorted_by_quality[0]
                fc_top_res = search_results[0]
                if best_res.url != fc_top_res.url:
                    dpo_pairs.append(
                        DPOPair(
                            query=tc.query,
                            test_case_id=tc.id,
                            chosen=DPOVariant(
                                url=best_res.url,
                                content_snippet=best_res.full_markdown[:500] if best_res.full_markdown else "",
                                firecrawl_rank=best_res.firecrawl_rank,
                                judge_score=eval_result.overall_score
                            ),
                            rejected=DPOVariant(
                                url=fc_top_res.url,
                                content_snippet=fc_top_res.full_markdown[:500] if fc_top_res.full_markdown else "",
                                firecrawl_rank=fc_top_res.firecrawl_rank,
                                judge_score=eval_result.overall_score * 0.8
                            ),
                            preference_rationale=getattr(diagnosis, "dpo_rationale", "Derived from LLM quality annotations"),
                            dimension_context="overall"
                        )
                    )
            except Exception as e:
                logger.warning(f"Failed to generate DPO for tc {tc.id}: {e}")

        # Reward Signals
        for sr in search_results:
            ideal_pos = url_to_ideal_rank.get(sr.url, sr.firecrawl_rank)
            kb_meta = getattr(sr, "kb_meta", None)
            if kb_meta and kb_meta.get("age_s") is not None:
                freshness = max(0.1, math.exp(-kb_meta["age_s"] / 600.0))
            else:
                freshness = 1.0

            relevance = eval_result.overall_score
            llm_quality = url_quality.get(sr.url, 0.5)
            
            # Content completeness
            completeness = 0.5
            authority = 0.0
            if getattr(eval_result, "document_profiles", None):
                for p in eval_result.document_profiles:
                    if p.get("url") == sr.url:
                        comp_str = p.get("content", {}).get("content_completeness", "unknown")
                        if comp_str == "complete": completeness = 1.0
                        elif comp_str == "partial": completeness = 0.7
                        elif comp_str == "appears_truncated": completeness = 0.4
                        elif comp_str == "navigation_only": completeness = 0.1
                        elif comp_str == "error_page": completeness = 0.0
                        
                        dom_type = p.get("structure", {}).get("domain_type", p.get("domain_type", "unknown"))
                        auth_sigs = p.get("content", {}).get("authority_signals", [])
                        if dom_type in ["authoritative", "academic"]:
                            authority = 1.0
                        elif auth_sigs:
                            authority = 0.5

            composite = (
                0.30 * relevance
                + 0.25 * llm_quality
                + 0.20 * completeness
                + 0.15 * freshness
                + 0.10 * authority
            )

            diag_note = ""
            for ann in getattr(diagnosis, "url_quality_annotations", []):
                if ann.get("url") == sr.url:
                    diag_note = ann.get("quality_note", "")

            reward_signals.append(
                RewardSignal(
                    query=tc.query,
                    test_case_id=tc.id,
                    url=sr.url,
                    reward_components=RewardComponents(
                        relevance=relevance,
                        completeness=completeness,
                        freshness=freshness,
                        markdown_quality=llm_quality,
                        authority=authority
                    ),
                    composite_reward=round(composite, 4),
                    trajectory=Trajectory(
                        search_rank=sr.firecrawl_rank,
                        ideal_rank=ideal_pos,
                        rank_delta=ideal_pos - sr.firecrawl_rank
                    ),
                    diagnostic_notes=diag_note
                )
            )

        # Micro Pattern
        if getattr(diagnosis, "micro_pattern", None):
            mp = diagnosis.micro_pattern
            if isinstance(mp, dict):
                from models.rl_signal import TCMicroPattern
                tc_pattern = TCMicroPattern(
                    test_case_id=tc.id,
                    pattern_type=mp.get("pattern_type", "unknown"),
                    affected_dimension=mp.get("affected_dimension", "unknown"),
                    severity=mp.get("severity", "medium"),
                    description=mp.get("description", ""),
                    suggested_fix=mp.get("suggested_fix", "")
                )

        return dpo_pairs, reward_signals, tc_pattern

    def aggregate_patterns(
        self,
        micro_patterns: List[Any],
        eval_results: List[EvalResult],
        test_cases: List[TestCase]
    ) -> List[ImprovementPattern]:
        logger.info("Aggregating RL micro-patterns...")
        patterns = []
        
        grouping = {}
        for mp in micro_patterns:
            ptype = getattr(mp, "pattern_type", "unknown")
            if ptype not in grouping:
                grouping[ptype] = []
            grouping[ptype].append(mp)
            
        for ptype, mps in grouping.items():
            affected_tcs = [getattr(mp, "test_case_id") for mp in mps]
            
            # Severity resolution (take highest severity)
            sev_levels = {"critical": 4, "high": 3, "medium": 2, "low": 1, "observation": 0}
            max_sev = max(mps, key=lambda x: sev_levels.get(getattr(x, "severity", "medium"), 2))
            severity = getattr(max_sev, "severity", "medium")
            
            patterns.append(
                ImprovementPattern(
                    issue=ptype,
                    frequency=f"{len(mps)} TCs",
                    description=getattr(mps[0], "description", ""),
                    suggested_fix=getattr(mps[0], "suggested_fix", ""),
                    severity=severity,
                    affected_tcs=affected_tcs
                )
            )
            
        self.patterns = sorted(patterns, key=lambda p: len(p.affected_tcs), reverse=True)
        return self.patterns

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
