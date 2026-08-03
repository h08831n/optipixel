import time
from pathlib import Path
from typing import List, Dict, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QStatusBar, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.config.constants import APP_NAME, APP_TAGLINE, APP_VERSION
from app.services.imagemagick_service import ImageMagickService
from app.services.history_service import HistoryService
from app.core.processor import ImageProcessor, ProcessingResult
from app.core.output_manager import OutputManager
from app.core.backup_manager import BackupManager
from app.workers.processing_worker import ProcessingWorker
from app.workers.worker_pool import WorkerPoolManager
from app.utils.size_utils import format_size

from app.ui.optimize_page import OptimizePage
from app.ui.convert_page import ConvertPage
from app.ui.audit_page import AuditPage
from app.ui.history_page import HistoryPage
from app.ui.settings_page import SettingsPage
from app.ui.about_page import AboutPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {APP_TAGLINE}")
        self.resize(1200, 800)

        self.im_service = ImageMagickService()
        self.history_service = HistoryService()
        self.worker_pool = WorkerPoolManager()
        self.processor = ImageProcessor(self.im_service)

        self.active_results: List[ProcessingResult] = []
        self.job_start_time = 0.0

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Navigation Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1A202C;
                color: #E2E8F0;
                border: none;
                font-size: 14px;
                padding-top: 10px;
            }
            QListWidget::item {
                height: 48px;
                padding-left: 16px;
            }
            QListWidget::item:selected {
                background-color: #3357C0;
                color: #FFFFFF;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: #2D3748;
            }
        """)

        nav_items = [
            ("⚡ Optimize", 0),
            ("🔄 Convert", 1),
            ("🔍 Audit", 2),
            ("📜 History", 3),
            ("⚙️ Settings", 4),
            ("ℹ️ About", 5)
        ]

        for text, index in nav_items:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, index)
            self.sidebar.addItem(item)

        self.sidebar.currentRowChanged.connect(self.on_nav_changed)

        # Page Stack
        self.stack = QStackedWidget()

        self.optimize_page = OptimizePage(self.im_service)
        self.optimize_page.start_processing_requested.connect(self.start_batch_job)

        self.convert_page = ConvertPage(self.im_service)
        self.audit_page = AuditPage()
        self.history_page = HistoryPage()
        self.settings_page = SettingsPage(self.im_service)
        self.about_page = AboutPage()

        self.stack.addWidget(self.optimize_page)
        self.stack.addWidget(self.convert_page)
        self.stack.addWidget(self.audit_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.about_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        self.sidebar.setCurrentRow(0)

        # Status Bar
        self.statusBar().showMessage(f"ImageMagick: {self.im_service.version_info}")

    def on_nav_changed(self, index: int):
        self.stack.setCurrentIndex(index)

    def start_batch_job(self, config: dict):
        images = config["images"]
        if not images:
            return

        settings = config["settings"]
        target_fmt = config["target_format"]

        output_mgr = OutputManager(
            mode=settings["output_mode"],
            output_folder=settings["output_folder"],
            preserve_structure=settings["preserve_structure"]
        )

        self.active_results.clear()
        self.job_start_time = time.time()
        total = len(images)
        completed = [0]

        def on_finished(result: ProcessingResult):
            self.active_results.append(result)
            completed[0] += 1
            self.optimize_page.progress_widget.update_progress(
                current=completed[0],
                total=total,
                current_file=result.source_path.name
            )

            if completed[0] == total:
                self.on_job_completed(total)

        for img in images:
            worker = ProcessingWorker(
                processor=self.processor,
                image_info=img,
                target_format=target_fmt,
                settings=settings,
                output_manager=output_mgr
            )
            worker.signals.finished.connect(on_finished)
            self.worker_pool.start_worker(worker)

    def on_job_completed(self, total: int):
        duration = time.time() - self.job_start_time
        processed = [r for r in self.active_results if r.status in ("optimized", "converted")]
        skipped = [r for r in self.active_results if r.status == "skipped"]
        failed = [r for r in self.active_results if r.status == "failed"]

        orig_bytes = sum(r.original_size_bytes for r in self.active_results)
        new_bytes = sum(r.new_size_bytes for r in processed) + sum(r.original_size_bytes for r in skipped + failed)
        saved_bytes = sum(r.saved_bytes for r in processed)

        # Save to history
        self.history_service.add_job_entry({
            "operation": "Batch Optimize",
            "files_processed": len(processed),
            "saved_space_str": format_size(saved_bytes),
            "duration_str": f"{duration:.1f}s"
        })

        QMessageBox.information(
            self,
            "Job Complete",
            f"Batch processing completed in {duration:.1f}s!\n\n"
            f"Processed: {len(processed)}\n"
            f"Skipped: {len(skipped)}\n"
            f"Failed: {len(failed)}\n\n"
            f"Total Space Saved: {format_size(saved_bytes)}"
        )
