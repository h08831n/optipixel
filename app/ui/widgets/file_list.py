from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from app.core.image_info import ImageInfo
from app.utils.size_utils import format_size
from app.i18n.i18n_manager import tr

class FileListWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 5, parent)
        self.retranslate_headers()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def retranslate_headers(self):
        self.setHorizontalHeaderLabels([
            tr("header.filename", "Filename"),
            tr("header.path", "Path"),
            tr("header.dimensions", "Dimensions"),
            tr("header.size", "Size"),
            tr("header.format", "Format")
        ])

    def add_image(self, info: ImageInfo):
        row = self.rowCount()
        self.insertRow(row)

        self.setItem(row, 0, QTableWidgetItem(info.file_path.name))
        self.setItem(row, 1, QTableWidgetItem(str(info.file_path)))
        dim_str = f"{info.width}x{info.height}" if info.width else "Unknown"
        self.setItem(row, 2, QTableWidgetItem(dim_str))
        self.setItem(row, 3, QTableWidgetItem(format_size(info.file_size_bytes)))
        self.setItem(row, 4, QTableWidgetItem(info.format.value))

    def clear_files(self):
        self.setRowCount(0)
