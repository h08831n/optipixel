import os
from pathlib import Path
from typing import List, Set, Generator, Optional
from app.config.constants import SUPPORTED_INPUT_EXTENSIONS
from app.core.image_info import ImageInfo

IGNORED_EXTENSIONS = {".tmp", ".part", ".crdownload", ".db", ".DS_Store"}

class ImageScanner:
    def __init__(self, allowed_extensions: Set[str] = SUPPORTED_INPUT_EXTENSIONS):
        self.allowed_extensions = {ext.lower() for ext in allowed_extensions}

    def is_valid_image_file(self, file_path: Path) -> bool:
        if not file_path.is_file():
            return False
        if file_path.suffix.lower() in IGNORED_EXTENSIONS:
            return False
        return file_path.suffix.lower() in self.allowed_extensions

    def scan_file(self, file_path: Path) -> Optional[ImageInfo]:
        if self.is_valid_image_file(file_path):
            return ImageInfo.extract(file_path)
        return None

    def scan_directory(self, dir_path: Path, recursive: bool = True) -> Generator[ImageInfo, None, None]:
        if not dir_path.is_dir():
            return

        if recursive:
            for root, _, files in os.walk(dir_path):
                for f in files:
                    p = Path(root) / f
                    if self.is_valid_image_file(p):
                        yield ImageInfo.extract(p)
        else:
            for p in dir_path.iterdir():
                if self.is_valid_image_file(p):
                    yield ImageInfo.extract(p)

    def scan_paths(self, paths: List[Path], recursive: bool = True) -> List[ImageInfo]:
        results: List[ImageInfo] = []
        for p in paths:
            if p.is_file():
                info = self.scan_file(p)
                if info:
                    results.append(info)
            elif p.is_dir():
                results.extend(self.scan_directory(p, recursive=recursive))
        return results
