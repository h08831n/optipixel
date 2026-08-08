from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from app.core.image_info import ImageInfo
from app.core.processor import ProcessingResult
from app.utils.size_utils import format_size
from app.i18n.i18n_manager import tr

class FileListWidget(QTableWidget):
    STATUS_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(0, 6, parent)
        self.retranslate_headers()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def retranslate_headers(self):
        self.setHorizontalHeaderLabels([
            tr("header.filename", "Filename"),
            tr("header.path", "Path"),
            tr("header.dimensions", "Dimensions"),
            tr("header.size", "Size"),
            tr("header.format", "Format"),
            tr("header.status", "Status")
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

        status_item = QTableWidgetItem(f"⏳ {tr('status.pending', 'Pending')}")
        status_item.setData(Qt.ItemDataRole.UserRole, str(info.file_path))
        status_item.setData(self.STATUS_ROLE, "pending")
        self._apply_status_style(status_item, "pending")
        self.setItem(row, 5, status_item)

    def update_result(self, result: ProcessingResult):
        for row in range(self.rowCount()):
            path_item = self.item(row, 1)
            if path_item and path_item.text() == str(result.source_path):
                # Update Size column
                if result.status in ("optimized", "converted") and result.new_size_bytes > 0:
                    orig_str = format_size(result.original_size_bytes)
                    new_str = format_size(result.new_size_bytes)
                    pct = result.reduction_percentage
                    size_text = f"{orig_str} → {new_str} (-{pct:.1f}%)"
                    size_item = QTableWidgetItem(size_text)
                    size_item.setForeground(QColor("#15803D"))  # Green text for size reduction
                    self.setItem(row, 3, size_item)

                # Update Dimensions if changed
                if result.width > 0 and result.height > 0:
                    self.setItem(row, 2, QTableWidgetItem(f"{result.width}x{result.height}"))

                # Update Status column
                status_text = ""
                if result.status == "optimized":
                    status_text = f"✅ {tr('status.optimized', 'Optimized')}"
                elif result.status == "converted":
                    status_text = f"✅ {tr('status.converted', 'Converted')}"
                elif result.status == "skipped":
                    status_text = f"⏭️ {tr('status.skipped', 'Skipped')}"
                else:
                    status_text = f"❌ {tr('status.failed', 'Failed')}"

                status_item = QTableWidgetItem(status_text)
                status_item.setToolTip(result.message)
                status_item.setData(Qt.ItemDataRole.UserRole, str(result.source_path))
                status_item.setData(self.STATUS_ROLE, result.status)
                self._apply_status_style(status_item, result.status)
                self.setItem(row, 5, status_item)
                break

    def _apply_status_style(self, item: QTableWidgetItem, status: str):
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        if status in ("optimized", "converted"):
            item.setBackground(QColor("#DCFCE7"))  # Light Green background
            item.setForeground(QColor("#15803D"))  # Dark Green text
        elif status == "failed":
            item.setBackground(QColor("#FEE2E2"))  # Light Red background
            item.setForeground(QColor("#B91C1C"))  # Dark Red text
        elif status == "skipped":
            item.setBackground(QColor("#FEF3C7"))  # Light Amber background
            item.setForeground(QColor("#B45309"))  # Dark Amber text
        else:  # pending
            item.setBackground(QColor("#EFF6FF"))  # Light Blue background
            item.setForeground(QColor("#1D4ED8"))  # Dark Blue text

    def get_status(self, file_path_str: str) -> str:
        for row in range(self.rowCount()):
            path_item = self.item(row, 1)
            if path_item and path_item.text() == file_path_str:
                status_item = self.item(row, 5)
                if status_item:
                    return status_item.data(self.STATUS_ROLE) or "pending"
        return "pending"

    def has_processed_files(self) -> bool:
        for row in range(self.rowCount()):
            status_item = self.item(row, 5)
            if status_item:
                status = status_item.data(self.STATUS_ROLE)
                if status in ("optimized", "converted", "failed"):
                    return True
        return False

    def reset_all_statuses(self):
        for row in range(self.rowCount()):
            status_item = self.item(row, 5)
            if status_item:
                file_path_str = status_item.data(Qt.ItemDataRole.UserRole)
                status_item.setText(f"⏳ {tr('status.pending', 'Pending')}")
                status_item.setData(self.STATUS_ROLE, "pending")
                self._apply_status_style(status_item, "pending")

    def clear_files(self):
        self.setRowCount(0)

