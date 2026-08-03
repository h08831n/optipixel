from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from app.services.history_service import HistoryService

class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_service = HistoryService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        title = QLabel("Optimization Job History")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D3748;")

        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.load_history)

        btn_clear = QPushButton("Clear History")
        btn_clear.clicked.connect(self.clear_history)

        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(btn_refresh)
        top_bar.addWidget(btn_clear)
        layout.addLayout(top_bar)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Timestamp", "Operation", "Processed Files", "Saved Space", "Duration"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.load_history()

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
