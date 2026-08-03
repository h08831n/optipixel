from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from PySide6.QtCore import Qt

class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-size: 13px; color: #4A5568;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                text-align: center;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: #3357C0;
                border-radius: 5px;
            }
        """)

        self.count_label = QLabel("0 / 0")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_label.setStyleSheet("font-size: 12px; color: #718096;")

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.status_label)
        sub_layout.addWidget(self.count_label)

        layout.addLayout(sub_layout)
        layout.addWidget(self.progress_bar)

    def update_progress(self, current: int, total: int, current_file: str = ""):
        if total > 0:
            pct = int((current / total) * 100)
            self.progress_bar.setValue(pct)
            self.count_label.setText(f"{current} / {total}")
        if current_file:
            self.status_label.setText(f"Processing: {current_file}")
