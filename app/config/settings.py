import json
from pathlib import Path
from .constants import SETTINGS_FILE
from .defaults import DEFAULT_SETTINGS

class AppSettings:
    def __init__(self, settings_path: Path = SETTINGS_FILE):
        self.settings_path = settings_path
        self.data = self._load()

    def _load(self) -> dict:
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    # Deep merge with default settings
                    merged = json.loads(json.dumps(DEFAULT_SETTINGS))
                    for section, values in user_data.items():
                        if section in merged and isinstance(values, dict):
                            merged[section].update(values)
                        else:
                            merged[section] = values
                    return merged
            except Exception:
                return json.loads(json.dumps(DEFAULT_SETTINGS))
        return json.loads(json.dumps(DEFAULT_SETTINGS))

    def save(self):
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, section: str, key: str, default=None):
        return self.data.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.save()
