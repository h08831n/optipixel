from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QCheckBox, QSpinBox, QComboBox, QGroupBox, QSplitter
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from typing import List, Dict, Any

from app.ui.widgets.drop_zone import DropZoneWidget
from app.ui.widgets.file_list import FileListWidget
from app.ui.widgets.progress_widget import ProgressWidget
from app.ui.widgets.stats_card import StatsCardWidget
from app.ui.widgets.format_selector import FormatSelectorWidget
from app.ui.widgets.quality_control import QualityControlWidget
from app.core.scanner import ImageScanner
from app.core.image_info import ImageInfo
from app.services.imagemagick_service import ImageMagickService
from app.utils.size_utils import format_size

class OptimizePage(QWidget):
    start_processing_requested = Signal(dict)

    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        self.scanned_images: List[ImageInfo] = []
        self.scanner = ImageScanner()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Top Bar Stats Cards
        stats_layout = QHBoxLayout()
        self.card_files = StatsCardWidget("Total Images", "0")
        self.card_size = StatsCardWidget("Original Size", "0 B")
        self.card_saved = StatsCardWidget("Potential Savings", "0 B")

        stats_layout.addWidget(self.card_files)
        stats_layout.addWidget(self.card_size)
        stats_layout.addWidget(self.card_saved)
        main_layout.addLayout(stats_layout)

        # Splitter: Left Options / Right Files & Dropzone
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Options Panel
        options_panel = QWidget()
        opt_layout = QVBoxLayout(options_panel)

        # Group 1: Output Format & Quality
        group_fmt = QGroupBox("Format & Quality")
        fmt_box = QVBoxLayout(group_fmt)

        self.fmt_selector = FormatSelectorWidget(self.im_service.supported_formats)
        self.quality_ctrl = QualityControlWidget(82)

        self.chk_threshold = QCheckBox("Optimize only images >")
        self.chk_threshold.setChecked(True)
        self.spin_threshold = QSpinBox()
        self.spin_threshold.setRange(10, 50000)
        self.spin_threshold.setValue(400)
        self.spin_threshold.setSuffix(" KB")

        thresh_layout = QHBoxLayout()
        thresh_layout.addWidget(self.chk_threshold)
        thresh_layout.addWidget(self.spin_threshold)

        self.chk_keep_orig = QCheckBox("Keep original if output is larger")
        self.chk_keep_orig.setChecked(True)

        fmt_box.addWidget(self.fmt_selector)
        fmt_box.addWidget(self.quality_ctrl)
        fmt_box.addLayout(thresh_layout)
        fmt_box.addWidget(self.chk_keep_orig)

        # Group 2: Resizing & Metadata
        group_resize = QGroupBox("Resize & Metadata")
        res_box = QVBoxLayout(group_resize)

        self.chk_resize = QCheckBox("Enable Resize")
        self.spin_max_w = QSpinBox()
        self.spin_max_w.setRange(100, 10000)
        self.spin_max_w.setValue(2000)
        self.spin_max_w.setPrefix("W: ")

        self.spin_max_h = QSpinBox()
        self.spin_max_h.setRange(100, 10000)
        self.spin_max_h.setValue(2000)
        self.spin_max_h.setPrefix("H: ")

        dim_layout = QHBoxLayout()
        dim_layout.addWidget(self.spin_max_w)
        dim_layout.addWidget(self.spin_max_h)

        self.chk_strip_meta = QCheckBox("Strip Metadata (Keep EXIF orientation)")
        self.chk_strip_meta.setChecked(True)

        res_box.addWidget(self.chk_resize)
        res_box.addLayout(dim_layout)
        res_box.addWidget(self.chk_strip_meta)

        # Group 3: Output Location
        group_output = QGroupBox("Output Strategy")
        out_box = QVBoxLayout(group_output)

        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Save to Another Folder", "folder")
        self.combo_mode.addItem("Replace Original", "replace")
        self.combo_mode.addItem("Save Next to Original", "next_to_original")

        self.btn_select_out_dir = QPushButton("Select Output Folder...")
        self.btn_select_out_dir.clicked.connect(self.select_output_folder)
        self.lbl_out_dir = QLabel("No output folder selected")
        self.lbl_out_dir.setStyleSheet("font-size: 11px; color: #718096;")

        self.chk_preserve_struct = QCheckBox("Preserve Subfolder Structure")
        self.chk_preserve_struct.setChecked(True)

        self.chk_backup = QCheckBox("Create Backup Before Replace")
        self.chk_backup.setChecked(True)

        out_box.addWidget(self.combo_mode)
        out_box.addWidget(self.btn_select_out_dir)
        out_box.addWidget(self.lbl_out_dir)
        out_box.addWidget(self.chk_preserve_struct)
        out_box.addWidget(self.chk_backup)

        opt_layout.addWidget(group_fmt)
        opt_layout.addWidget(group_resize)
        opt_layout.addWidget(group_output)
        opt_layout.addStretch()

        # Right Panel: Import & File List
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        import_bar = QHBoxLayout()
        self.btn_add_files = QPushButton("Select Files...")
        self.btn_add_files.clicked.connect(self.select_files)

        self.btn_add_folder = QPushButton("Select Folder...")
        self.btn_add_folder.clicked.connect(self.select_folder)

        self.chk_recursive = QCheckBox("Include Subfolders")
        self.chk_recursive.setChecked(True)

        self.btn_clear = QPushButton("Clear All")
        self.btn_clear.clicked.connect(self.clear_all)

        import_bar.addWidget(self.btn_add_files)
        import_bar.addWidget(self.btn_add_folder)
        import_bar.addWidget(self.chk_recursive)
        import_bar.addStretch()
        import_bar.addWidget(self.btn_clear)

        self.drop_zone = DropZoneWidget()
        self.drop_zone.files_dropped.connect(self.handle_paths_imported)

        self.file_list = FileListWidget()

        right_layout.addLayout(import_bar)
        right_layout.addWidget(self.drop_zone)
        right_layout.addWidget(self.file_list)

        splitter.addWidget(options_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 650])

        main_layout.addWidget(splitter)

        # Bottom Progress & Action Bar
        bottom_bar = QHBoxLayout()
        self.progress_widget = ProgressWidget()

        self.btn_start = QPushButton("Start Optimization")
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #3357C0;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 24px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #26429A;
            }
        """)
        self.btn_start.clicked.connect(self.emit_start)

        bottom_bar.addWidget(self.progress_widget, 1)
        bottom_bar.addWidget(self.btn_start)

        main_layout.addLayout(bottom_bar)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Images (*.jpg *.jpeg *.png *.webp *.avif *.heic *.tiff *.bmp *.gif)"
        )
        if files:
            self.handle_paths_imported([Path(f) for f in files])

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.handle_paths_imported([Path(folder)])

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.lbl_out_dir.setText(folder)

    def handle_paths_imported(self, paths: List[Path]):
        recursive = self.chk_recursive.isChecked()
        scanned = self.scanner.scan_paths(paths, recursive=recursive)
        for img in scanned:
            self.scanned_images.append(img)
            self.file_list.add_image(img)

        self.update_stats()

    def update_stats(self):
        total_files = len(self.scanned_images)
        total_bytes = sum(img.file_size_bytes for img in self.scanned_images)
        est_saved = int(total_bytes * 0.45)  # Est 45% compression

        self.card_files.set_value(str(total_files))
        self.card_size.set_value(format_size(total_bytes))
        self.card_saved.set_value(format_size(est_saved), "Estimated")

    def clear_all(self):
        self.scanned_images.clear()
        self.file_list.clear_files()
        self.update_stats()

    def emit_start(self):
        if not self.scanned_images:
            return

        out_folder_str = self.lbl_out_dir.text()
        out_folder = Path(out_folder_str) if out_folder_str != "No output folder selected" else None

        job_config = {
            "images": self.scanned_images,
            "target_format": self.fmt_selector.current_format(),
            "settings": {
                "quality": self.quality_ctrl.value(),
                "threshold_enabled": self.chk_threshold.isChecked(),
                "size_threshold_kb": self.spin_threshold.value(),
                "keep_original_if_larger": self.chk_keep_orig.isChecked(),
                "enable_resize": self.chk_resize.isChecked(),
                "max_width": self.spin_max_w.value(),
                "max_height": self.spin_max_h.value(),
                "strip_metadata": self.chk_strip_meta.isChecked(),
                "output_mode": self.combo_mode.currentData(),
                "output_folder": out_folder,
                "preserve_structure": self.chk_preserve_struct.isChecked(),
                "backup": {"enabled": self.chk_backup.isChecked()}
            }
        }
        self.start_processing_requested.emit(job_config)
