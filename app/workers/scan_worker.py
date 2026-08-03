from PySide6.QtCore import QRunnable, QObject, Signal
from pathlib import Path
from typing import List
from app.core.scanner import ImageScanner
from app.core.image_info import ImageInfo

class ScanWorkerSignals(QObject):
    file_found = Signal(object)  # ImageInfo
    finished = Signal(list)     # List[ImageInfo]
    progress = Signal(int)

class ScanWorker(QRunnable):
    def __init__(self, paths: List[Path], recursive: bool = True):
        super().__init__()
        self.paths = paths
        self.recursive = recursive
        self.signals = ScanWorkerSignals()
        self.scanner = ImageScanner()

    def run(self):
        found_images = []
        for path in self.paths:
            if path.is_file():
                info = self.scanner.scan_file(path)
                if info:
                    found_images.append(info)
                    self.signals.file_found.emit(info)
            elif path.is_dir():
                for info in self.scanner.scan_directory(path, recursive=self.recursive):
                    found_images.append(info)
                    self.signals.file_found.emit(info)
        self.signals.finished.emit(found_images)
