from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
    QPushButton, QGroupBox, QLineEdit, QFileDialog, QCheckBox
)
from app.services.imagemagick_service import ImageMagickService
from app.services.settings_service import SettingsService

class SettingsPage(QWidget):
    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        self.settings_service = SettingsService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Application Settings & Diagnostics")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D3748;")
        layout.addWidget(title)

        # ImageMagick Diagnostics
        group_im = QGroupBox("ImageMagick Engine Diagnostics")
        im_box = QVBoxLayout(group_im)

        lbl_exe = QLabel(f"Detected Executable: {self.im_service.executable or 'Not Found'}")
        lbl_ver = QLabel(f"Version: {self.im_service.version_info}")

        fmts = ", ".join([f for f, ok in self.im_service.supported_formats.items() if ok])
        lbl_fmts = QLabel(f"Supported Delegates: {fmts or 'None'}")

        im_box.addWidget(lbl_exe)
        im_box.addWidget(lbl_ver)
        im_box.addWidget(lbl_fmts)
        layout.addWidget(group_im)

        # General
        group_gen = QGroupBox("General & Localization")
        gen_box = QVBoxLayout(group_gen)

        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("English", "en")
        self.combo_lang.addItem("فارسی (Persian)", "fa")
        self.combo_lang.addItem("Deutsch", "de")
        self.combo_lang.addItem("Türkçe", "tr")
        self.combo_lang.addItem("العربية", "ar")
        self.combo_lang.addItem("Français", "fr")
        self.combo_lang.addItem("Español", "es")
        self.combo_lang.addItem("Русский", "ru")
        lang_layout.addWidget(self.combo_lang)
        gen_box.addLayout(lang_layout)

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("UI Theme:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["System", "Light", "Dark"])
        theme_layout.addWidget(self.combo_theme)
        gen_box.addLayout(theme_layout)

        layout.addWidget(group_gen)

        # Processing Workers
        group_proc = QGroupBox("Processing Workers")
        proc_box = QHBoxLayout(group_proc)
        proc_box.addWidget(QLabel("Worker Threads:"))
        self.spin_workers = QSpinBox()
        self.spin_workers.setRange(0, 32)
        self.spin_workers.setValue(0)  # Auto
        proc_box.addWidget(self.spin_workers)
        layout.addWidget(group_proc)

        layout.addStretch()
