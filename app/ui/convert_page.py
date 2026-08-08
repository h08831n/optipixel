from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QSplitter, QMessageBox
)
from PySide6.QtCore import Signal, Qt

from app.services.imagemagick_service import ImageMagickService
from app.ui.widgets.drop_zone import DropZoneWidget
from app.ui.widgets.file_list import FileListWidget
from app.ui.widgets.format_selector import FormatSelectorWidget
from app.ui.widgets.progress_widget import ProgressWidget
from app.ui.widgets.quality_control import QualityControlWidget
from app.core.scanner import ImageScanner
from app.core.image_info import ImageInfo
from app.i18n.i18n_manager import tr, I18nManager

class ConvertPage(QWidget):
    start_conversion_requested = Signal(dict)

    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        self.scanned_images: List[ImageInfo] = []
        self.scanner = ImageScanner()
        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.title = QLabel(tr("convert.title", "Format Converter Matrix"))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.subtitle = QLabel(tr("convert.subtitle", "Convert batch images between WebP, AVIF, JPEG, PNG, TIFF, HEIC, BMP"))
        self.subtitle.setStyleSheet("font-size: 13px; opacity: 0.8;")
        layout.addWidget(self.subtitle)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Options Left
        opts_panel = QWidget()
        opts_layout = QVBoxLayout(opts_panel)
        opts_layout.setContentsMargins(0, 0, 8, 0)
        opts_layout.setSpacing(12)

        self.fmt_selector = FormatSelectorWidget(self.im_service.supported_formats)
        self.quality_ctrl = QualityControlWidget(85)

        opts_layout.addWidget(self.fmt_selector)
        opts_layout.addWidget(self.quality_ctrl)
        opts_layout.addStretch()

        # Files Right
        files_panel = QWidget()
        files_layout = QVBoxLayout(files_panel)
        files_layout.setContentsMargins(8, 0, 0, 0)

        import_bar = QHBoxLayout()
        self.btn_select = QPushButton(tr("button.select_files", "Select Files..."))
        self.btn_select.clicked.connect(self.select_files)

        self.btn_clear = QPushButton(tr("button.clear", "Clear All"))
        self.btn_clear.clicked.connect(self.clear_all)

        import_bar.addWidget(self.btn_select)
        import_bar.addStretch()
        import_bar.addWidget(self.btn_clear)

        self.drop_zone = DropZoneWidget()
        self.drop_zone.files_dropped.connect(self.handle_paths_imported)
        self.drop_zone.clicked.connect(self.select_files)

        self.file_list = FileListWidget()

        files_layout.addLayout(import_bar)
        files_layout.addWidget(self.drop_zone)
        files_layout.addWidget(self.file_list)

        splitter.addWidget(opts_panel)
        splitter.addWidget(files_panel)
        splitter.setSizes([320, 780])

        layout.addWidget(splitter)

        bottom_bar = QHBoxLayout()
        self.progress_widget = ProgressWidget()

        self.btn_start = QPushButton(tr("button.start_convert", "Start Conversion"))
        self.btn_start.setObjectName("PrimaryButton")
        self.btn_start.setMinimumHeight(44)
        self.btn_start.clicked.connect(self.emit_start)

        bottom_bar.addWidget(self.progress_widget, 1)
        bottom_bar.addWidget(self.btn_start)

        layout.addLayout(bottom_bar)

    def retranslate_ui(self):
        self.title.setText(tr("convert.title", "Format Converter Matrix"))
        self.subtitle.setText(tr("convert.subtitle", "Convert batch images between WebP, AVIF, JPEG, PNG, TIFF, HEIC, BMP"))
        self.fmt_selector.retranslate_ui()
        self.quality_ctrl.retranslate_ui()
        self.btn_select.setText(tr("button.select_files", "Select Files..."))
        self.btn_clear.setText(tr("button.clear", "Clear All"))
        self.drop_zone.retranslate_ui()
        self.file_list.retranslate_headers()
        self.progress_widget.retranslate_ui()
        self.btn_start.setText(tr("button.start_convert", "Start Conversion"))

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, tr("title.select_images", "Select Images"), "",
            "Images (*.jpg *.jpeg *.png *.webp *.avif *.heic *.tiff *.bmp *.gif)"
        )
        if files:
            self.handle_paths_imported([Path(f) for f in files])

    def handle_paths_imported(self, paths: List[Path]):
        scanned = self.scanner.scan_paths(paths, recursive=True)
        for img in scanned:
            if not any(existing.file_path == img.file_path for existing in self.scanned_images):
                self.scanned_images.append(img)
                self.file_list.add_image(img)

    def clear_all(self):
        self.scanned_images.clear()
        self.file_list.clear_files()

    def emit_start(self):
        if not self.scanned_images:
            return

        target_images = self.scanned_images
        if self.file_list.has_processed_files():
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(tr("dialog.reprocess_title", "Already Processed Files"))
            msg_box.setText(tr("dialog.reprocess_msg", "Some files in the list have already been processed. How would you like to proceed?"))
            btn_skip = msg_box.addButton(tr("button.skip_completed", "Skip Completed"), QMessageBox.ButtonRole.AcceptRole)
            btn_reprocess = msg_box.addButton(tr("button.reprocess_all", "Re-process All"), QMessageBox.ButtonRole.ActionRole)
            btn_cancel = msg_box.addButton(tr("button.cancel", "Cancel"), QMessageBox.ButtonRole.RejectRole)
            msg_box.setDefaultButton(btn_skip)
            msg_box.exec()

            clicked_btn = msg_box.clickedButton()
            if clicked_btn == btn_cancel or clicked_btn is None:
                return
            elif clicked_btn == btn_skip:
                target_images = [img for img in self.scanned_images if self.file_list.get_status(str(img.file_path)) not in ("optimized", "converted")]
                if not target_images:
                    return
            else:
                self.file_list.reset_all_statuses()
                target_images = self.scanned_images

        first_parent = target_images[0].file_path.parent
        out_folder = first_parent / "converted"
        out_folder.mkdir(parents=True, exist_ok=True)

        job_config = {
            "images": target_images,
            "target_format": self.fmt_selector.current_format(),
            "settings": {
                "quality": self.quality_ctrl.value(),
                "threshold_enabled": False,
                "keep_original_if_larger": False,
                "enable_resize": False,
                "strip_metadata": False,
                "output_mode": "folder",
                "output_folder": out_folder,
                "preserve_structure": False,
                "backup": {"enabled": False}
            }
        }
        self.start_conversion_requested.emit(job_config)
