from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from app.config.constants import APP_NAME, APP_TAGLINE, APP_VERSION
from app.i18n.i18n_manager import tr, I18nManager

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        I18nManager.instance().language_changed.connect(self.retranslate_ui)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(24, 24, 24, 24)

        card = QFrame()
        card.setObjectName("StatsCard")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(32, 32, 32, 32)

        self.title = QLabel(APP_NAME)
        self.title.setStyleSheet("font-size: 32px; font-weight: 900; color: #6366F1;")

        self.tagline = QLabel(tr("app.tagline", APP_TAGLINE))
        self.tagline.setStyleSheet("font-size: 15px; opacity: 0.8;")

        self.ver = QLabel(f"Version {APP_VERSION}")
        self.ver.setStyleSheet("font-size: 13px; opacity: 0.6;")

        self.pub = QLabel("Developed by h08831n")
        self.pub.setStyleSheet("font-size: 13px; font-weight: 600;")

        btn_box = QHBoxLayout()
        btn_box.setSpacing(12)

        self.btn_github = QPushButton("GitHub Repository")
        self.btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/h08831n/OptiPixel")))

        self.btn_issues = QPushButton("Report Issue")
        self.btn_issues.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/h08831n/OptiPixel/issues")))

        self.btn_update = QPushButton(tr("about.check_update", "Check for Updates"))
        self.btn_update.clicked.connect(self.check_update)

        btn_box.addWidget(self.btn_github)
        btn_box.addWidget(self.btn_issues)
        btn_box.addWidget(self.btn_update)

        # Donation Box
        donate_box = QFrame()
        donate_box.setStyleSheet("background-color: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 12px;")
        donate_layout = QVBoxLayout(donate_box)
        donate_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_donate_title = QLabel(tr("about.donate_title", "☕ Support Ongoing Development"))
        self.lbl_donate_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #F59E0B;")

        self.lbl_donate_addr = QLabel("TON / USDT (TON): UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3")
        self.lbl_donate_addr.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lbl_donate_addr.setStyleSheet("font-size: 12px; font-family: monospace;")

        donate_layout.addWidget(self.lbl_donate_title)
        donate_layout.addWidget(self.lbl_donate_addr)

        card_layout.addWidget(self.title)
        card_layout.addWidget(self.tagline)
        card_layout.addWidget(self.ver)
        card_layout.addWidget(self.pub)
        card_layout.addSpacing(16)
        card_layout.addLayout(btn_box)
        card_layout.addSpacing(16)
        card_layout.addWidget(donate_box)

        layout.addWidget(card)

    def retranslate_ui(self):
        self.tagline.setText(tr("app.tagline", APP_TAGLINE))
        self.btn_github.setText(tr("about.github", "GitHub Repository"))
        self.btn_issues.setText(tr("about.issues", "Report Issue"))
        self.btn_update.setText(tr("about.check_update", "Check for Updates"))
        self.lbl_donate_title.setText(tr("about.donate_title", "☕ Support Ongoing Development"))

    def check_update(self):
        from PySide6.QtWidgets import QMessageBox
        from app.services.update_service import UpdateService

        self.btn_update.setEnabled(False)
        self.btn_update.setText(tr("about.checking", "Checking..."))

        release_info = UpdateService().check_for_updates()

        self.btn_update.setEnabled(True)
        self.btn_update.setText(tr("about.check_update", "Check for Updates"))

        if release_info and release_info.get("has_update"):
            tag = release_info.get("tag_name", "New")
            installer_url = release_info.get("installer_url", release_info.get("html_url"))

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(tr("update.available_title", "Update Available"))
            msg_box.setText(tr("update.available_msg", f"A new version (v{tag}) is available!\nWould you like to download the Installer?"))
            btn_dl = msg_box.addButton(tr("update.download_installer", "Download Installer"), QMessageBox.ButtonRole.AcceptRole)
            btn_page = msg_box.addButton(tr("update.view_release", "View Release Page"), QMessageBox.ButtonRole.ActionRole)
            btn_close = msg_box.addButton(tr("button.cancel", "Cancel"), QMessageBox.ButtonRole.RejectRole)

            msg_box.exec()

            if msg_box.clickedButton() == btn_dl:
                QDesktopServices.openUrl(QUrl(installer_url))
            elif msg_box.clickedButton() == btn_page:
                QDesktopServices.openUrl(QUrl(release_info.get("html_url")))
        else:
            QMessageBox.information(
                self,
                tr("update.up_to_date_title", "Up to Date"),
                tr("update.up_to_date_msg", f"You are using the latest version of OptiPixel (v{APP_VERSION}).")
            )
