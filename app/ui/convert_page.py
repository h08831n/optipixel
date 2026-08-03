from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from app.services.imagemagick_service import ImageMagickService
from app.ui.widgets.drop_zone import DropZoneWidget

class ConvertPage(QWidget):
    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        layout = QVBoxLayout(self)

        title = QLabel("Format Converter Matrix")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D3748;")
        layout.addWidget(title)

        subtitle = QLabel("Convert batch images between WebP, AVIF, JPEG, PNG, TIFF, HEIC, BMP")
        subtitle.setStyleSheet("font-size: 13px; color: #718096;")
        layout.addWidget(subtitle)

        drop_zone = DropZoneWidget()
        layout.addWidget(drop_zone)

        layout.addStretch()
