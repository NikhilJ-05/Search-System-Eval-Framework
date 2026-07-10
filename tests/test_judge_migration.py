import sys
import os
import unittest

# Ensure root dir is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.judge import (
    extract_structure_profile,
    extract_spot_check_samples,
    detect_result_overlap,
    is_profile_viable,
    enforce_baseline_dimensions,
    sanity_check
)
from models.test_case import EvalRubric, RubricDimension
from models.eval_result import (
    CriteriaCheck,
    DimensionEval,
    EvalResult
)


class TestJudgeReworkAndMigration(unittest.TestCase):
    def test_extract_structure_profile(self):
        markdown = """# Main Title
Some introductory text with a [link](https://example.com).

## Table Section
| Col A | Col B |
|-------|-------|
| Val 1 | Val 2 |
| Val 3 | Val 4 |

## Code Section
```python
def foo():
    return "bar"
```

Please accept our cookies to continue using this website.
Copyright 2026 Example Corp.
"""
        profile = extract_structure_profile(markdown, "https://example.gov/doc", "Main Title")
        self.assertEqual(profile["domain_type"], "authoritative")
        self.assertEqual(profile["structure"]["heading_count"], 3)
        self.assertEqual(profile["structure"]["table_count"], 1)
        self.assertEqual(profile["structure"]["tables"][0]["row_count"], 3)
        self.assertEqual(profile["structure"]["code_block_count"], 1)
        self.assertTrue(profile["noise"]["cookie_banner_present"])
        self.assertGreaterEqual(profile["noise"]["boilerplate_pattern_count"], 1)

    def test_extract_spot_check_samples(self):
        markdown = "A" * 600 + "\n# Header\n" + "B" * 600 + "\n| X | Y |\n| 1 | 2 |\n" + "C" * 600
        samples = extract_spot_check_samples(markdown)
        self.assertTrue(len(samples["beginning_sample"]) > 0)
        self.assertTrue(len(samples["middle_sample"]) > 0)
        self.assertTrue(len(samples["structural_sample"]) > 0)
        self.assertIn("| X | Y |", samples["structural_sample"])

    def test_detect_result_overlap(self):
        profiles = [
            {"content": {"key_claims": ["Claim A", "Claim B"]}},
            {"content": {"key_claims": ["Claim A", "Claim C"]}},
            {"content": {"key_claims": ["Claim A", "Claim D"]}}
        ]
        res = detect_result_overlap(profiles)
        self.assertIn("Claim A", res["duplicated_claims"])
        self.assertLess(res["unique_claim_ratio"], 1.0)

    def test_is_profile_viable(self):
        viable = {"content": {"key_claims": ["Claim 1"]}, "structure": {"size": {"total_words": 100}}}
        unviable_empty = {"content": {"key_claims": []}, "structure": {"size": {"total_words": 10}}}
        unviable_err = {"content": {"key_claims": ["Error 404"], "content_completeness": "error_page"}, "structure": {"size": {"total_words": 100}}}
        self.assertTrue(is_profile_viable(viable))
        self.assertFalse(is_profile_viable(unviable_empty))
        self.assertFalse(is_profile_viable(unviable_err))

    def test_enforce_baseline_dimensions(self):
        # Empty rubric should get all 3 baselines
        empty_rubric = EvalRubric(dimensions=[])
        enforced_empty = enforce_baseline_dimensions(empty_rubric)
        self.assertEqual(len(enforced_empty.dimensions), 3)
        self.assertAlmostEqual(sum(d.weight for d in enforced_empty.dimensions), 1.0, places=2)

        # Rubric with only custom coverage axis should inject ranking and fidelity
        partial_rubric = EvalRubric(dimensions=[
            RubricDimension(name="accuracy_coverage", weight=1.0, criteria="Good content")
        ])
        enforced_partial = enforce_baseline_dimensions(partial_rubric)
        names = [d.name for d in enforced_partial.dimensions]
        self.assertIn("_baseline_ranking", names)
        self.assertIn("_baseline_fidelity", names)
        self.assertAlmostEqual(sum(d.weight for d in enforced_partial.dimensions), 1.0, places=2)

    def test_eval_result_convenience_properties_and_wrappers(self):
        dim_cov = DimensionEval(
            dimension_name="coverage_accuracy",
            weight=0.5,
            evidence_found=["Evidence 1"],
            criteria_checklist=[CriteriaCheck("Cond 1", "MET", "Ev")],
            contrastive_fail_triggered=False,
            contrastive_fail_explanation="",
            assigned_level="L5",
            level_justification="Perfect",
            score=0.95,
            reasoning="Excellent coverage"
        )
        dim_rank = DimensionEval(
            dimension_name="ranking_ordering",
            weight=0.3,
            evidence_found=[],
            criteria_checklist=[],
            contrastive_fail_triggered=False,
            contrastive_fail_explanation="",
            assigned_level="L4",
            level_justification="Good",
            score=0.75,
            reasoning="Good ranking"
        )
        dim_fid = DimensionEval(
            dimension_name="scrape_fidelity",
            weight=0.2,
            evidence_found=[],
            criteria_checklist=[],
            contrastive_fail_triggered=False,
            contrastive_fail_explanation="",
            assigned_level="L3",
            level_justification="Ok",
            score=0.55,
            reasoning="Fair scrape"
        )

        res = EvalResult(
            test_case_id="tc101",
            dimension_evals=[dim_cov, dim_rank, dim_fid],
            overall_score=0.81,
            document_profiles=[{"url": "https://example.com"}]
        )

        # Test properties
        self.assertEqual(res.coverage_score, 0.95)
        self.assertEqual(res.ranking_score, 0.75)
        self.assertEqual(res.fidelity_score, 0.55)

        # Test compatibility wrappers
        self.assertEqual(res.coverage.recall_score, 0.95)
        self.assertEqual(res.ranking.ndcg_at_5, 0.75)
        sq = res.scrape_quality.get("https://example.com")
        self.assertIsNotNone(sq)
        self.assertEqual(sq.overall_markdown_quality, 0.55)

        # Test serialization
        res_dict = res.to_dict()
        self.assertEqual(res_dict["test_case_id"], "tc101")
        self.assertEqual(len(res_dict["dimension_evals"]), 3)


if __name__ == "__main__":
    unittest.main()
