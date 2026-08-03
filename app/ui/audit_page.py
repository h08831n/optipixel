from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from pathlib import Path
from app.core.scanner import ImageScanner
from app.ui.widgets.stats_card import StatsCardWidget
from app.utils.size_utils import format_size

class AuditPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanner = ImageScanner()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("SEO & Web Performance Image Audit (Read-Only)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D3748;")
        layout.addWidget(title)

        top_bar = QHBoxLayout()
        self.btn_select = QPushButton("Scan Directory for Audit...")
        self.btn_select.clicked.connect(self.select_directory)
        top_bar.addWidget(self.btn_select)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        stats_layout = QHBoxLayout()
        self.card_total = StatsCardWidget("Total Scanned", "0")
        self.card_size = StatsCardWidget("Total Volume", "0 B")
        self.card_heavy = StatsCardWidget("Over 400 KB", "0", "Needs Optimization")
        self.card_huge = StatsCardWidget("Over 1 MB", "0", "Critical Issue")

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_size)
        stats_layout.addWidget(self.card_heavy)
        stats_layout.addWidget(self.card_huge)
        layout.addLayout(stats_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Filename", "Path", "Format", "Size", "Audit Recommendation"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Audit")
        if not folder:
            return

        images = self.scanner.scan_paths([Path(folder)], recursive=True)
        self.table.setRowCount(0)

        total_bytes = 0
        heavy_count = 0
        huge_count = 0

        for img in images:
            total_bytes += img.file_size_bytes
            rec = "OK - Optimized"

            if img.file_size_kb > 1024:
                huge_count += 1
                rec = "CRITICAL: Convert to WebP & Resize"
            elif img.file_size_kb > 400:
                heavy_count += 1
                rec = "WARNING: Convert to WebP / Compress"

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(img.file_path.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(img.file_path)))
            self.table.setItem(row, 2, QTableWidgetItem(img.format.value))
            self.table.setItem(row, 3, QTableWidgetItem(format_size(img.file_size_bytes)))
            self.table.setItem(row, 4, QTableWidgetItem(rec))

        self.card_total.set_value(str(len(images)))
        self.card_size.set_value(format_size(total_bytes))
        self.card_heavy.set_value(str(heavy_count))
        self.card_huge.set_value(str(huge_count))
