import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from app.config.constants import BACKUP_DIR

class BackupManager:
    def __init__(self, backup_dir: Path = BACKUP_DIR, strategy: str = "timestamped"):
        self.backup_dir = backup_dir
        self.strategy = strategy
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, source_path: Path) -> Optional[Path]:
        if not source_path.exists():
            return None

        try:
            if self.strategy == "suffix":
                backup_path = source_path.with_suffix(source_path.suffix + ".backup")
                shutil.copy2(source_path, backup_path)
                return backup_path
            else:
                # Timestamped subfolder
                today_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                target_dir = self.backup_dir / today_str
                target_dir.mkdir(parents=True, exist_ok=True)
                backup_path = target_dir / source_path.name
                shutil.copy2(source_path, backup_path)
                return backup_path
        except Exception as e:
            print(f"Failed to create backup for {source_path}: {e}")
            return None
