from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
    QPushButton, QGroupBox
)
from PySide6.QtCore import Signal
from app.services.imagemagick_service import ImageMagickService
from app.services.settings_service import SettingsService
from app.i18n.i18n_manager import tr, I18nManager
from app.ui.widgets.log_dialog import LogViewerDialog
from app.utils.logging_utils import LOG_FILE

class SettingsPage(QWidget):
    theme_changed = Signal(str)

    def __init__(self, im_service: ImageMagickService, parent=None):
        super().__init__(parent)
        self.im_service = im_service
        self.settings_service = SettingsService()
        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.title = QLabel(tr("settings.title", "Application Settings & Diagnostics"))
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        # ImageMagick Diagnostics
        self.group_im = QGroupBox(tr("settings.im_diagnostics", "ImageMagick Engine Diagnostics"))
        im_box = QVBoxLayout(self.group_im)

        self.lbl_exe = QLabel(f"Detected Executable: {self.im_service.executable or 'Not Found'}")
        self.lbl_ver = QLabel(f"Version: {self.im_service.version_info}")

        fmts = ", ".join([f for f, ok in self.im_service.supported_formats.items() if ok])
        self.lbl_fmts = QLabel(f"Supported Delegates: {fmts or 'None'}")

        im_box.addWidget(self.lbl_exe)
        im_box.addWidget(self.lbl_ver)
        im_box.addWidget(self.lbl_fmts)
        layout.addWidget(self.group_im)

        # Developer & Debug Logs
        self.group_log = QGroupBox(tr("settings.dev_logs", "Developer & Debug Logging"))
        log_box = QVBoxLayout(self.group_log)
        self.lbl_log_file = QLabel(f"<b>Log File:</b> {LOG_FILE}")
        self.lbl_log_file.setWordWrap(True)
        log_box.addWidget(self.lbl_log_file)

        btn_log_layout = QHBoxLayout()
        self.btn_open_log_dialog = QPushButton(tr("settings.view_logs", "Open Live Log Viewer"))
        self.btn_open_log_dialog.clicked.connect(self.show_log_dialog)
        btn_log_layout.addWidget(self.btn_open_log_dialog)
        btn_log_layout.addStretch()
        log_box.addLayout(btn_log_layout)
        layout.addWidget(self.group_log)

        # General & Localization
        self.group_gen = QGroupBox(tr("settings.localization", "General & Localization"))
        gen_box = QVBoxLayout(self.group_gen)

        lang_layout = QHBoxLayout()
        self.lbl_lang = QLabel(tr("settings.language", "Language:"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("English", "en")
        self.combo_lang.addItem("فارسی (Persian)", "fa")
        self.combo_lang.addItem("Deutsch", "de")
        self.combo_lang.addItem("Türkçe", "tr")
        self.combo_lang.addItem("العربية", "ar")
        self.combo_lang.addItem("Français", "fr")
        self.combo_lang.addItem("Español", "es")
        self.combo_lang.addItem("Русский", "ru")

        curr_lang = I18nManager.instance().current_language
        idx = self.combo_lang.findData(curr_lang)
        if idx >= 0:
            self.combo_lang.setCurrentIndex(idx)

        self.combo_lang.currentIndexChanged.connect(self.on_language_changed)

        lang_layout.addWidget(self.lbl_lang)
        lang_layout.addWidget(self.combo_lang)
        gen_box.addLayout(lang_layout)

        theme_layout = QHBoxLayout()
        self.lbl_theme = QLabel(tr("settings.theme", "UI Theme:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark", "Light"])
        
        saved_theme = self.settings_service.get_settings().get("general", "theme", "Dark")
        idx_t = self.combo_theme.findText(saved_theme)
        if idx_t >= 0:
            self.combo_theme.setCurrentIndex(idx_t)

        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)

        theme_layout.addWidget(self.lbl_theme)
        theme_layout.addWidget(self.combo_theme)
        gen_box.addLayout(theme_layout)

        layout.addWidget(self.group_gen)

        # Processing Workers
        self.group_proc = QGroupBox(tr("settings.processing_workers", "Processing Workers"))
        proc_box = QHBoxLayout(self.group_proc)
        self.lbl_workers = QLabel(tr("settings.worker_threads", "Worker Threads:"))
        self.spin_workers = QSpinBox()
        self.spin_workers.setRange(0, 32)
        self.spin_workers.setValue(0)
        proc_box.addWidget(self.lbl_workers)
        proc_box.addWidget(self.spin_workers)
        layout.addWidget(self.group_proc)

        layout.addStretch()

    def show_log_dialog(self):
        dialog = LogViewerDialog(self)
        dialog.exec()

    def on_language_changed(self, index: int):
        lang_code = self.combo_lang.itemData(index)
        if lang_code:
            I18nManager.instance().set_language(lang_code)

    def on_theme_changed(self, theme_text: str):
        settings = self.settings_service.get_settings()
        settings.set("general", "theme", theme_text)
        self.theme_changed.emit(theme_text)

    def retranslate_ui(self):
        self.title.setText(tr("settings.title", "Application Settings & Diagnostics"))
        self.group_im.setTitle(tr("settings.im_diagnostics", "ImageMagick Engine Diagnostics"))
        self.group_log.setTitle(tr("settings.dev_logs", "Developer & Debug Logging"))
        self.btn_open_log_dialog.setText(tr("settings.view_logs", "Open Live Log Viewer"))
        self.group_gen.setTitle(tr("settings.localization", "General & Localization"))
        self.lbl_lang.setText(tr("settings.language", "Language:"))
        self.lbl_theme.setText(tr("settings.theme", "UI Theme:"))
        self.group_proc.setTitle(tr("settings.processing_workers", "Processing Workers"))
        self.lbl_workers.setText(tr("settings.worker_threads", "Worker Threads:"))
