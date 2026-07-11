import logging
from models.test_case import TestCase, TestCaseExpectedCoverage, TestCaseExpectedRanking, TestCaseExpectedScrapeChallenges
from models.eval_result import FirecrawlSearchResult

logger = logging.getLogger(__name__)

class JudgeCalibration:
    def __init__(self):
        self.gold_cases = self._build_gold_cases()

    def _build_gold_cases(self):
        # Build 1 synthetic test case with known results
        tc = TestCase(
            id="calib_tc_1",
            query="test query for calibration",
            intent="factual_lookup",
            difficulty="easy",
            category="structured_data_extraction",
            expected_coverage=TestCaseExpectedCoverage(
                must_mention=["found_this"],
                should_mention=[],
                min_relevant_results=1
            ),
            expected_ranking=TestCaseExpectedRanking(
                ranking_signals=["recency"],
                ideal_ranking_rationale="best first",
                expected_source_priority=["official_docs"]
            ),
            expected_scrape_challenges=TestCaseExpectedScrapeChallenges(
                likely_page_types=["blog_post"],
                expected_elements=["code_blocks"],
                noise_risks=["sidebar_nav"]
            )
        )
        
        # Perfect result
        res1 = FirecrawlSearchResult(
            query="test query for calibration",
            firecrawl_rank=1,
            url="https://example.com/perfect",
            title="Official Documentation and Guide for Calibration",
            snippet="found_this is right here in our official documentation",
            full_markdown="""# Official Documentation and Guide for Calibration

Welcome to the official documentation page. This comprehensive guide details the calibration procedure and standard metrics.

## Calibration Procedures
To start calibration, we have found_this procedure to be the most effective:
1. Initialize the calibration client.
2. Load the gold standard cases from disk or database.
3. Validate the model output against expected metrics.

## Detailed Metrics Table
Below is a table outlining the recommended thresholds:

| Metric | Minimum Value | Ideal Value | Description |
|---|---|---|---|
| Coverage Recall | 0.80 | 1.00 | Ratio of must-mention terms retrieved |
| NDCG@5 | 0.80 | 1.00 | Ranking quality index |
| Scrape Quality | 0.80 | 0.95 | Cleanliness and semantic structure of markdown |

For further assistance, check out our comprehensive guide or contact support.""",
            scrape_latency_ms=100,
            search_latency_ms=100,
            content_length=500,
            status="success"
        )
        
        # Terrible result
        res2 = FirecrawlSearchResult(
            query="test query for calibration",
            firecrawl_rank=2,
            url="https://example.com/terrible",
            title="Navigation and Cookie Policy Page",
            snippet="nothing useful here",
            full_markdown="""# Navigation Menu
Toggle navigation
* Login
* Signup
* Products
* Services
* Pricing
* Contact

---

{{ cookie_banner_placeholder_error_404 }}
This website uses cookies to ensure you get the best experience on our website. Learn more
[Accept] [Decline]

---

© 2026 Sandbox Inc. All rights reserved. Terms of Service | Privacy Policy""",
            scrape_latency_ms=100,
            search_latency_ms=100,
            content_length=200,
            status="success"
        )
        
        return [(tc, [res1, res2])]

    async def run_calibration(self, judge_client) -> bool:
        logger.info("Running judge calibration (real)...")
        
        passed = 0
        for tc, results in self.gold_cases:
            try:
                eval_res = await judge_client.evaluate(tc, results)
                
                # Check expectations: res1 should be perfect, res2 should be terrible
                # Therefore, coverage should be high, ndcg_at_5 should be high (since perfect is first)
                # Scrape quality for res1 should be high, for res2 should be low
                
                fidelity_score = eval_res.fidelity_score
                is_valid = (
                    eval_res.coverage_score > 0.8 and
                    eval_res.ranking_score > 0.7 and
                    fidelity_score > 0.5 and
                    eval_res.overall_score >= 0.6
                )
                
                if is_valid:
                    passed += 1
                else:
                    logger.warning(f"Calibration case failed expectations. Cov: {eval_res.coverage_score:.2f}, Rnk: {eval_res.ranking_score:.2f}, Overall: {eval_res.overall_score:.2f}")
                    
            except Exception as e:
                logger.error(f"Judge calibration failed on case {tc.id}: {e}")
                
        if passed >= len(self.gold_cases):
            logger.info("Judge calibration passed.")
            return True
        else:
            logger.warning(f"Judge calibration failed ({passed}/{len(self.gold_cases)} passed). Model might be unreliable.")
            return False
