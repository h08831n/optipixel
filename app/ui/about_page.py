from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from app.config.constants import APP_NAME, APP_TAGLINE, APP_VERSION, APP_PUBLISHER, APP_WEBSITE

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel(APP_NAME)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #3357C0;")

        tagline = QLabel(APP_TAGLINE)
        tagline.setStyleSheet("font-size: 16px; color: #4A5568;")

        ver = QLabel(f"Version {APP_VERSION}")
        ver.setStyleSheet("font-size: 14px; color: #718096;")

        pub = QLabel(f"Published by {APP_PUBLISHER}")
        pub.setStyleSheet("font-size: 13px; color: #A0AEC0;")

        btn_web = QPushButton("Visit Website (ahaninja.com)")
        btn_web.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(APP_WEBSITE)))

        layout.addWidget(title)
        layout.addWidget(tagline)
        layout.addWidget(ver)
        layout.addWidget(pub)
        layout.addSpacing(20)
        layout.addWidget(btn_web)
