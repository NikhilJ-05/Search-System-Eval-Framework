import logging
import json
import math
import os
import asyncio
from typing import List, Any, Optional, Dict
from models.eval_result import EvalResult, FirecrawlSearchResult
from models.rl_signal import (
    DPOPair, DPOVariant, RewardSignal, RewardComponents, Trajectory, ImprovementPattern,
    ListwiseRankingExample, ContrastiveFailPair, QueryReformulationPair, SFTGoldExample, ScrapeQualityLabel,
    TCMicroPattern
)
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
                        comp_str = p.get("content_completeness", "unknown")
                        if comp_str == "complete": completeness = 1.0
                        elif comp_str == "partial": completeness = 0.7
                        elif comp_str == "appears_truncated": completeness = 0.4
                        elif comp_str == "navigation_only": completeness = 0.1
                        elif comp_str == "error_page": completeness = 0.0
                        
                        dom_type = p.get("domain_type", "unknown")
                        authority = p.get("authority_score", 0.0)
                        if authority == 0.0:  # fallback if old profile or unpopulated
                            auth_str = p.get("authority_assessment", "")
                            if dom_type in ["authoritative", "academic"]:
                                authority = 1.0
                            elif dom_type == "organization" and auth_str:
                                authority = 0.7
                            elif len(auth_str) > 20:
                                authority = 0.4
                                
                        relevance = p.get("query_relevance_score", eval_result.overall_score)

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

        # Listwise Ranking
        listwise_rankings = self._generate_listwise_ranking(tc, search_results, diagnosis, url_quality)
        
        # Contrastive Fail Pairs
        contrastive_fail_pairs = self._generate_contrastive_fail_pairs(tc, eval_result, url_quality)
        
        # Scrape Quality Labels
        scrape_quality_labels = self._generate_scrape_quality_labels(tc, eval_result)

        return dpo_pairs, reward_signals, tc_pattern, listwise_rankings, contrastive_fail_pairs, scrape_quality_labels

    def _generate_listwise_ranking(
        self,
        tc: TestCase,
        search_results: List[FirecrawlSearchResult],
        diagnosis: Any,
        url_quality: Dict[str, float]
    ) -> Optional[ListwiseRankingExample]:
        annotations = getattr(diagnosis, "url_quality_annotations", [])
        if len(annotations) < 2:
            return None
            
        ideal_ranking = sorted(url_quality.keys(), key=lambda k: url_quality[k], reverse=True)
        url_quality_notes = {ann.get("url"): ann.get("quality_note", "") for ann in annotations if ann.get("url")}
        
        confidence = "low"
        if len(annotations) >= 3:
            confidence = "high"
        elif len(annotations) >= 1:
            confidence = "medium"
            
        fc_ranking = [r.url for r in sorted(search_results, key=lambda r: r.firecrawl_rank)]
        
        return ListwiseRankingExample(
            query=tc.query,
            test_case_id=tc.id,
            intent=tc.intent,
            difficulty=tc.difficulty,
            ideal_ranking=ideal_ranking,
            url_quality_scores=url_quality,
            url_quality_notes=url_quality_notes,
            firecrawl_ranking=fc_ranking,
            source="judge_quality_annotations",
            confidence=confidence
        )

    def _generate_contrastive_fail_pairs(
        self,
        tc: TestCase,
        eval_result: EvalResult,
        url_quality: Dict[str, float]
    ) -> List[ContrastiveFailPair]:
        pairs = []
        if not eval_result.document_profiles:
            return pairs
            
        for de in getattr(eval_result, "dimension_evals", []):
            if not getattr(de, "contrastive_fail_triggered", False):
                continue
                
            # Find bad URL: top ranked URL from firecrawl_ranking that matches bad state
            fc_urls = [p.get("url") for p in eval_result.document_profiles] # roughly order
            if not fc_urls: continue
            bad_url = fc_urls[0] # simplification: assume top ranked is the bad one triggering it
            
            # Find good URL: highest quality score
            good_url = None
            if url_quality:
                good_url = max(url_quality.keys(), key=lambda k: url_quality[k])
                
            if not good_url or good_url == bad_url:
                continue
                
            bad_state = next((p for p in eval_result.document_profiles if p.get("url") == bad_url), {})
            good_state = next((p for p in eval_result.document_profiles if p.get("url") == good_url), {})
            
            if not bad_state or not good_state:
                continue
                
            # Simplify states
            def _extract_state(state):
                return {
                    "url": state.get("url"),
                    "page_type": state.get("page_type"),
                    "domain_type": state.get("domain_type"),
                    "snippet": state.get("primary_topic", "")[:200],
                    "scrape_score": state.get("scrape_score", 0.0),
                    "content_completeness": state.get("content_completeness", "unknown")
                }
            
            pairs.append(ContrastiveFailPair(
                query=tc.query,
                test_case_id=tc.id,
                dimension=de.dimension_name,
                bad_state=_extract_state(bad_state),
                good_state=_extract_state(good_state),
                failure_explanation=getattr(de, "contrastive_fail_explanation", ""),
                judge_score=de.score,
                failure_level=de.assigned_level
            ))
            
        return pairs

    def _generate_scrape_quality_labels(self, tc: TestCase, eval_result: EvalResult) -> List[ScrapeQualityLabel]:
        labels = []
        if not eval_result.document_profiles:
            return labels
            
        # Get overall fidelity score for the TC as fallback if per-URL is not available
        overall_fidelity = eval_result.fidelity_score
            
        for p in eval_result.document_profiles:
            url = p.get("url")
            if not url: continue
            
            nav_ratio = p.get("nav_link_ratio", 0.0)
            bp_count = p.get("boilerplate_pattern_count", 0)
            words = p.get("word_count", 0)
            table_count = p.get("table_count", 0)
            heading_count = p.get("heading_count", 0)
            list_count = p.get("list_count", 0)
            code_block_count = p.get("code_block_count", 0)
            appears_truncated = (p.get("content_completeness", "") == "appears_truncated")
            content_completeness = p.get("content_completeness", "unknown")
            domain_type = p.get("domain_type", "unknown")
            detected_language = p.get("detected_language", "en")
            
            fid_score = p.get("scrape_score", overall_fidelity)
            
            tables_preserved = (table_count > 0 and fid_score >= 0.7)
            
            issues = []
            if table_count > 0 and not tables_preserved: issues.append("table_flattened")
            if appears_truncated: issues.append("truncated")
            if nav_ratio > 0.30: issues.append("nav_noise_dominant")
            if bp_count >= 3: issues.append("boilerplate_heavy")
            if words < 100: issues.append("thin_content")
            if content_completeness == "navigation_only": issues.append("navigation_only")
            if content_completeness == "error_page": issues.append("error_page")
            if detected_language not in ("en", "mixed", ""): issues.append(f"non_english_content_{detected_language}")
            
            ql = "unusable"
            if fid_score >= 0.80: ql = "excellent"
            elif fid_score >= 0.60: ql = "good"
            elif fid_score >= 0.35: ql = "poor"
            
            labels.append(ScrapeQualityLabel(
                url=url,
                test_case_id=tc.id,
                quality_label=ql,
                fidelity_score=fid_score,
                issues=issues,
                noise_ratio=nav_ratio,
                word_count=words,
                has_tables=(table_count > 0),
                tables_preserved=tables_preserved,
                appears_truncated=appears_truncated,
                boilerplate_pattern_count=bp_count,
                content_completeness=content_completeness,
                domain_type=domain_type
            ))
            
        return labels

    def _generate_query_reformulation(self, tc: TestCase, diagnosis: Any) -> Optional[QueryReformulationPair]:
        qr_dict = getattr(diagnosis, "query_reformulation", None)
        if not qr_dict:
            return None
            
        return QueryReformulationPair(
            test_case_id=tc.id,
            original_query=tc.query,
            reformulated_query=qr_dict.get("reformulated_query", ""),
            chaos_archetype=tc.chaos_archetype,
            intent=tc.intent,
            failing_dimensions=getattr(diagnosis, "failure_dimensions", []),
            expected_coverage_delta=qr_dict.get("expected_delta", ""),
            rationale=qr_dict.get("rationale", "")
        )

    def _generate_sft_gold(
        self,
        test_cases: List[TestCase],
        eval_results: List[EvalResult],
        tc_diagnoses: List[Any],
        search_results_dict: Dict[str, List[FirecrawlSearchResult]],
        threshold: float = 0.85
    ) -> List[SFTGoldExample]:
        gold = []
        tc_map = {tc.id: tc for tc in test_cases}
        diag_map = {d.tc_id: d for d in tc_diagnoses}
        
        for er in eval_results:
            if er.overall_score >= threshold and not er.floor_failures:
                tc = tc_map.get(er.test_case_id)
                diag = diag_map.get(er.test_case_id)
                if not tc: continue
                
                # Determine gold_urls
                gold_urls = []
                if diag and diag.url_quality_annotations:
                    sorted_anns = sorted(diag.url_quality_annotations, key=lambda a: a.get("quality_score", 0), reverse=True)
                    gold_urls = [a.get("url") for a in sorted_anns if a.get("url")]
                else:
                    srs = search_results_dict.get(tc.id, [])
                    gold_urls = [r.url for r in sorted(srs, key=lambda r: r.firecrawl_rank)]
                
                # key claims
                key_claims = []
                if er.document_profiles:
                    for p in er.document_profiles[:3]:
                        claims = p.get("content", {}).get("key_claims", [])
                        for c in claims:
                            if c not in key_claims:
                                key_claims.append(c)
                                
                dim_scores = {de.dimension_name: de.score for de in er.dimension_evals}
                
                import dataclasses
                rubric_dims = [dataclasses.asdict(d) for d in tc.rubric.dimensions] if tc.rubric else []
                
                gold.append(SFTGoldExample(
                    query=tc.query,
                    test_case_id=tc.id,
                    intent=tc.intent,
                    difficulty=tc.difficulty,
                    chaos_archetype=tc.chaos_archetype,
                    overall_score=er.overall_score,
                    gold_urls=gold_urls,
                    key_claims_covered=key_claims,
                    dimension_scores=dim_scores,
                    rubric_dimensions=rubric_dims
                ))
        return gold

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

    def save_signals(
        self,
        dpo_pairs: List[DPOPair],
        reward_signals: List[RewardSignal],
        patterns: List[ImprovementPattern],
        run_id: str,
        listwise_rankings: List[ListwiseRankingExample] = None,
        contrastive_fail_pairs: List[ContrastiveFailPair] = None,
        query_reformulations: List[QueryReformulationPair] = None,
        sft_gold: List[SFTGoldExample] = None,
        scrape_quality_labels: List[ScrapeQualityLabel] = None
    ):
        out_dir = os.path.join(APP_DIR, "outputs", "runs", run_id, "rl_signals")
        os.makedirs(out_dir, exist_ok=True)
        import dataclasses
        
        def _write_jsonl(filename, items):
            if items:
                path = os.path.join(out_dir, filename)
                with open(path, 'w', encoding='utf-8') as f:
                    for item in items:
                        f.write(json.dumps(dataclasses.asdict(item)) + '\n')
        
        _write_jsonl("dpo_pairs.jsonl", dpo_pairs)
        _write_jsonl("rewards.jsonl", reward_signals)
        _write_jsonl("listwise_rankings.jsonl", listwise_rankings)
        _write_jsonl("contrastive_fail_pairs.jsonl", contrastive_fail_pairs)
        _write_jsonl("query_reformulations.jsonl", query_reformulations)
        _write_jsonl("sft_gold.jsonl", sft_gold)
        _write_jsonl("scrape_quality_labels.jsonl", scrape_quality_labels)
                
        # Save taxonomy
        tax_path = os.path.join(out_dir, "taxonomy.json")
        with open(tax_path, 'w', encoding='utf-8') as f:
            # Handle both dataclasses and dicts
            out_patterns = [dataclasses.asdict(p) if dataclasses.is_dataclass(p) else p for p in patterns]
            json.dump(out_patterns, f, indent=2)
            
        logger.info(f"Saved RL signals to {out_dir}")

    async def save_signals_async(self, *args, **kwargs):
        await asyncio.to_thread(self.save_signals, *args, **kwargs)
