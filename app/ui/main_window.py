import time
from pathlib import Path
from typing import List, Dict, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QStatusBar, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

from app.config.constants import APP_NAME, APP_TAGLINE
from app.services.imagemagick_service import ImageMagickService
from app.services.history_service import HistoryService
from app.services.settings_service import SettingsService
from app.core.processor import ImageProcessor, ProcessingResult
from app.core.output_manager import OutputManager
from app.workers.processing_worker import ProcessingWorker
from app.workers.worker_pool import WorkerPoolManager
from app.utils.size_utils import format_size
from app.i18n.i18n_manager import tr, I18nManager
from app.ui.styles import DARK_STYLESHEET, LIGHT_STYLESHEET

from app.ui.optimize_page import OptimizePage
from app.ui.convert_page import ConvertPage
from app.ui.audit_page import AuditPage
from app.ui.history_page import HistoryPage
from app.ui.settings_page import SettingsPage
from app.ui.about_page import AboutPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1240, 820)

        self.im_service = ImageMagickService()
        self.history_service = HistoryService()
        self.settings_service = SettingsService()
        self.worker_pool = WorkerPoolManager()
        self.processor = ImageProcessor(self.im_service)

        self.active_results: List[ProcessingResult] = []
        self.active_workers: List[ProcessingWorker] = []
        self.job_start_time = 0.0

        # Set window icon
        logo_path = Path(__file__).parent.parent.parent / "public" / "logo.svg"
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

        self.init_ui()

        # Connect language & theme listeners
        I18nManager.instance().language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

        saved_theme = self.settings_service.get_settings().get("general", "theme", "Dark")
        self.apply_theme(saved_theme)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Navigation Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("SidebarList")
        self.sidebar.setFixedWidth(210)

        nav_items = [
            (f"⚡ {tr('nav.optimize', 'Optimize')}", 0),
            (f"🔄 {tr('nav.convert', 'Convert')}", 1),
            (f"🔍 {tr('nav.audit', 'Audit')}", 2),
            (f"📜 {tr('nav.history', 'History')}", 3),
            (f"⚙️ {tr('nav.settings', 'Settings')}", 4),
            (f"ℹ️ {tr('nav.about', 'About')}", 5)
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
        self.convert_page.start_conversion_requested.connect(self.start_batch_job)

        self.audit_page = AuditPage()
        self.history_page = HistoryPage()
        
        self.settings_page = SettingsPage(self.im_service)
        self.settings_page.theme_changed.connect(self.apply_theme)

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

    def apply_theme(self, theme_name: str):
        if theme_name.lower() == "light":
            self.setStyleSheet(LIGHT_STYLESHEET)
        else:
            self.setStyleSheet(DARK_STYLESHEET)

    def retranslate_ui(self):
        # Update layout direction
        app_inst = QApplication.instance()
        if I18nManager.instance().is_rtl():
            if app_inst:
                app_inst.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            if app_inst:
                app_inst.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        title_app = tr("app.name", APP_NAME)
        tagline_app = tr("app.tagline", APP_TAGLINE)
        self.setWindowTitle(f"{title_app} - {tagline_app}")

        nav_items_text = [
            f"⚡ {tr('nav.optimize', 'Optimize')}",
            f"🔄 {tr('nav.convert', 'Convert')}",
            f"🔍 {tr('nav.audit', 'Audit')}",
            f"📜 {tr('nav.history', 'History')}",
            f"⚙️ {tr('nav.settings', 'Settings')}",
            f"ℹ️ {tr('nav.about', 'About')}"
        ]
        for idx, text in enumerate(nav_items_text):
            item = self.sidebar.item(idx)
            if item:
                item.setText(text)

    def on_nav_changed(self, index: int):
        self.stack.setCurrentIndex(index)

    def start_batch_job(self, config: dict):
        images = config["images"]
        if not images:
            return

        settings = config["settings"]
        target_fmt = config["target_format"]

        output_mgr = OutputManager(
            mode=settings.get("output_mode", "folder"),
            output_folder=settings.get("output_folder"),
            base_input_folder=settings.get("base_input_folder"),
            preserve_structure=settings.get("preserve_structure", False)
        )

        self.active_results.clear()
        self.active_workers.clear()
        self.job_start_time = time.time()
        total = len(images)
        completed = [0]

        def on_finished(result: ProcessingResult):
            self.active_results.append(result)
            completed[0] += 1
            
            curr_page = self.stack.currentWidget()
            if hasattr(curr_page, "progress_widget"):
                curr_page.progress_widget.update_progress(
                    current=completed[0],
                    total=total,
                    current_file=result.source_path.name
                )

            if completed[0] == total:
                self.on_job_completed(total)

        def on_error(file_path_str: str, err_msg: str):
            res = ProcessingResult(
                source_path=Path(file_path_str),
                output_path=Path(file_path_str),
                status="failed",
                message=err_msg
            )
            on_finished(res)

        for img in images:
            worker = ProcessingWorker(
                processor=self.processor,
                image_info=img,
                target_format=target_fmt,
                settings=settings,
                output_manager=output_mgr
            )
            worker.signals.finished.connect(on_finished)
            worker.signals.error.connect(on_error)
            self.active_workers.append(worker)
            self.worker_pool.start_worker(worker)

    def on_job_completed(self, total: int):
        self.active_workers.clear()
        duration = time.time() - self.job_start_time
        processed = [r for r in self.active_results if r.status in ("optimized", "converted")]
        skipped = [r for r in self.active_results if r.status == "skipped"]
        failed = [r for r in self.active_results if r.status == "failed"]

        saved_bytes = sum(r.saved_bytes for r in processed)

        # Save to history
        self.history_service.add_job_entry({
            "operation": tr("nav.optimize", "Batch Optimize"),
            "files_processed": len(processed),
            "saved_space_str": format_size(saved_bytes),
            "duration_str": f"{duration:.1f}s"
        })

        msg_title = tr("dialog.complete_title", "Job Complete")
        msg_body = (
            f"{tr('dialog.complete_body', 'Batch processing completed in')} {duration:.1f}s!\n\n"
            f"{tr('stats.processed', 'Processed')}: {len(processed)}\n"
            f"{tr('stats.skipped', 'Skipped')}: {len(skipped)}\n"
            f"{tr('stats.failed', 'Failed')}: {len(failed)}\n\n"
            f"{tr('stats.saved', 'Total Space Saved')}: {format_size(saved_bytes)}"
        )

        QMessageBox.information(self, msg_title, msg_body)
