from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from app.i18n.i18n_manager import tr

class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.status_label = QLabel(tr("status.ready", "Ready"))
        self.status_label.setStyleSheet("font-size: 13px; font-weight: 600;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.count_label = QLabel("0 / 0")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_label.setStyleSheet("font-size: 12px; font-weight: 600; opacity: 0.8;")

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.status_label)
        sub_layout.addWidget(self.count_label)

        layout.addLayout(sub_layout)
        layout.addWidget(self.progress_bar)

        self._anim = None

    def retranslate_ui(self):
        if self.progress_bar.value() == 0:
            self.status_label.setText(tr("status.ready", "Ready"))

    def update_progress(self, current: int, total: int, current_file: str = ""):
        if total > 0:
            target_val = int((current / total) * 100)
            if target_val != self.progress_bar.value():
                self._anim = QPropertyAnimation(self.progress_bar, b"value")
                self._anim.setDuration(250)
                self._anim.setStartValue(self.progress_bar.value())
                self._anim.setEndValue(target_val)
                self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
                self._anim.start()
            self.count_label.setText(f"{current} / {total}")
        if current_file:
            proc_text = tr("status.processing", "Processing:")
            self.status_label.setText(f"{proc_text} {current_file}")
        if current == total and total > 0:
            self.status_label.setText(f"✨ {tr('status.completed', 'Completed!')}")

