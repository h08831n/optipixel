from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class StatsCardWidget(QFrame):
    def __init__(self, title: str, value: str = "0", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            StatsCardWidget {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(self)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 12px; color: #718096; font-weight: 500;")

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 20px; color: #1A202C; font-weight: bold;")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet("font-size: 11px; color: #A0AEC0;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    def set_value(self, value: str, subtitle: str = ""):
        self.value_label.setText(value)
        if subtitle:
            self.subtitle_label.setText(subtitle)
