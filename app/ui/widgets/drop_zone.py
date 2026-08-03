from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path

class DropZoneWidget(QFrame):
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            DropZoneWidget {
                border: 2px dashed #3357C0;
                border-radius: 12px;
                background-color: rgba(51, 87, 192, 0.04);
                padding: 24px;
            }
            DropZoneWidget:hover {
                background-color: rgba(51, 87, 192, 0.08);
                border-color: #26429A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel("📁")
        self.icon_label.setStyleSheet("font-size: 48px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Drag & Drop Images or Folders Here")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2D3748;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle_label = QLabel("Supports WebP, AVIF, HEIC, JPG, PNG, TIFF, BMP")
        self.subtitle_label.setStyleSheet("font-size: 13px; color: #718096;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        paths = [Path(url.toLocalFile()) for url in urls if url.isLocalFile()]
        if paths:
            self.files_dropped.emit(paths)
