import os
from pathlib import Path

def sanitize_path(path_str: str) -> Path:
    return Path(path_str.strip().strip('"').strip("'"))

def is_subpath(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False
