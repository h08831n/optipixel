import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from app.config.constants import HISTORY_FILE

class HistoryService:
    def __init__(self, history_file: Path = HISTORY_FILE):
        self.history_file = history_file

    def get_history(self) -> List[Dict[str, Any]]:
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def add_job_entry(self, job_summary: Dict[str, Any]):
        history = self.get_history()
        entry = {
            "id": len(history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **job_summary
        }
        history.insert(0, entry)  # Prepend newest
        # Keep last 100 entries
        history = history[:100]

        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save history: {e}")

    def clear_history(self):
        try:
            if self.history_file.exists():
                self.history_file.unlink()
        except Exception as e:
            print(f"Failed to clear history: {e}")
