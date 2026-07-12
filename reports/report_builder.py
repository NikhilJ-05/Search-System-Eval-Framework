import os
import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from models.eval_result import EvalResult
from models.test_case import TestCase
from eval.comparator import RankingComparator

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

class ReportBuilder:
    def __init__(self, config=None):
        self.config = config

    def _build_histogram(self, scores: List[float]) -> str:
        bins = [0, 0, 0, 0, 0]
        for s in scores:
            if s < 0.2: bins[0] += 1
            elif s < 0.4: bins[1] += 1
            elif s < 0.6: bins[2] += 1
            elif s < 0.8: bins[3] += 1
            else: bins[4] += 1
        
        max_bin = max(bins) if bins else 1
        bar_len = 20
        hist = ""
        labels = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
        for i, count in enumerate(bins):
            filled = int((count / max_bin) * bar_len)
            bar = "▓" * filled + "░" * (bar_len - filled)
            hist += f"  {labels[i]}  {bar}  {count}\n"
        return hist

    def build_markdown(
        self, 
        run_id: str, 
        test_cases: List[TestCase], 
        eval_results: List[EvalResult],
        search_results_dict: dict = None, 
        rl_summary: dict = None,
        reg_data: dict = None,
        round_stats: List[dict] = None,
        kb_rankings: dict = None,
        comparator: RankingComparator = None,
        improvement_analysis: Any = None,
        tc_diagnoses: List[Any] = None,
        run_meta: dict = None
    ) -> str:
        logger.info(f"Building markdown report for run {run_id}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md = f"# Firecrawl Eval Report: {run_id}\nGenerated: {timestamp}\n\n"
        
        if run_meta:
            md += "## Run Configuration\n"
            md += "| Setting | Value |\n"
            md += "|---|---|\n"
            md += f"| Generator Model | {run_meta.get('generator_model', '')} |\n"
            md += f"| P1 Model (Extraction) | {run_meta.get('p1_model', '')} |\n"
            md += f"| P2 Model (Reasoning)  | {run_meta.get('p2_model', '')} |\n"
            md += f"| Improvement Agent | {run_meta.get('improvement_agent_model', '')} |\n"
            md += f"| Pass Threshold | {run_meta.get('pass_threshold', 0.65)} (floor: {run_meta.get('dimension_floor', 0.40)}) |\n"
            md += f"| Test Cases | {run_meta.get('num_test_cases', len(eval_results))} |\n"
            
            dur = run_meta.get('duration_s', 0)
            mins, secs = int(dur // 60), int(dur % 60)
            md += f"| Duration | {mins}m {secs}s |\n\n"
        
        if not eval_results:
            return md + "No evaluation results."
            
        avg_overall = sum(e.overall_score for e in eval_results) / len(eval_results)
        
        threshold = self.config.pass_threshold if self.config else 0.65
        floor = self.config.dimension_floor if self.config else 0.40
        passed_count = sum(1 for e in eval_results if e.passes(threshold, floor))
        failed_count = len(eval_results) - passed_count
        status_icon = "🟢" if avg_overall >= 0.8 else ("🟡" if avg_overall >= 0.6 else "🔴")
        
        md += "## Executive Summary\n"
        md += f"- **Overall Score**: {avg_overall:.2f} {status_icon}\n"
        md += f"- **Test Cases**: {len(eval_results)} | Passed: {passed_count} | Failed: {failed_count}\n\n"
        
        # Floor failures summary
        tc_with_floor_fails = [e for e in eval_results if e.floor_failures]
        if tc_with_floor_fails:
            floor_dim_counts = {}
            for e in tc_with_floor_fails:
                for f in e.floor_failures:
                    floor_dim_counts[f] = floor_dim_counts.get(f, 0) + 1
            most_common_floor = max(floor_dim_counts, key=floor_dim_counts.get) if floor_dim_counts else "None"
            md += "### Floor Failures (Dimension Score < {:.2f})\n".format(floor)
            md += f"- **TCs with floor failures**: {len(tc_with_floor_fails)} / {len(eval_results)}\n"
            md += f"- **Most common floor dimension**: `{most_common_floor}` ({floor_dim_counts.get(most_common_floor, 0)} TCs)\n\n"

        md += self._build_dimension_breakdown(eval_results, threshold, floor)
        md += self._build_top_unmet_criteria(eval_results)
        
        if improvement_analysis and getattr(improvement_analysis, 'root_causes', []):
            primary_rc = improvement_analysis.root_causes[0].title
            md += f"### Executive Diagnosis\n"
            md += f"This run achieved a pass rate of **{passed_count/max(1, len(eval_results))*100:.0f}%** across {len(eval_results)} test cases. "
            md += f"The primary bottleneck identified is **{primary_rc}**, impacting {improvement_analysis.root_causes[0].frequency} of the evaluated queries. "
            md += f"Addressing the key root causes could yield a significant boost in performance, particularly on the **{improvement_analysis.root_causes[0].dimension}** dimension.\n\n"
            
        # Round Progression (If Batched)
        if round_stats:
            md += "## Batch Progression (KB Build)\n"
            md += "| Round | TCs | New Indexed | Deduped (Hits) |\n"
            md += "|-------|-----|-------------|----------------|\n"
            for stat in round_stats:
                md += f"| {stat['round']} | {stat['tcs_processed']} | {stat['new_indexed_docs']} | {stat['deduped_docs']} |\n"
            md += "\n"

        # Cache Analytics
        md += "## Two-Layer Cache Analytics\n"
        
        # Calculate hits
        q_hits = 0
        c_hits = 0
        total_q = len(eval_results)
        total_c = 0
        
        intent_validation = {}
        for tc in test_cases:
            intent_validation[tc.cache_intent] = {"count": 0, "q_hits": 0, "c_hits": 0, "total_c": 0}
            
        for res in eval_results:
            tc = next(t for t in test_cases if t.id == res.test_case_id)
            intent = tc.cache_intent
            
            search_res_list = search_results_dict.get(res.test_case_id, [])
            if search_res_list and search_res_list[0].query_cache_status == "hit":
                q_hits += 1
                intent_validation[intent]["q_hits"] += 1
                
            intent_validation[intent]["count"] += 1
            
            for sr in search_res_list:
                if sr.full_markdown: # Only count actually scraped/cached urls
                    total_c += 1
                    intent_validation[intent]["total_c"] += 1
                    if sr.scrape_cache_status == "kb_semantic_hit":
                        c_hits += 1
                        intent_validation[intent]["c_hits"] += 1
                        
        q_rate = (q_hits / total_q) * 100 if total_q else 0
        c_rate = (c_hits / total_c) * 100 if total_c else 0
        
        md += f"- **Layer 1 (Query) Cache Hit Rate**: {q_rate:.1f}% ({q_hits}/{total_q})\n"
        md += f"- **Layer 2 (Content) Cache Hit Rate**: {c_rate:.1f}% ({c_hits}/{total_c})\n\n"
        
        md += "### Cache Intent Validation\n"
        md += "*(Did the generator successfully trick the cache?)*\n"
        md += "| Generator Intent | Count | Query Hit % | Content Hit % |\n"
        md += "|------------------|-------|-------------|---------------|\n"
        for intent, data in intent_validation.items():
            if data["count"] > 0:
                q_pct = (data["q_hits"] / data["count"]) * 100
                c_pct = (data["c_hits"] / data["total_c"]) * 100 if data["total_c"] else 0
                md += f"| `{intent}` | {data['count']} | {q_pct:.1f}% | {c_pct:.1f}% |\n"
        md += "\n"
        
        md += self._build_archetype_breakdown(test_cases, eval_results, threshold, floor)
        md += self._build_intent_difficulty_breakdown(test_cases, eval_results, threshold, floor)

        # Three-Way Retrieval Comparison
        if kb_rankings and comparator:
            md += "## Retrieval Comparison: Firecrawl vs KB vs Ideal\n"
            md += "*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*\n\n"
            
            fc_taus, kb_taus = [], []
            fc_o3, kb_o3 = [], []
            
            for res in eval_results:
                tc = next(t for t in test_cases if t.id == res.test_case_id)
                fc_urls = [r.url for r in search_results_dict.get(tc.id, [])]
                kb_urls = kb_rankings.get(tc.id, [])

                # Derive ideal URL order from document profiles: highest key_claims density = most valuable result
                profiles = getattr(res, 'document_profiles', [])
                ideal_urls = [p.get('url', '') for p in sorted(
                    profiles,
                    key=lambda p: len(p.get('key_claims', [])),
                    reverse=True
                )] if profiles else fc_urls  # fallback to fc order if no profiles

                comp = comparator.compare(fc_urls, ideal_urls, kb_urls)
                fc_taus.append(comp["fc_vs_ideal"]["kendall_tau"])
                kb_taus.append(comp["kb_vs_ideal"]["kendall_tau"])
                fc_o3.append(comp["fc_vs_ideal"]["overlap_at_3"])
                kb_o3.append(comp["kb_vs_ideal"]["overlap_at_3"])
                
            avg_fc_tau = sum(fc_taus)/len(fc_taus) if fc_taus else 0
            avg_kb_tau = sum(kb_taus)/len(kb_taus) if kb_taus else 0
            avg_fc_o3 = sum(fc_o3)/len(fc_o3) if fc_o3 else 0
            avg_kb_o3 = sum(kb_o3)/len(kb_o3) if kb_o3 else 0
            
            fc_o5, kb_o5 = [], []
            kb_outperforms = []
            for res in eval_results:
                tc = next(t for t in test_cases if t.id == res.test_case_id)
                fc_urls = [r.url for r in search_results_dict.get(tc.id, [])]
                kb_urls = kb_rankings.get(tc.id, [])
                profiles = getattr(res, 'document_profiles', [])
                ideal_urls = [p.get('url', '') for p in sorted(
                    profiles,
                    key=lambda p: len(p.get('key_claims', [])),
                    reverse=True
                )] if profiles else fc_urls
                comp = comparator.compare(fc_urls, ideal_urls, kb_urls)
                fc_o5.append(comp["fc_vs_ideal"].get("overlap_at_5", 0))
                kb_o5.append(comp["kb_vs_ideal"].get("overlap_at_5", 0))
                kb_outperforms.append(comp.get("kb_outperforms_fc", False))

            avg_fc_o5 = sum(fc_o5)/len(fc_o5) if fc_o5 else 0
            avg_kb_o5 = sum(kb_o5)/len(kb_o5) if kb_o5 else 0
            kb_win_rate = (sum(1 for x in kb_outperforms if x) / len(kb_outperforms)) * 100 if kb_outperforms else 0

            avg_fc_tau_display = (avg_fc_tau + 1) / 2
            avg_kb_tau_display = (avg_kb_tau + 1) / 2

            md += "| Metric | Firecrawl | Internal KB | Winner |\n"
            md += "|--------|-----------|-------------|--------|\n"
            md += f"| Kendall's τ (vs Ideal, normalized 0→1) | {avg_fc_tau_display:.3f} | {avg_kb_tau_display:.3f} | {'KB 🏆' if avg_kb_tau > avg_fc_tau else 'Firecrawl 🏆'} |\n"
            md += f"| Overlap@3 (vs Ideal) | {avg_fc_o3:.3f} | {avg_kb_o3:.3f} | {'KB 🏆' if avg_kb_o3 > avg_fc_o3 else 'Firecrawl 🏆'} |\n"
            md += f"| Overlap@5 (vs Ideal) | {avg_fc_o5:.3f} | {avg_kb_o5:.3f} | {'KB 🏆' if avg_kb_o5 > avg_fc_o5 else 'Firecrawl 🏆'} |\n"
            md += f"| KB Outperforms FC | - | - | {kb_win_rate:.1f}% of TCs |\n\n"


        # Improvement Roadmap
        if improvement_analysis:
            md += "## Improvement Roadmap\n\n"
            
            if getattr(improvement_analysis, 'root_causes', []):
                md += "### Root Causes (ranked by severity)\n"
                md += "| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |\n"
                md += "|---|-----------|-------|----------|------------|--------------|-----------|\n"
                for i, rc in enumerate(improvement_analysis.root_causes, 1):
                    tcs_str = ", ".join(rc.affected_tcs[:3])
                    if len(rc.affected_tcs) > 3: tcs_str += "..."
                    conf = getattr(rc, 'confidence', 'medium')
                    md += f"| {i} | {rc.dimension} | {rc.title} | {rc.severity} | {conf} | {tcs_str} | {rc.frequency} |\n"
                md += "\n"
                
            if getattr(improvement_analysis, 'proposals', []):
                md += "### Proposals (ranked by priority)\n"
                md += "| # | Targets | Proposal | Expected Impact | Effort | Priority |\n"
                md += "|---|---------|----------|-----------------|--------|----------|\n"
                # Sort proposals by priority_score descending
                sorted_props = sorted(improvement_analysis.proposals, key=lambda x: getattr(x, 'priority_score', 0), reverse=True)
                for i, prop in enumerate(sorted_props, 1):
                    md += f"| {i} | {prop.targets_root_cause} | {prop.title} | {prop.expected_impact} | {prop.effort} | {getattr(prop, 'priority_score', 'N/A')} |\n"
                md += "\n"

            if getattr(improvement_analysis, 'quick_wins', []):
                md += "### Quick Wins\n"
                md += "| # | Action | Description | Expected Impact |\n"
                md += "|---|--------|-------------|-----------------|\n"
                for i, qw in enumerate(improvement_analysis.quick_wins, 1):
                    md += f"| {i} | {qw.get('title','')} | {qw.get('description','')} | {qw.get('expected_impact','')} |\n"
                md += "\n"

            if getattr(improvement_analysis, 'cross_dimension_patterns', []):
                md += "### Cross-Dimension Failure Patterns\n"
                md += "| Pattern | Hypothesis / Context |\n"
                md += "|---------|----------------------|\n"
                for pat in improvement_analysis.cross_dimension_patterns:
                    md += f"| {pat.get('pattern','')} | {pat.get('hypothesis','')} |\n"
                md += "\n"
                
            if getattr(improvement_analysis, 'judge_bias_flags', []):
                md += "### Judge Bias Warnings\n"
                for bias in improvement_analysis.judge_bias_flags:
                    md += f"- ⚠️ {bias}\n"
                md += "\n"

        # RL Signal Bridge
        if rl_summary:
            md += "## RL Training Signals\n"
            md += "| Signal Type | Count | Output File |\n"
            md += "|-------------|-------|-------------|\n"
            md += f"| DPO Pairs | {rl_summary.get('dpo_pairs', 0)} | dpo_pairs.jsonl |\n"
            md += f"| Reward Signals | {rl_summary.get('reward_signals', 0)} | rewards.jsonl |\n"
            md += f"| Listwise Rankings | {rl_summary.get('listwise_rankings', 0)} | listwise_rankings.jsonl |\n"
            md += f"| Contrastive Fail Pairs | {rl_summary.get('contrastive_fail_pairs', 0)} | contrastive_fail_pairs.jsonl |\n"
            md += f"| Query Reformulations | {rl_summary.get('query_reformulations', 0)} | query_reformulations.jsonl |\n"
            md += f"| SFT Gold Examples | {rl_summary.get('sft_gold_examples', 0)} | sft_gold.jsonl |\n"
            md += f"| Scrape Quality Labels | {rl_summary.get('scrape_quality_labels', 0)} | scrape_quality_labels.jsonl |\n\n"
            if rl_summary.get('patterns'):
                md += "### Improvement Taxonomy (Micro-Patterns)\n"
                md += "| Issue | Severity | Frequency | Description |\n"
                md += "|-------|----------|-----------|-------------|\n"
                for p in rl_summary['patterns']:
                    # if ImprovementPattern dataclass, get attributes
                    issue = getattr(p, 'issue', p.get('issue', '')) if not isinstance(p, dict) else p.get('issue', '')
                    sev = getattr(p, 'severity', p.get('severity', '')) if not isinstance(p, dict) else p.get('severity', '')
                    freq = getattr(p, 'frequency', p.get('frequency', '')) if not isinstance(p, dict) else p.get('frequency', '')
                    desc = getattr(p, 'description', p.get('description', '')) if not isinstance(p, dict) else p.get('description', '')
                    md += f"| {issue} | {sev} | {freq} | {desc} |\n"
                md += "\n"

        # Regression
        if reg_data:
            md += "## Regression vs Previous Run\n"
            md += f"- Trend: {reg_data.get('trend', 'Unknown')}\n"
            if 'diff' in reg_data:
                md += f"- Difference: {reg_data['diff']:+.2f}\n"
            
        # Appendix: Failed Cases Only
        failed_results = [e for e in eval_results if not e.passes()]
        if failed_results:
            md += "\n## Appendix: Failed Test Cases Detail\n"
            md += "*(Showing only test cases that failed the pass threshold or hit a dimension floor)*\n\n"
            
            tc_dict = {tc.id: tc for tc in test_cases}
            diag_dict = {d.tc_id: d for d in tc_diagnoses} if tc_diagnoses else {}
            
            for idx, res in enumerate(failed_results):
                tc = tc_dict[res.test_case_id]
                diag = diag_dict.get(tc.id)
                md += f"### {tc.id} (Score: {res.overall_score:.2f}) ❌\n"
                md += f"**Query**: `{tc.query}`\n"
                md += f"**Category**: {tc.category} | **Intent**: {tc.cache_intent}\n\n"
                
                if diag:
                    md += f"**Root Cause**: {diag.root_cause_summary}\n\n"
                    md += f"- **Coverage Diagnosis**: {diag.coverage_diagnosis}\n"
                    md += f"- **Ranking Diagnosis**: {diag.ranking_diagnosis}\n"
                    md += f"- **Scrape Diagnosis**: {diag.scrape_diagnosis}\n\n"
                    if diag.improvement_actions:
                        md += f"**Fix Actions**:\n"
                        for act in diag.improvement_actions:
                            md += f"- {act}\n"
                        md += "\n"
                else:
                    for de in getattr(res, 'dimension_evals', []):
                        if de.score < 0.8:
                            md += f"**{de.dimension_name} Issue (Score: {de.score:.2f}, Level: {de.assigned_level})**\n"
                            md += f"- Reasoning: {de.reasoning}\n"
                            if de.contrastive_fail_triggered:
                                md += f"- Contrastive Fail: {de.contrastive_fail_explanation}\n"
                md += "\n---\n"
                
        out_dir = os.path.join(APP_DIR, "outputs", "runs", run_id)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "report.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md)
            
        return path

    def build_tc_report(self, tc: TestCase, eval_result: EvalResult, search_results: List[Any], diag: Any, pass_threshold: float) -> str:
        passed = eval_result.passes(pass_threshold, 0.40)
        badge = "🟢 PASSED" if passed else "🔴 FAILED"
        
        md = f"# Test Case Report: {tc.id} ({badge})\n\n"
        md += f"## Metadata\n"
        md += f"- **Query**: `{tc.query}`\n"
        md += f"- **Category**: {tc.category}\n"
        md += f"- **Intent**: {tc.intent}\n"
        md += f"- **Difficulty**: {tc.difficulty}\n"
        md += f"- **Overall Score**: {eval_result.overall_score:.3f}\n"
        if getattr(eval_result, "floor_failures", []):
            md += f"- **Floor Failures**: {', '.join(eval_result.floor_failures)} (Score < 0.40)\n"
        
        # Cache Status
        md += f"\n## Cache Behavior\n"
        if search_results:
            q_status = search_results[0].query_cache_status if hasattr(search_results[0], 'query_cache_status') else "unknown"
            md += f"- **Query Cache**: {q_status}\n"
            md += f"- **Content Cache Per Result**:\n"
            for res in search_results:
                c_status = res.scrape_cache_status if hasattr(res, 'scrape_cache_status') else "unknown"
                md += f"  - `{res.url}`: {c_status}\n"
        else:
            md += f"No search results collected.\n"
            
        # Judge Results
        md += f"\n## Judge Evaluation Details\n"
        for i, de in enumerate(getattr(eval_result, 'dimension_evals', []), 1):
            status = "✅" if de.score >= pass_threshold else ("⚠️" if de.score >= 0.40 else "❌")
            md += f"### {i}. {de.dimension_name} (Score: {de.score:.2f}, Level: {de.assigned_level}) {status}\n"
            md += f"- **Weight**: {de.weight:.2f}\n"
            md += f"- **Reasoning**: {de.reasoning}\n"
            md += f"- **Level Justification**: {de.level_justification}\n"
            md += f"- **Contrastive Fail Triggered**: {'YES ⚠️' if de.contrastive_fail_triggered else 'No'}\n"
            if de.contrastive_fail_triggered:
                md += f"- **Failure Explanation**: {de.contrastive_fail_explanation}\n"
            md += "\n"

        if getattr(eval_result, 'document_profiles', None):
            md += f"### Document Profiles Evaluated\n"
            md += "| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |\n"
            md += "|------|-----|-------------|-------|----------|--------|--------------|\n"
            for p in eval_result.document_profiles:
                st = p.get('structure', {})
                co = p.get('content', {})
                md += f"| {p.get('rank', '-')} | {p.get('url', 'N/A')} | {st.get('domain_type', 'N/A')} | {st.get('size', {}).get('total_words', 0)} | {st.get('structure', {}).get('heading_count', 0)} | {st.get('structure', {}).get('table_count', 0)} | {co.get('content_completeness', 'unknown')} |\n"
            md += "\n"
            
        # Failure Diagnosis Section
        if not passed:
            md += f"\n## Failure Diagnosis & Recovery Roadmap\n"
            if diag:
                dims = ", ".join(getattr(diag, "failure_dimensions", []))
                if getattr(diag, "floor_failures", []):
                    dims += f" (Critical: {', '.join(diag.floor_failures)})"
                md += f"- **Failure Dimensions**: `{dims}`\n"
                md += f"- **Root Cause**: {getattr(diag, 'root_cause_summary', 'N/A')}\n\n"
                md += f"### Diagnostic Breakdown\n"
                md += f"- **Coverage Diagnosis**: {getattr(diag, 'coverage_diagnosis', 'N/A')}\n"
                md += f"- **Ranking Diagnosis**: {getattr(diag, 'ranking_diagnosis', 'N/A')}\n"
                md += f"- **Scrape Diagnosis**: {getattr(diag, 'scrape_diagnosis', 'N/A')}\n\n"
                if getattr(diag, 'improvement_actions', []):
                    md += f"### Recommended Fix Actions\n"
                    for act in diag.improvement_actions:
                        md += f"- {act}\n"
            else:
                md += "No detailed automated diagnosis was generated for this failure.\n"
        else:
            if diag and (getattr(diag, 'improvement_actions', []) or getattr(diag, 'micro_pattern', None)):
                md += f"\n## Optimization Opportunities\n"
                md += f"*(This test case passed, but the diagnostic LLM found areas for proactive improvement)*\n\n"
                md += f"- **Observations**: {getattr(diag, 'root_cause_summary', 'N/A')}\n\n"
                if getattr(diag, 'improvement_actions', []):
                    md += f"### Suggested Enhancements\n"
                    for act in diag.improvement_actions:
                        md += f"- {act}\n"
                if getattr(diag, 'micro_pattern', None):
                    mp = diag.micro_pattern
                    md += f"\n### Identified Micro-Pattern\n"
                    md += f"- **Type**: `{mp.get('pattern_type', 'unknown')}`\n"
                    md += f"- **Description**: {mp.get('description', '')}\n"
                    
        return md

    def build_tc_reports(self, run_id: str, test_cases: List[TestCase], eval_results: List[EvalResult], search_results_dict: dict, tc_diagnoses: List[Any], pass_threshold: float) -> List[str]:
        out_dir = os.path.join(APP_DIR, "outputs", "runs", run_id, "tc_reports")
        os.makedirs(out_dir, exist_ok=True)
        
        tc_dict = {tc.id: tc for tc in test_cases}
        diag_dict = {d.tc_id: d for d in tc_diagnoses} if tc_diagnoses else {}
        
        paths = []
        for res in eval_results:
            tc = tc_dict.get(res.test_case_id)
            if not tc:
                continue
            search_res = search_results_dict.get(tc.id, [])
            diag = diag_dict.get(tc.id)
            
            md = self.build_tc_report(tc, res, search_res, diag, pass_threshold)
            
            path = os.path.join(out_dir, f"{tc.id}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            paths.append(path)
            
        return paths


    def _build_dimension_breakdown(self, eval_results: List[EvalResult], threshold: float, floor: float) -> str:
        md = "## Dimension Performance Breakdown\n"
        md += "| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |\n"
        md += "|-----------|-------------|-----------|-----------|-------------|-----------|\n"
        
        dim_stats = {}
        for e in eval_results:
            for de in getattr(e, 'dimension_evals', []):
                name = de.dimension_name
                if name not in dim_stats:
                    dim_stats[name] = {"scores": [], "weights": [], "floor_fails": 0}
                dim_stats[name]["scores"].append(de.score)
                dim_stats[name]["weights"].append(de.weight)
                if de.score < floor:
                    dim_stats[name]["floor_fails"] += 1
                    
        sorted_dims = sorted(dim_stats.items(), key=lambda x: sum(x[1]["scores"])/max(1, len(x[1]["scores"])))
        for name, stats in sorted_dims:
            scores = stats["scores"]
            avg_score = sum(scores) / len(scores)
            avg_weight = sum(stats["weights"]) / len(stats["weights"])
            pass_rate = (sum(1 for s in scores if s >= threshold) / len(scores)) * 100
            hist = self._build_histogram(scores).replace('\n', '<br>')
            md += f"| {name} | {avg_weight:.2f} | {avg_score:.2f} | {pass_rate:.1f}% | {stats['floor_fails']} | <pre>{hist}</pre> |\n"
        return md + "\n"

    def _build_top_unmet_criteria(self, eval_results: List[EvalResult]) -> str:
        md = "## Most Frequently Unmet Rubric Criteria\n"
        md += "| Condition (truncated) | Times Not Met |\n"
        md += "|---|---|\n"
        
        misses = {}
        for e in eval_results:
            for de in getattr(e, 'dimension_evals', []):
                for check in de.criteria_checklist:
                    if check.status == "NOT_MET":
                        cond = check.condition[:80] + "..." if len(check.condition) > 80 else check.condition
                        misses[cond] = misses.get(cond, 0) + 1
                        
        sorted_misses = sorted(misses.items(), key=lambda x: x[1], reverse=True)[:8]
        if not sorted_misses:
            return md + "| No unmet criteria found! | - |\n\n"
            
        for cond, count in sorted_misses:
            md += f"| {cond} | {count} |\n"
        return md + "\n"

    def _build_archetype_breakdown(self, test_cases: List[TestCase], eval_results: List[EvalResult], threshold: float, floor: float) -> str:
        md = "## Chaos Archetype Analysis\n"
        md += "| Archetype | TCs | Avg Score | Pass Rate |\n"
        md += "|---|---|---|---|\n"
        
        tc_dict = {tc.id: tc for tc in test_cases}
        arch_stats = {}
        
        for e in eval_results:
            tc = tc_dict.get(e.test_case_id)
            if not tc: continue
            arch = getattr(tc, 'chaos_archetype', 'none')
            if arch not in arch_stats:
                arch_stats[arch] = {"count": 0, "scores": [], "passes": 0}
            arch_stats[arch]["count"] += 1
            arch_stats[arch]["scores"].append(e.overall_score)
            if e.passes(threshold, floor):
                arch_stats[arch]["passes"] += 1
                
        sorted_arch = sorted(arch_stats.items(), key=lambda x: sum(x[1]["scores"])/max(1, len(x[1]["scores"])))
        for arch, stats in sorted_arch:
            avg = sum(stats["scores"]) / stats["count"]
            pass_rate = (stats["passes"] / stats["count"]) * 100
            warning = " ⚠️" if pass_rate < 50 else ""
            md += f"| {arch}{warning} | {stats['count']} | {avg:.2f} | {pass_rate:.1f}% |\n"
        return md + "\n"

    def _build_intent_difficulty_breakdown(self, test_cases: List[TestCase], eval_results: List[EvalResult], threshold: float, floor: float) -> str:
        md = "## Intent × Difficulty Analysis\n\n"
        
        tc_dict = {tc.id: tc for tc in test_cases}
        intent_stats = {}
        diff_stats = {}
        
        for e in eval_results:
            tc = tc_dict.get(e.test_case_id)
            if not tc: continue
            
            intent = getattr(tc, 'intent', 'unknown')
            if intent not in intent_stats:
                intent_stats[intent] = {"count": 0, "scores": [], "passes": 0}
            intent_stats[intent]["count"] += 1
            intent_stats[intent]["scores"].append(e.overall_score)
            if e.passes(threshold, floor):
                intent_stats[intent]["passes"] += 1
                
            diff = getattr(tc, 'difficulty', 'unknown')
            if diff not in diff_stats:
                diff_stats[diff] = {"count": 0, "scores": [], "passes": 0}
            diff_stats[diff]["count"] += 1
            diff_stats[diff]["scores"].append(e.overall_score)
            if e.passes(threshold, floor):
                diff_stats[diff]["passes"] += 1
                
        md += "### By Intent\n"
        md += "| Intent | TCs | Avg Score | Pass Rate |\n"
        md += "|---|---|---|---|\n"
        for intent, stats in sorted(intent_stats.items(), key=lambda x: sum(x[1]["scores"])/max(1, len(x[1]["scores"]))):
            avg = sum(stats["scores"]) / stats["count"]
            pass_rate = (stats["passes"] / stats["count"]) * 100
            md += f"| {intent} | {stats['count']} | {avg:.2f} | {pass_rate:.1f}% |\n"
            
        md += "\n### By Difficulty\n"
        md += "| Difficulty | TCs | Avg Score | Pass Rate |\n"
        md += "|---|---|---|---|\n"
        for diff, stats in sorted(diff_stats.items(), key=lambda x: sum(x[1]["scores"])/max(1, len(x[1]["scores"]))):
            avg = sum(stats["scores"]) / stats["count"]
            pass_rate = (stats["passes"] / stats["count"]) * 100
            md += f"| {diff} | {stats['count']} | {avg:.2f} | {pass_rate:.1f}% |\n"
            
        return md + "\n"

    async def build_markdown_async(self, *args, **kwargs) -> str:
        return await asyncio.to_thread(self.build_markdown, *args, **kwargs)

    async def build_tc_reports_async(self, *args, **kwargs) -> List[str]:
        return await asyncio.to_thread(self.build_tc_reports, *args, **kwargs)

    def build_single_tc_report(self, run_id: str, tc: TestCase, eval_res: EvalResult, search_res: list, diag: Any, pass_threshold: float) -> str:
        out_dir = os.path.join(APP_DIR, "outputs", "runs", run_id, "tc_reports")
        os.makedirs(out_dir, exist_ok=True)
        md = self.build_tc_report(tc, eval_res, search_res, diag, pass_threshold)
        path = os.path.join(out_dir, f"{tc.id}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        return path

    async def build_single_tc_report_async(self, *args, **kwargs) -> str:
        return await asyncio.to_thread(self.build_single_tc_report, *args, **kwargs)
