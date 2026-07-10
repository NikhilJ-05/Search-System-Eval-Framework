import logging
import json
import os
import shutil
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)  # Firecrawl root

@dataclass
class RunMetadata:
    run_id: str
    status: str
    overall_score: float = 0.0
    tc_count: int = 0
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration_s: float = 0.0

    def to_dict(self):
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


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

    def write_run_atomic(self, run_id: str, payload: dict):
        """Write run.json atomically to prevent partial reads."""
        run_dir = os.path.join(self.runs_dir, run_id)
        os.makedirs(run_dir, exist_ok=True)
        path = os.path.join(run_dir, "run.json")
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        os.replace(tmp_path, path)

    def write_run_metadata(self, run_id: str, meta: RunMetadata):
        """Write a small meta.json file alongside run.json for fast listing."""
        run_dir = os.path.join(self.runs_dir, run_id)
        os.makedirs(run_dir, exist_ok=True)
        path = os.path.join(run_dir, "meta.json")
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(meta.to_dict(), f, indent=2)
        os.replace(tmp_path, path)

    def get_run_status(self, run_id: str) -> Optional[dict]:
        """Read only the meta.json file to get the run status efficiently."""
        meta_path = os.path.join(self.runs_dir, run_id, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def list_runs(self) -> list:
        # Kept for backward compatibility, returns list of run_ids
        runs = set()
        if os.path.exists(self.runs_dir):
            for entry in os.listdir(self.runs_dir):
                full_path = os.path.join(self.runs_dir, entry)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "run.json")):
                    runs.add(entry)
                elif entry.endswith('.json'):
                    runs.add(entry[:-5])
        return sorted(list(runs), reverse=True)

    def list_runs_with_meta(self) -> List[dict]:
        """Returns a list of metadata dicts for all runs."""
        runs_meta = []
        if os.path.exists(self.runs_dir):
            for entry in os.listdir(self.runs_dir):
                full_path = os.path.join(self.runs_dir, entry)
                if os.path.isdir(full_path):
                    meta = self.get_run_status(entry)
                    if meta:
                        runs_meta.append(meta)
                    elif os.path.exists(os.path.join(full_path, "run.json")):
                        # Fallback if meta.json doesn't exist
                        runs_meta.append({"run_id": entry, "status": "unknown"})
                elif entry.endswith('.json'):
                    run_id = entry[:-5]
                    runs_meta.append({"run_id": run_id, "status": "unknown"})
        # Sort by run_id descending (newest first)
        return sorted(runs_meta, key=lambda x: x.get("run_id", ""), reverse=True)
