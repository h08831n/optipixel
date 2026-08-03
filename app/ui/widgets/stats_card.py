from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class StatsCardWidget(QFrame):
    def __init__(self, title: str, value: str = "0", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("StatsCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("Title")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("Value")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("Subtitle")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_value(self, value: str, subtitle: str = ""):
        self.value_label.setText(value)
        if subtitle:
            self.subtitle_label.setText(subtitle)
