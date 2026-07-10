import json
import os
import random
import logging
from typing import List, Dict, Any, Optional
from models.test_case import TestCase

logger = logging.getLogger(__name__)

class TestCaseHistory:
    def __init__(self, history_file: Optional[str] = None):
        if history_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.history_file = os.path.join(base_dir, "outputs", "data", "test_case_history.jsonl")
        else:
            self.history_file = history_file
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        logger.info(f"Initialized TestCaseHistory at {self.history_file}")

    def append(self, tc: TestCase) -> None:
        """Append a TestCase to the history file as a single line JSON."""
        import dataclasses
        try:
            tc_dict = dataclasses.asdict(tc)
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(tc_dict) + "\n")
            logger.debug(f"Appended test case {tc.id} ({tc.query}) to history.")
        except Exception as e:
            logger.error(f"Failed to append test case to history: {e}")

    def load_all(self) -> List[TestCase]:
        """Load all test cases from history."""
        if not os.path.exists(self.history_file):
            return []
        
        cases = []
        with open(self.history_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    cases.append(TestCase.from_dict(data))
                except Exception as e:
                    logger.warning(f"Failed to parse history line: {e}")
                    pass
        return cases

    def sample(self, n: int) -> List[TestCase]:
        """
        Sample n test cases from history.
        Stratified approach: always include the last 5 for recency,
        then sample the remaining from older history for diversity.
        """
        all_cases = self.load_all()
        if not all_cases:
            return []
            
        if len(all_cases) <= n:
            return all_cases
            
        RECENT_N = 5
        recent = all_cases[-RECENT_N:]
        older = all_cases[:-RECENT_N]
        
        needed = n - len(recent)
        if needed <= 0:
            return random.sample(recent, n)
            
        sampled_older = random.sample(older, min(needed, len(older)))
        return recent + sampled_older

    def all_queries(self) -> List[str]:
        """Get all queries present in the history."""
        return [tc.query for tc in self.load_all()]

    def count(self) -> int:
        """Return the number of stored test cases."""
        if not os.path.exists(self.history_file):
            return 0
        count = 0
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        count += 1
        except Exception:
            return 0
        return count
