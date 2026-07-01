import logging
import os
import json
from typing import List
import dataclasses
from models.eval_result import EvalResult

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

class RegressionDetector:
    def __init__(self):
        self.runs_dir = os.path.join(APP_DIR, "outputs", "runs")
        os.makedirs(self.runs_dir, exist_ok=True)

    def detect(self, current_run_id: str, current_results: List[EvalResult]) -> dict:
        logger.info("Running regression detection...")
        
        # NOTE: the orchestrator writes the full run payload — skip duplicating it here.
        # Find previous run (both subdirectories containing run.json and legacy .json files)
        runs = []
        if os.path.exists(self.runs_dir):
            for entry in os.listdir(self.runs_dir):
                if entry == current_run_id or entry == f"{current_run_id}.json":
                    continue
                full_path = os.path.join(self.runs_dir, entry)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "run.json")):
                    runs.append((entry, os.path.join(full_path, "run.json")))
                elif entry.endswith('.json'):
                    runs.append((entry[:-5], full_path))
        runs.sort(key=lambda x: x[0])
        if not runs:
            return {"status": "first_run", "trend": "No previous data"}
            
        prev_run_id, prev_file_path = runs[-1]
        try:
            with open(prev_file_path, 'r', encoding='utf-8') as f:
                prev_data = json.load(f)
                
            prev_results = prev_data.get("eval_results", prev_data) if isinstance(prev_data, dict) else prev_data
            if not isinstance(prev_results, list) or not prev_results:
                return {"status": "first_run", "trend": "No previous evaluation scores"}

            curr_avg = sum(e.overall_score for e in current_results) / max(1, len(current_results))
            prev_avg = sum(e.get("overall_score", 0) if isinstance(e, dict) else getattr(e, "overall_score", 0) for e in prev_results) / max(1, len(prev_results))
            
            diff = curr_avg - prev_avg
            if diff > 0.05:
                trend = "Significant Improvement 🚀"
            elif diff < -0.05:
                trend = "Regression Detected ⚠️"
            else:
                trend = "Stable ➡️"
                
            return {
                "status": "compared",
                "trend": trend,
                "diff": diff,
                "prev_run": prev_run_id
            }
        except Exception as e:
            logger.error(f"Failed to compare with previous run: {e}")
            return {"status": "error", "trend": "Comparison failed"}
