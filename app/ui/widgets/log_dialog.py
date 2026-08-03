import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from app.utils.logging_utils import get_log_buffer, LOG_FILE, get_logger
from app.i18n.i18n_manager import tr

logger = get_logger()

class LogViewerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("log.title", "OptiPixel Developer & Debug Logs"))
        self.resize(750, 500)
        self.init_ui()

        # Timer to auto-refresh live log buffer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Header bar
        header_layout = QHBoxLayout()
        lbl_info = QLabel(f"<b>Log File:</b> {LOG_FILE}")
        lbl_info.setWordWrap(True)
        header_layout.addWidget(lbl_info)
        layout.addLayout(header_layout)

        # Log Text Box
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.txt_logs.setFont(font)
        self.txt_logs.setStyleSheet("""
            QTextEdit {
                background-color: #0F172A;
                color: #38BDF8;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.txt_logs)

        # Buttons bar
        btn_layout = QHBoxLayout()

        btn_refresh = QPushButton(tr("log.refresh", "Refresh Logs"))
        btn_refresh.clicked.connect(self.refresh_logs)
        btn_layout.addWidget(btn_refresh)

        btn_copy = QPushButton(tr("log.copy", "Copy to Clipboard"))
        btn_copy.clicked.connect(self.copy_logs)
        btn_layout.addWidget(btn_copy)

        btn_open_file = QPushButton(tr("log.open_file", "Open Log File"))
        btn_open_file.clicked.connect(self.open_log_file)
        btn_layout.addWidget(btn_open_file)

        btn_clear = QPushButton(tr("log.clear", "Clear Buffer"))
        btn_clear.clicked.connect(self.clear_logs)
        btn_layout.addWidget(btn_clear)

        btn_layout.addStretch()

        btn_close = QPushButton(tr("common.close", "Close"))
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

        self.refresh_logs()

    def refresh_logs(self):
        buf = get_log_buffer()
        logs_text = buf.get_logs()
        if not logs_text and LOG_FILE.exists():
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs_text = f.read()[-20000:] # last 20k chars
            except Exception as e:
                logs_text = f"Failed to read log file: {e}"

        if not logs_text:
            logs_text = "[No logs recorded yet]"

        # Preserve scroll if user is scrolled up
        scrollbar = self.txt_logs.verticalScrollBar()
        at_bottom = scrollbar.value() >= (scrollbar.maximum() - 20)
        
        self.txt_logs.setPlainText(logs_text)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def copy_logs(self):
        text = self.txt_logs.toPlainText()
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, tr("log.title", "Debug Logs"), tr("log.copied", "Logs copied to clipboard."))

    def open_log_file(self):
        if not LOG_FILE.exists():
            LOG_FILE.touch()
        try:
            import subprocess
            if os.name == 'nt':
                os.startfile(str(LOG_FILE))
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', str(LOG_FILE)])
        except Exception as e:
            QMessageBox.warning(self, "Log File", f"Could not open log file directly:\n{e}\n\nPath: {LOG_FILE}")

    def clear_logs(self):
        get_log_buffer().clear()
        self.refresh_logs()
