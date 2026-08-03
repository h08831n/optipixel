import os
from pathlib import Path

def ensure_directory(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)

def safe_delete(file_path: Path) -> bool:
    try:
        if file_path.exists():
            file_path.unlink()
            return True
    except Exception:
        pass
    return False
