from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from app.core.scanner import ImageScanner
from app.ui.widgets.stats_card import StatsCardWidget
from app.utils.size_utils import format_size
from app.i18n.i18n_manager import tr, I18nManager

class AuditPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanner = ImageScanner()
        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.title = QLabel(tr("audit.title", "SEO & Web Performance Image Audit (Read-Only)"))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        top_bar = QHBoxLayout()
        self.btn_select = QPushButton(tr("audit.select_btn", "Scan Directory for Audit..."))
        self.btn_select.clicked.connect(self.select_directory)
        top_bar.addWidget(self.btn_select)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        self.card_total = StatsCardWidget(tr("audit.scanned", "Total Scanned"), "0")
        self.card_size = StatsCardWidget(tr("audit.volume", "Total Volume"), "0 B")
        self.card_heavy = StatsCardWidget(tr("audit.heavy", "Over 400 KB"), "0", tr("audit.needs_opt", "Needs Optimization"))
        self.card_huge = StatsCardWidget(tr("audit.huge", "Over 1 MB"), "0", tr("audit.critical", "Critical Issue"))

        stats_layout.addWidget(self.card_total)
        stats_layout.addWidget(self.card_size)
        stats_layout.addWidget(self.card_heavy)
        stats_layout.addWidget(self.card_huge)
        layout.addLayout(stats_layout)

        self.table = QTableWidget(0, 5)
        self.retranslate_headers()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    def retranslate_headers(self):
        self.table.setHorizontalHeaderLabels([
            tr("header.filename", "Filename"),
            tr("header.path", "Path"),
            tr("header.format", "Format"),
            tr("header.size", "Size"),
            tr("audit.recommendation", "Audit Recommendation")
        ])

    def retranslate_ui(self):
        self.title.setText(tr("audit.title", "SEO & Web Performance Image Audit (Read-Only)"))
        self.btn_select.setText(tr("audit.select_btn", "Scan Directory for Audit..."))
        self.card_total.set_title(tr("audit.scanned", "Total Scanned"))
        self.card_size.set_title(tr("audit.volume", "Total Volume"))
        self.card_heavy.set_title(tr("audit.heavy", "Over 400 KB"))
        self.card_huge.set_title(tr("audit.huge", "Over 1 MB"))
        self.retranslate_headers()

    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, tr("title.select_folder", "Select Folder to Audit"))
        if not folder:
            return

        images = self.scanner.scan_paths([Path(folder)], recursive=True)
        self.table.setRowCount(0)

        total_bytes = 0
        heavy_count = 0
        huge_count = 0

        for img in images:
            total_bytes += img.file_size_bytes
            rec = tr("audit.rec_ok", "OK - Optimized")

            if img.file_size_kb > 1024:
                huge_count += 1
                rec = tr("audit.rec_critical", "CRITICAL: Convert to WebP & Resize")
            elif img.file_size_kb > 400:
                heavy_count += 1
                rec = tr("audit.rec_warning", "WARNING: Convert to WebP / Compress")

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
