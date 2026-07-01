import logging
import json
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

class PipelineStore:
    def __init__(self):
        self.runs_dir = os.path.join(APP_DIR, "outputs", "runs")
        os.makedirs(self.runs_dir, exist_ok=True)

    def _get_full_run(self, run_id: str):
        """Return the full run payload dict, or None if not found."""
        path_new = os.path.join(self.runs_dir, run_id, "run.json")
        path_old = os.path.join(self.runs_dir, f"{run_id}.json")
        if os.path.exists(path_new):
            with open(path_new, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif os.path.exists(path_old):
            with open(path_old, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_run(self, run_id: str) -> list:
        data = self._get_full_run(run_id)
        if data is None:
            return []
        # Return the eval_results array directly for legacy callers
        return data.get("eval_results", data) if isinstance(data, dict) else data

    def list_runs(self) -> list:
        runs = set()
        if os.path.exists(self.runs_dir):
            for entry in os.listdir(self.runs_dir):
                full_path = os.path.join(self.runs_dir, entry)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "run.json")):
                    runs.add(entry)
                elif entry.endswith('.json'):
                    runs.add(entry[:-5])
        return sorted(list(runs), reverse=True)
