from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path
from app.i18n.i18n_manager import tr

class DropZoneWidget(QFrame):
    files_dropped = Signal(list)
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel("📁")
        self.icon_label.setStyleSheet("font-size: 44px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(tr("dropzone.title", "Drag & Drop Images or Folders Here, or Click to Browse"))
        self.title_label.setStyleSheet("font-size: 15px; font-weight: 700; margin-top: 8px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle_label = QLabel(tr("dropzone.subtitle", "Supports WebP, AVIF, HEIC, JPG, PNG, TIFF, BMP"))
        self.subtitle_label.setStyleSheet("font-size: 12px; opacity: 0.7;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)

    def retranslate_ui(self):
        self.title_label.setText(tr("dropzone.title", "Drag & Drop Images or Folders Here, or Click to Browse"))
        self.subtitle_label.setText(tr("dropzone.subtitle", "Supports WebP, AVIF, HEIC, JPG, PNG, TIFF, BMP"))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        paths = [Path(url.toLocalFile()) for url in urls if url.isLocalFile()]
        if paths:
            self.files_dropped.emit(paths)
