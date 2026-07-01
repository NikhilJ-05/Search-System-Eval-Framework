import logging
import json
from typing import List, Dict, Any
from dataclasses import dataclass, field
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig
from models.test_case import TestCase
from models.eval_result import EvalResult, FirecrawlSearchResult

logger = logging.getLogger(__name__)

@dataclass
class TestCaseDiagnosis:
    tc_id: str
    overall_score: float
    failure_dimensions: List[str]
    root_cause_summary: str
    coverage_diagnosis: str
    ranking_diagnosis: str
    scrape_diagnosis: str
    improvement_actions: List[str]

@dataclass
class RootCause:
    id: str
    dimension: str           # "coverage" | "ranking" | "scrape" | "system"
    title: str
    evidence: List[str]      # Specific TC IDs and what went wrong
    affected_tcs: List[str]
    severity: str            # "critical" | "high" | "medium" | "low"
    frequency: str           # e.g., "8/50 TCs"
    confidence: str = "medium" # "low" | "medium" | "high"

@dataclass
class ImprovementProposal:
    id: str
    targets_root_cause: str  # root cause ID
    title: str
    description: str         # Concrete engineering proposal
    expected_impact: str     # e.g., "+0.12 on ranking dimension"
    effort: str              # "low" | "medium" | "high"
    priority_score: float    # 1-10 computed from impact × frequency / effort

@dataclass
class ImprovementAnalysis:
    root_causes: List[RootCause] = field(default_factory=list)
    proposals: List[ImprovementProposal] = field(default_factory=list)
    judge_bias_flags: List[str] = field(default_factory=list)
    enhanced_patterns: List[dict] = field(default_factory=list)
    quick_wins: List[dict] = field(default_factory=list)
    cross_dimension_patterns: List[dict] = field(default_factory=list)

class ImprovementAgent:
    def __init__(self, config: EvalConfig, or_pool: OpenRouterClientPool):
        self.config = config
        self.or_pool = or_pool
        self.model = config.improvement_agent_model
        self.providers = config.improvement_agent_providers or config.generator_providers


    def _build_agent_input(self, test_cases: List[TestCase], eval_results: List[EvalResult], 
                           search_results_dict: dict, cache_analytics: dict, retrieval_comparison: dict,
                           tc_diagnoses: List[TestCaseDiagnosis] = None) -> dict:
        tc_dict = {tc.id: tc for tc in test_cases}
        
        # Histograms
        overall_scores = [e.overall_score for e in eval_results]
        cov_scores = [e.coverage.recall_score for e in eval_results]
        rank_scores = [e.ranking.ndcg_at_5 for e in eval_results]
        
        def compute_hist(scores):
            bins = [0, 0, 0, 0, 0]
            for s in scores:
                if s < 0.2: bins[0] += 1
                elif s < 0.4: bins[1] += 1
                elif s < 0.6: bins[2] += 1
                elif s < 0.8: bins[3] += 1
                else: bins[4] += 1
            return {"0.0-0.2": bins[0], "0.2-0.4": bins[1], "0.4-0.6": bins[2], "0.6-0.8": bins[3], "0.8-1.0": bins[4]}

        # Intent breakdown
        intent_stats = {}
        for res in eval_results:
            tc = tc_dict[res.test_case_id]
            intent = tc.intent
            if intent not in intent_stats:
                intent_stats[intent] = {"count": 0, "overall": 0.0, "coverage": 0.0, "ranking": 0.0}
            intent_stats[intent]["count"] += 1
            intent_stats[intent]["overall"] += res.overall_score
            intent_stats[intent]["coverage"] += res.coverage.recall_score
            intent_stats[intent]["ranking"] += res.ranking.ndcg_at_5
        for intent in intent_stats:
            c = intent_stats[intent]["count"]
            intent_stats[intent] = {
                "count": c,
                "avg_overall": round(intent_stats[intent]["overall"] / c, 3),
                "avg_coverage": round(intent_stats[intent]["coverage"] / c, 3),
                "avg_ranking": round(intent_stats[intent]["ranking"] / c, 3)
            }

        # Difficulty breakdown
        diff_stats = {}
        for res in eval_results:
            tc = tc_dict[res.test_case_id]
            diff = tc.difficulty
            if diff not in diff_stats:
                diff_stats[diff] = {"count": 0, "overall": 0.0}
            diff_stats[diff]["count"] += 1
            diff_stats[diff]["overall"] += res.overall_score
        for diff in diff_stats:
            c = diff_stats[diff]["count"]
            diff_stats[diff] = {
                "count": c,
                "avg_overall": round(diff_stats[diff]["overall"] / c, 3)
            }

        # Ranking disagreements
        ranking_disagreements = []
        for res in eval_results:
            ideal = res.ranking.llm_ideal_ranking
            fc = res.ranking.firecrawl_ranking
            if ideal and fc and ideal[0] != fc[0]:
                tc = tc_dict[res.test_case_id]
                ranking_disagreements.append({
                    "tc_id": tc.id,
                    "query": tc.query,
                    "ideal_first_index": ideal[0],
                    "firecrawl_first_index": fc[0],
                    "reasoning": res.ranking.ranking_reasoning
                })

        # Top coverage misses
        coverage_misses_counts = {}
        for res in eval_results:
            for miss in res.coverage.must_mention_misses:
                coverage_misses_counts[miss] = coverage_misses_counts.get(miss, 0) + 1

        # Best 3 TCs
        sorted_results = sorted(eval_results, key=lambda x: x.overall_score)
        best_3 = []
        for res in sorted_results[-3:]:
            tc = tc_dict[res.test_case_id]
            best_3.append({
                "id": tc.id,
                "query": tc.query,
                "overall_score": res.overall_score
            })
        
        # Bottom 10 TCs by overall score
        worst_10 = []
        for res in sorted_results[:10]:
            tc = tc_dict[res.test_case_id]
            worst_url = ""
            worst_sq_issues = []
            if res.scrape_quality:
                worst_sq = min(res.scrape_quality.items(), key=lambda x: x[1].overall_markdown_quality)
                worst_url = worst_sq[0]
                worst_sq_issues = [f"{i.type}: {i.detail}" for i in worst_sq[1].issues_found]
                
            worst_10.append({
                "id": tc.id,
                "query": tc.query,
                "category": tc.category,
                "intent": tc.intent,
                "overall_score": res.overall_score,
                "coverage_score": res.coverage.recall_score,
                "coverage_misses": res.coverage.must_mention_misses,
                "ranking_score": res.ranking.ndcg_at_5,
                "ranking_suggestions": res.ranking.improvement_suggestions,
                "worst_scrape_url": worst_url,
                "worst_scrape_issues": worst_sq_issues
            })

        # Category breakdown
        cat_stats = {}
        for res in eval_results:
            cat = tc_dict[res.test_case_id].category
            if cat not in cat_stats:
                cat_stats[cat] = {"count": 0, "overall": 0.0}
            cat_stats[cat]["count"] += 1
            cat_stats[cat]["overall"] += res.overall_score
        
        for cat in cat_stats:
            cat_stats[cat]["avg"] = round(cat_stats[cat]["overall"] / cat_stats[cat]["count"], 3)
            del cat_stats[cat]["overall"]

        # Issue frequency
        issue_counts = {}
        for res in eval_results:
            for sq in res.scrape_quality.values():
                for issue in sq.issues_found:
                    issue_counts[issue.type] = issue_counts.get(issue.type, 0) + 1

        avg_overall = sum(r.overall_score for r in eval_results) / max(1, len(eval_results))
        avg_cov = sum(r.coverage.recall_score for r in eval_results) / max(1, len(eval_results))
        avg_rank = sum(r.ranking.ndcg_at_5 for r in eval_results) / max(1, len(eval_results))

        import dataclasses
        return {
            "summary": {
                "total_tcs": len(eval_results),
                "avg_overall": round(avg_overall, 3),
                "avg_coverage": round(avg_cov, 3),
                "avg_ranking": round(avg_rank, 3),
            },
            "score_distributions": {
                "overall": compute_hist(overall_scores),
                "coverage": compute_hist(cov_scores),
                "ranking": compute_hist(rank_scores)
            },
            "intent_breakdown": intent_stats,
            "difficulty_breakdown": diff_stats,
            "ranking_disagreements": ranking_disagreements,
            "top_coverage_misses": coverage_misses_counts,
            "best_3_tcs": best_3,
            "worst_10_tcs": worst_10,
            "category_breakdown": cat_stats,
            "issue_frequency": issue_counts,
            "cache_analytics": cache_analytics,
            "retrieval_comparison": retrieval_comparison,
            "per_tc_diagnoses": [dataclasses.asdict(d) for d in tc_diagnoses] if tc_diagnoses else []
        }

    async def analyze(self, test_cases: List[TestCase], eval_results: List[EvalResult], 
                      search_results_dict: dict, cache_analytics: dict, retrieval_comparison: dict,
                      tc_diagnoses: List[TestCaseDiagnosis] = None) -> ImprovementAnalysis:
        logger.info("Running Improvement Agent (LLM-C) analysis...")
        
        if self.model == "PLACEHOLDER" or not self.model:
            logger.warning("Improvement Agent model is PLACEHOLDER or empty. Skipping LLM call and returning mock analysis.")
            return ImprovementAnalysis(
                root_causes=[RootCause(id="rc_mock", dimension="system", title="Placeholder Agent Mode", evidence=["Model not configured"], affected_tcs=[], severity="low", frequency="0/0", confidence="high")],
                proposals=[ImprovementProposal(id="ip_mock", targets_root_cause="rc_mock", title="Set improvement_agent_model in config", description="Update config.py or .env with a valid OpenRouter model slug.", expected_impact="+0.0", effort="low", priority_score=10.0)],
                judge_bias_flags=[],
                enhanced_patterns=[{"issue": "placeholder", "frequency": "N/A", "description": "Placeholder pattern", "suggested_fix": "Set valid model"}],
                quick_wins=[{"title": "Configure LLM Model", "description": "Add IMPROVEMENT_AGENT_MODEL to environment", "expected_impact": "Full diagnostic analysis activated"}],
                cross_dimension_patterns=[{"pattern": "N/A", "hypothesis": "Mock agent mode active"}]
            )

        agent_input = self._build_agent_input(test_cases, eval_results, search_results_dict, cache_analytics, retrieval_comparison, tc_diagnoses)
        
        system_prompt = """You are a senior Search/IR engineer at Firecrawl. You have just received evaluation results from a comprehensive test run, including individual TestCase diagnoses. Your job is to:
1. Identify the TOP 5 root causes of failure, ranked by impact. Assign a confidence rating ("low", "medium", or "high") to each.
2. For each root cause, propose a SPECIFIC engineering fix.
3. Estimate the expected score improvement if the fix were applied.
4. Flag any patterns that suggest systematic bias in the judge itself.
5. Provide a list of "quick_wins" (fixes requiring low effort but having high impact).
6. Detail "cross_dimension_patterns" representing systematic failures observed across multiple dimensions (e.g. coverage + ranking).
7. Provide enhanced RL training patterns.

Be concrete. Don't say "improve ranking". Say "the recency signal is too weak for queries containing year references — results from 2024 are ranking above 2026 content in 40% of rapidly_changing queries."

Output JSON schema:
{
  "root_causes": [
    {
      "id": "rc_001",
      "dimension": "ranking",
      "title": "Recency signal too weak for temporal queries",
      "evidence": ["tc_abc: 2024 article ranked #1 for '2026 trends'"],
      "affected_tcs": ["tc_abc"],
      "severity": "high",
      "frequency": "8/50 TCs",
      "confidence": "high"
    }
  ],
  "proposals": [
    {
      "id": "ip_001",
      "targets_root_cause": "rc_001",
      "title": "Add temporal-decay ranking signal",
      "description": "Implement a recency multiplier...",
      "expected_impact": "+0.12 on ranking dimension",
      "effort": "medium",
      "priority_score": 8.5
    }
  ],
  "quick_wins": [
    {
      "title": "Shorten Prompt Lengths",
      "description": "Truncate extremely long HTML elements in scraping payload to avoid token exhaustion",
      "expected_impact": "+0.05 overall"
    }
  ],
  "cross_dimension_patterns": [
    {
      "pattern": "SPA websites fail both scrape and ranking",
      "hypothesis": "JavaScript elements fail to load, resulting in blank snippets, which then ruins RRF ranking relevancy"
    }
  ],
  "judge_bias_flags": [
    "Judge may be over-penalizing PDF content..."
  ],
  "enhanced_patterns": [
    {
      "issue": "recency_bias",
      "frequency": "16%",
      "description": "Temporal queries consistently rank stale content higher",
      "suggested_fix": "Add publication-date extraction + recency-decay signal"
    }
  ]
}"""

        prompt = f"Analyze these evaluation results:\n\n{json.dumps(agent_input, indent=2)}"

        try:
            raw_response = await self.or_pool.generate(
                prompt=prompt,
                model=self.model,
                temperature=0.2,
                response_format={"type": "json_object"},
                system_prompt=system_prompt,
                max_tokens=16000,
                providers=self.providers
            )
            
            clean_response = raw_response.strip()
            import re
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', clean_response, re.DOTALL)
            if json_match:
                clean_response = json_match.group(1)
            else:
                start = min([i for i in (clean_response.find('{'), clean_response.find('[')) if i != -1] or [-1])
                if start != -1:
                    is_arr = clean_response[start] == '['
                    end = clean_response.rfind(']' if is_arr else '}')
                    if end != -1:
                        clean_response = clean_response[start:end+1]
            
            data = json.loads(clean_response)
            
            root_causes = [
                RootCause(
                    id=rc.get("id", f"rc_{i:03d}"),
                    dimension=rc.get("dimension", "system"),
                    title=rc.get("title", "Unknown root cause"),
                    evidence=rc.get("evidence", []),
                    affected_tcs=rc.get("affected_tcs", []),
                    severity=rc.get("severity", "medium"),
                    frequency=rc.get("frequency", "unknown"),
                    confidence=rc.get("confidence", "medium"),
                )
                for i, rc in enumerate(data.get("root_causes", []))
            ]
            proposals = [
                ImprovementProposal(
                    id=ip.get("id", f"ip_{i:03d}"),
                    targets_root_cause=ip.get("targets_root_cause", ""),
                    title=ip.get("title", "Untitled proposal"),
                    description=ip.get("description", ""),
                    expected_impact=ip.get("expected_impact", "unknown"),
                    effort=ip.get("effort", "medium"),
                    priority_score=float(ip.get("priority_score", 5.0)),
                )
                for i, ip in enumerate(data.get("proposals", []))
            ]
            
            return ImprovementAnalysis(
                root_causes=root_causes,
                proposals=proposals,
                judge_bias_flags=data.get("judge_bias_flags", []),
                enhanced_patterns=data.get("enhanced_patterns", []),
                quick_wins=data.get("quick_wins", []),
                cross_dimension_patterns=data.get("cross_dimension_patterns", [])
            )
        except Exception as e:
            logger.error(f"Improvement Agent analysis failed: {e}")
            return ImprovementAnalysis()

    async def analyze_tc(self, test_case: TestCase, eval_result: EvalResult, search_results: List[FirecrawlSearchResult]) -> TestCaseDiagnosis:
        logger.info(f"Running TestCase level diagnosis for {test_case.id}...")
        
        failure_dims = []
        if eval_result.coverage.recall_score < self.config.pass_threshold:
            failure_dims.append("coverage")
        if eval_result.ranking.ndcg_at_5 < self.config.pass_threshold:
            failure_dims.append("ranking")
        avg_sq = sum(sq.overall_markdown_quality for sq in eval_result.scrape_quality.values()) / max(1, len(eval_result.scrape_quality))
        if avg_sq < self.config.pass_threshold:
            failure_dims.append("scrape")
            
        # If score is fine, or no model is configured, return simple stub diagnosis
        if not failure_dims or self.model == "PLACEHOLDER" or not self.model:
            return TestCaseDiagnosis(
                tc_id=test_case.id,
                overall_score=eval_result.overall_score,
                failure_dimensions=failure_dims,
                root_cause_summary="Fidelity is stable, minimal issues flagged." if not failure_dims else "Placeholder model mode.",
                coverage_diagnosis="All required elements detected." if "coverage" not in failure_dims else "Missing must_mention items.",
                ranking_diagnosis="Ideal order matches Firecrawl order." if "ranking" not in failure_dims else "Ideal order deviates from Firecrawl order.",
                scrape_diagnosis="Scrape formatting is correct." if "scrape" not in failure_dims else "Markdown formatting issues detected.",
                improvement_actions=[]
            )
            
        # Call OpenRouter to diagnose this single TC
        system_prompt = """You are a Search/IR diagnostics agent at Firecrawl. Given a single test case query and its scoring details, diagnose why the search or scrape failed and recommend 1-3 specific improvement actions.
Output JSON schema:
{
  "root_cause_summary": "1-2 sentence description of main issue",
  "coverage_diagnosis": "Explain what expected terms were missing, if any",
  "ranking_diagnosis": "Explain why ranking diverged from ideal ranking, if any",
  "scrape_diagnosis": "Explain formatting/noise/completeness issues in crawled markdown, if any",
  "improvement_actions": ["concrete action 1", "concrete action 2"]
}"""
        
        # Build clean search results info
        sr_info = []
        for r in search_results:
            sq = eval_result.scrape_quality.get(r.url)
            issues_str = ""
            if sq:
                issues_str = ", ".join(f"{i.type}: {i.detail}" for i in sq.issues_found)
            sr_info.append({
                "rank": r.firecrawl_rank,
                "url": r.url,
                "title": r.title,
                "snippet": r.snippet[:200] if r.snippet else "",
                "scrape_quality_score": sq.overall_markdown_quality if sq else 1.0,
                "scrape_issues": issues_str
            })
            
        prompt_data = {
            "query": test_case.query,
            "category": test_case.category,
            "intent": test_case.intent,
            "difficulty": test_case.difficulty,
            "overall_score": eval_result.overall_score,
            "coverage": {
                "score": eval_result.coverage.recall_score,
                "hits": eval_result.coverage.must_mention_hits,
                "misses": eval_result.coverage.must_mention_misses,
                "reasoning": eval_result.coverage.reasoning
            },
            "ranking": {
                "score": eval_result.ranking.ndcg_at_5,
                "firecrawl_ranking": eval_result.ranking.firecrawl_ranking,
                "llm_ideal_ranking": eval_result.ranking.llm_ideal_ranking,
                "reasoning": eval_result.ranking.ranking_reasoning,
                "suggestions": eval_result.ranking.improvement_suggestions
            },
            "search_results": sr_info
        }
        
        prompt = f"Diagnose this test case failure:\n\n{json.dumps(prompt_data, indent=2)}"
        
        try:
            raw_response = await self.or_pool.generate(
                prompt=prompt,
                model=self.model,
                temperature=0.1,
                response_format={"type": "json_object"},
                system_prompt=system_prompt,
                max_tokens=16000,
                providers=self.providers
            )
            
            clean_response = raw_response.strip()
            import re
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', clean_response, re.DOTALL)
            if json_match:
                clean_response = json_match.group(1)
            else:
                start = min([i for i in (clean_response.find('{'), clean_response.find('[')) if i != -1] or [-1])
                if start != -1:
                    is_arr = clean_response[start] == '['
                    end = clean_response.rfind(']' if is_arr else '}')
                    if end != -1:
                        clean_response = clean_response[start:end+1]
                        
            data = json.loads(clean_response)
            return TestCaseDiagnosis(
                tc_id=test_case.id,
                overall_score=eval_result.overall_score,
                failure_dimensions=failure_dims,
                root_cause_summary=data.get("root_cause_summary", "Unknown root cause"),
                coverage_diagnosis=data.get("coverage_diagnosis", "N/A"),
                ranking_diagnosis=data.get("ranking_diagnosis", "N/A"),
                scrape_diagnosis=data.get("scrape_diagnosis", "N/A"),
                improvement_actions=data.get("improvement_actions", [])
            )
        except Exception as e:
            logger.error(f"Failed to diagnose tc {test_case.id}: {e}")
            return TestCaseDiagnosis(
                tc_id=test_case.id,
                overall_score=eval_result.overall_score,
                failure_dimensions=failure_dims,
                root_cause_summary=f"Analysis failed: {str(e)}",
                coverage_diagnosis="N/A",
                ranking_diagnosis="N/A",
                scrape_diagnosis="N/A",
                improvement_actions=[]
            )
