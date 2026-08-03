from pathlib import Path
from typing import List, Dict, Any, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QCheckBox, QSpinBox, QComboBox, QGroupBox, QSplitter
)
from PySide6.QtCore import Qt, Signal

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
from app.i18n.i18n_manager import tr, I18nManager

class OptimizePage(QWidget):
    start_processing_requested = Signal(dict)

    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        self.scanned_images: List[ImageInfo] = []
        self.scanner = ImageScanner()
        self.output_folder_path: Optional[Path] = None

        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Top Bar Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        self.card_files = StatsCardWidget(tr("stats.total", "Total Images"), "0")
        self.card_size = StatsCardWidget(tr("stats.original_size", "Original Size"), "0 B")
        self.card_saved = StatsCardWidget(tr("stats.saved", "Potential Savings"), "0 B")

        stats_layout.addWidget(self.card_files)
        stats_layout.addWidget(self.card_size)
        stats_layout.addWidget(self.card_saved)
        main_layout.addLayout(stats_layout)

        # Splitter: Left Options / Right Files & Dropzone
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Options Panel
        options_panel = QWidget()
        opt_layout = QVBoxLayout(options_panel)
        opt_layout.setContentsMargins(0, 0, 8, 0)
        opt_layout.setSpacing(12)

        # Group 1: Output Format & Quality
        self.group_fmt = QGroupBox(tr("group.format_quality", "Format & Quality"))
        fmt_box = QVBoxLayout(self.group_fmt)
        fmt_box.setSpacing(8)

        self.fmt_selector = FormatSelectorWidget(self.im_service.supported_formats)
        self.quality_ctrl = QualityControlWidget(82)

        self.chk_threshold = QCheckBox(tr("label.threshold", "Optimize only images >"))
        self.chk_threshold.setChecked(False)
        self.spin_threshold = QSpinBox()
        self.spin_threshold.setRange(10, 50000)
        self.spin_threshold.setValue(400)
        self.spin_threshold.setSuffix(" KB")

        thresh_layout = QHBoxLayout()
        thresh_layout.addWidget(self.chk_threshold)
        thresh_layout.addWidget(self.spin_threshold)

        self.chk_keep_orig = QCheckBox(tr("label.keep_original", "Keep original if output is larger"))
        self.chk_keep_orig.setChecked(True)

        fmt_box.addWidget(self.fmt_selector)
        fmt_box.addWidget(self.quality_ctrl)
        fmt_box.addLayout(thresh_layout)
        fmt_box.addWidget(self.chk_keep_orig)

        # Group 2: Resizing & Metadata
        self.group_resize = QGroupBox(tr("group.resize_metadata", "Resize & Metadata"))
        res_box = QVBoxLayout(self.group_resize)
        res_box.setSpacing(8)

        self.chk_resize = QCheckBox(tr("label.resize", "Enable Resize"))
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

        self.chk_strip_meta = QCheckBox(tr("label.strip_metadata", "Strip Metadata (Keep EXIF orientation)"))
        self.chk_strip_meta.setChecked(True)

        res_box.addWidget(self.chk_resize)
        res_box.addLayout(dim_layout)
        res_box.addWidget(self.chk_strip_meta)

        # Group 3: Output Location
        self.group_output = QGroupBox(tr("label.output_mode", "Output Strategy"))
        out_box = QVBoxLayout(self.group_output)
        out_box.setSpacing(8)

        self.combo_mode = QComboBox()
        self.combo_mode.addItem(tr("mode.folder", "Save to Another Folder"), "folder")
        self.combo_mode.addItem(tr("mode.replace", "Replace Original"), "replace")
        self.combo_mode.addItem(tr("mode.next_to_original", "Save Next to Original"), "next_to_original")

        self.btn_select_out_dir = QPushButton(tr("button.select_output_folder", "Select Output Folder..."))
        self.btn_select_out_dir.clicked.connect(self.select_output_folder)
        self.lbl_out_dir = QLabel(tr("label.no_output_folder", "No output folder selected"))
        self.lbl_out_dir.setStyleSheet("font-size: 11px; opacity: 0.7;")

        self.chk_preserve_struct = QCheckBox(tr("label.preserve_structure", "Preserve Subfolder Structure"))
        self.chk_preserve_struct.setChecked(True)

        self.chk_backup = QCheckBox(tr("label.backup", "Create Backup Before Replace"))
        self.chk_backup.setChecked(True)

        out_box.addWidget(self.combo_mode)
        out_box.addWidget(self.btn_select_out_dir)
        out_box.addWidget(self.lbl_out_dir)
        out_box.addWidget(self.chk_preserve_struct)
        out_box.addWidget(self.chk_backup)

        opt_layout.addWidget(self.group_fmt)
        opt_layout.addWidget(self.group_resize)
        opt_layout.addWidget(self.group_output)
        opt_layout.addStretch()

        # Right Panel: Import & File List
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(12)

        import_bar = QHBoxLayout()
        self.btn_add_files = QPushButton(tr("button.select_files", "Select Files..."))
        self.btn_add_files.clicked.connect(self.select_files)

        self.btn_add_folder = QPushButton(tr("button.select_folder", "Select Folder..."))
        self.btn_add_folder.clicked.connect(self.select_folder)

        self.chk_recursive = QCheckBox(tr("label.subfolders", "Include Subfolders"))
        self.chk_recursive.setChecked(True)

        self.btn_clear = QPushButton(tr("button.clear", "Clear All"))
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
        splitter.setSizes([380, 720])

        main_layout.addWidget(splitter)

        # Bottom Progress & Action Bar
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(16)
        self.progress_widget = ProgressWidget()

        self.btn_start = QPushButton(tr("button.start", "Start Optimization"))
        self.btn_start.setObjectName("PrimaryButton")
        self.btn_start.setMinimumHeight(44)
        self.btn_start.clicked.connect(self.emit_start)

        bottom_bar.addWidget(self.progress_widget, 1)
        bottom_bar.addWidget(self.btn_start)

        main_layout.addLayout(bottom_bar)

    def retranslate_ui(self):
        self.card_files.set_title(tr("stats.total", "Total Images"))
        self.card_size.set_title(tr("stats.original_size", "Original Size"))
        self.card_saved.set_title(tr("stats.saved", "Potential Savings"))

        self.group_fmt.setTitle(tr("group.format_quality", "Format & Quality"))
        self.fmt_selector.retranslate_ui()
        self.quality_ctrl.retranslate_ui()
        self.chk_threshold.setText(tr("label.threshold", "Optimize only images >"))
        self.chk_keep_orig.setText(tr("label.keep_original", "Keep original if output is larger"))

        self.group_resize.setTitle(tr("group.resize_metadata", "Resize & Metadata"))
        self.chk_resize.setText(tr("label.resize", "Enable Resize"))
        self.chk_strip_meta.setText(tr("label.strip_metadata", "Strip Metadata"))

        self.group_output.setTitle(tr("label.output_mode", "Output Strategy"))
        
        mode_val = self.combo_mode.currentData()
        self.combo_mode.clear()
        self.combo_mode.addItem(tr("mode.folder", "Save to Another Folder"), "folder")
        self.combo_mode.addItem(tr("mode.replace", "Replace Original"), "replace")
        self.combo_mode.addItem(tr("mode.next_to_original", "Save Next to Original"), "next_to_original")
        idx = self.combo_mode.findData(mode_val)
        if idx >= 0:
            self.combo_mode.setCurrentIndex(idx)

        self.btn_select_out_dir.setText(tr("button.select_output_folder", "Select Output Folder..."))
        if not self.output_folder_path:
            self.lbl_out_dir.setText(tr("label.no_output_folder", "No output folder selected"))

        self.chk_preserve_struct.setText(tr("label.preserve_structure", "Preserve Subfolder Structure"))
        self.chk_backup.setText(tr("label.backup", "Create Backup Before Replace"))

        self.btn_add_files.setText(tr("button.select_files", "Select Files..."))
        self.btn_add_folder.setText(tr("button.select_folder", "Select Folder..."))
        self.chk_recursive.setText(tr("label.subfolders", "Include Subfolders"))
        self.btn_clear.setText(tr("button.clear", "Clear All"))

        self.drop_zone.retranslate_ui()
        self.file_list.retranslate_headers()
        self.progress_widget.retranslate_ui()
        self.btn_start.setText(tr("button.start", "Start Optimization"))

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, tr("title.select_images", "Select Images"), "",
            "Images (*.jpg *.jpeg *.png *.webp *.avif *.heic *.tiff *.bmp *.gif)"
        )
        if files:
            self.handle_paths_imported([Path(f) for f in files])

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, tr("title.select_folder", "Select Folder"))
        if folder:
            self.handle_paths_imported([Path(folder)])

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, tr("title.select_output_folder", "Select Output Folder"))
        if folder:
            self.output_folder_path = Path(folder)
            self.lbl_out_dir.setText(str(self.output_folder_path))

    def handle_paths_imported(self, paths: List[Path]):
        recursive = self.chk_recursive.isChecked()
        scanned = self.scanner.scan_paths(paths, recursive=recursive)
        for img in scanned:
            if not any(existing.file_path == img.file_path for existing in self.scanned_images):
                self.scanned_images.append(img)
                self.file_list.add_image(img)

        self.update_stats()

    def update_stats(self):
        total_files = len(self.scanned_images)
        total_bytes = sum(img.file_size_bytes for img in self.scanned_images)
        est_saved = int(total_bytes * 0.45)

        self.card_files.set_value(str(total_files))
        self.card_size.set_value(format_size(total_bytes))
        self.card_saved.set_value(format_size(est_saved), tr("stats.estimated", "Estimated"))

    def clear_all(self):
        self.scanned_images.clear()
        self.file_list.clear_files()
        self.update_stats()

    def emit_start(self):
        if not self.scanned_images:
            return

        mode = self.combo_mode.currentData()
        out_folder = self.output_folder_path

        # If mode is "folder" and no output folder has been chosen by the user
        if mode == "folder" and not out_folder:
            # First try prompting user to pick a folder
            chosen = QFileDialog.getExistingDirectory(self, tr("title.select_output_folder", "Select Output Folder"))
            if chosen:
                out_folder = Path(chosen)
                self.output_folder_path = out_folder
                self.lbl_out_dir.setText(str(out_folder))
            else:
                # Fallback automatically to an "optimized" folder next to the first image
                first_parent = self.scanned_images[0].file_path.parent
                out_folder = first_parent / "optimized"
                out_folder.mkdir(parents=True, exist_ok=True)
                self.output_folder_path = out_folder
                self.lbl_out_dir.setText(str(out_folder))

        # Determine common parent folder for subfolder structure
        base_folder = None
        if len(self.scanned_images) > 0:
            parents = [img.file_path.parent for img in self.scanned_images]
            try:
                base_folder = Path(Path.commonpath(parents))
            except Exception:
                base_folder = parents[0]

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
                "output_mode": mode,
                "output_folder": out_folder,
                "base_input_folder": base_folder,
                "preserve_structure": self.chk_preserve_struct.isChecked(),
                "backup": {"enabled": self.chk_backup.isChecked()}
            }
        }
        self.start_processing_requested.emit(job_config)
