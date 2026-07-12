import pytest
from eval.test_generator import _jaccard_similarity, TestGenerator
from eval.improvement_agent import ImprovementAgent
from config import EvalConfig

class MockOpenRouterPool:
    pass

@pytest.fixture
def test_generator():
    config = EvalConfig()
    return TestGenerator(config, MockOpenRouterPool())

def test_jaccard_similarity():
    # Identical
    assert _jaccard_similarity("hello world", "Hello World") == 1.0
    # Completely disjoint
    assert _jaccard_similarity("apple orange", "banana grape") == 0.0
    # Overlap
    assert abs(_jaccard_similarity("hello world", "hello friend") - 1/3) < 0.01

def test_validate_generated_tc_contrastive_fail_copy(test_generator):
    tc_data = {
        "query": "test",
        "rubric": {
            "dimensions": [
                {
                    "name": "coverage",
                    "criteria": "Results contain specific numerical data.",
                    "contrastive_fail": "Results contain specific numerical data." # Copy
                }
            ]
        }
    }
    is_valid, warnings = test_generator._validate_generated_tc(tc_data)
    assert not is_valid
    assert any("too similar" in w for w in warnings)

def test_validate_generated_tc_contrastive_fail_short(test_generator):
    tc_data = {
        "query": "test",
        "rubric": {
            "dimensions": [
                {
                    "name": "coverage",
                    "criteria": "Results contain specific numerical data about population.",
                    "contrastive_fail": "It fails." # Too short
                }
            ]
        }
    }
    is_valid, warnings = test_generator._validate_generated_tc(tc_data)
    assert not is_valid
    assert any("too short" in w for w in warnings)

def test_validate_generated_tc_valid(test_generator):
    tc_data = {
        "query": "test",
        "rubric": {
            "dimensions": [
                {
                    "name": "coverage",
                    "criteria": "Results contain specific numerical data about population.",
                    "contrastive_fail": "Results fail if they provide generic geographic descriptions without citing actual demographic statistics or population counts."
                }
            ]
        }
    }
    is_valid, warnings = test_generator._validate_generated_tc(tc_data)
    assert is_valid
    assert not warnings
