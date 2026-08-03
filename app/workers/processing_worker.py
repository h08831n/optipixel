from PySide6.QtCore import QRunnable, QObject, Signal
from pathlib import Path
from typing import Dict, Any
from app.core.processor import ImageProcessor, ProcessingResult
from app.core.image_info import ImageInfo
from app.core.formats import ImageFormat
from app.core.output_manager import OutputManager

class ProcessingWorkerSignals(QObject):
    started = Signal(str)
    finished = Signal(object)  # ProcessingResult
    error = Signal(str, str)

class ProcessingWorker(QRunnable):
    def __init__(
        self,
        processor: ImageProcessor,
        image_info: ImageInfo,
        target_format: ImageFormat,
        settings: Dict[str, Any],
        output_manager: OutputManager
    ):
        super().__init__()
        self.processor = processor
        self.image_info = image_info
        self.target_format = target_format
        self.settings = settings
        self.output_manager = output_manager
        self.signals = ProcessingWorkerSignals()

    def run(self):
        self.signals.started.emit(str(self.image_info.file_path))
        try:
            result = self.processor.process_single(
                image_info=self.image_info,
                target_format=self.target_format,
                settings=self.settings,
                output_manager=self.output_manager
            )
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(self.image_info.file_path), str(e))
