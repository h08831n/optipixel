from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent
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

        self.icon_label = QLabel("📥")
        self.icon_label.setStyleSheet("font-size: 48px;")
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

    def animate_icon_bounce(self):
        self.anim = QPropertyAnimation(self.icon_label, b"pos")
        orig_pos = self.icon_label.pos()
        self.anim.setDuration(300)
        self.anim.setStartValue(orig_pos)
        self.anim.setKeyValueAt(0.5, orig_pos + Qt.QPoint(0, -10) if hasattr(Qt, "QPoint") else orig_pos)
        self.anim.setEndValue(orig_pos)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        urls = event.mimeData().urls()
        paths = [Path(url.toLocalFile()) for url in urls if url.isLocalFile()]
        if paths:
            self.files_dropped.emit(paths)

