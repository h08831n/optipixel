from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from app.services.history_service import HistoryService
from app.i18n.i18n_manager import tr, I18nManager

class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_service = HistoryService()
        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        top_bar = QHBoxLayout()
        self.title = QLabel(tr("history.title", "Optimization Job History"))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.btn_refresh = QPushButton(tr("history.refresh", "Refresh"))
        self.btn_refresh.clicked.connect(self.load_history)

        self.btn_clear = QPushButton(tr("history.clear", "Clear History"))
        self.btn_clear.clicked.connect(self.clear_history)

        top_bar.addWidget(self.title)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_refresh)
        top_bar.addWidget(self.btn_clear)
        layout.addLayout(top_bar)

        self.table = QTableWidget(0, 6)
        self.retranslate_headers()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.load_history()

    def retranslate_headers(self):
        self.table.setHorizontalHeaderLabels([
            tr("history.col_id", "ID"),
            tr("history.col_timestamp", "Timestamp"),
            tr("history.col_operation", "Operation"),
            tr("history.col_files", "Processed Files"),
            tr("history.col_saved", "Saved Space"),
            tr("history.col_duration", "Duration")
        ])

    def retranslate_ui(self):
        self.title.setText(tr("history.title", "Optimization Job History"))
        self.btn_refresh.setText(tr("history.refresh", "Refresh"))
        self.btn_clear.setText(tr("history.clear", "Clear History"))
        self.retranslate_headers()

    def load_history(self):
        history = self.history_service.get_history()
        self.table.setRowCount(0)

        for item in history:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("timestamp", "")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("operation", "Optimize")))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get("files_processed", 0))))
            self.table.setItem(row, 4, QTableWidgetItem(item.get("saved_space_str", "0 B")))
            self.table.setItem(row, 5, QTableWidgetItem(item.get("duration_str", "0s")))

    def clear_history(self):
        self.history_service.clear_history()
        self.load_history()
