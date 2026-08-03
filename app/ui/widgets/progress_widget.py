from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from PySide6.QtCore import Qt
from app.i18n.i18n_manager import tr

class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.status_label = QLabel(tr("status.ready", "Ready"))
        self.status_label.setStyleSheet("font-size: 13px; font-weight: 500;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.count_label = QLabel("0 / 0")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_label.setStyleSheet("font-size: 12px; opacity: 0.8;")

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.status_label)
        sub_layout.addWidget(self.count_label)

        layout.addLayout(sub_layout)
        layout.addWidget(self.progress_bar)

    def retranslate_ui(self):
        if self.progress_bar.value() == 0:
            self.status_label.setText(tr("status.ready", "Ready"))

    def update_progress(self, current: int, total: int, current_file: str = ""):
        if total > 0:
            pct = int((current / total) * 100)
            self.progress_bar.setValue(pct)
            self.count_label.setText(f"{current} / {total}")
        if current_file:
            proc_text = tr("status.processing", "Processing:")
            self.status_label.setText(f"{proc_text} {current_file}")
        if current == total and total > 0:
            self.status_label.setText(tr("status.completed", "Completed!"))
