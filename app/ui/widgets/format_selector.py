from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel
from typing import Dict, List
from app.core.formats import ImageFormat

class FormatSelectorWidget(QWidget):
    def __init__(self, supported_formats: Dict[str, bool], parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Target Format:"))
        self.combo = QComboBox()

        for fmt_str in ["WEBP", "AVIF", "JPEG", "PNG", "TIFF", "BMP", "ORIGINAL"]:
            if fmt_str == "ORIGINAL" or supported_formats.get(fmt_str, True):
                self.combo.addItem(fmt_str)

        layout.addWidget(self.combo)

    def current_format(self) -> ImageFormat:
        val = self.combo.currentText()
        if val == "ORIGINAL":
            return ImageFormat.ORIGINAL
        return ImageFormat.from_extension(val.lower())
