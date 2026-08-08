import os
import sys
import time
import urllib.request
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QTextEdit, QFrame, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal
from app.config.constants import APP_VERSION
from app.i18n.i18n_manager import tr

def _get_subproc_kwargs():
    kwargs = {}
    if sys.platform == "win32" or os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    return kwargs

class UpdateDownloadThread(QThread):
    progress = Signal(int, int, float, str)  # downloaded, total, percent, speed_str
    finished = Signal(str)                   # installer file path
    error = Signal(str)                      # error message

    def __init__(self, download_url: str, save_path: str):
        super().__init__()
        self.download_url = download_url
        self.save_path = save_path
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        try:
            req = urllib.request.Request(
                self.download_url,
                headers={"User-Agent": "OptiPixel-App-Updater"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0
                block_size = 1024 * 64
                start_time = time.time()

                Path(self.save_path).parent.mkdir(parents=True, exist_ok=True)
                with open(self.save_path, "wb") as f:
                    while not self._is_cancelled:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        downloaded += len(buffer)
                        f.write(buffer)

                        elapsed = time.time() - start_time
                        speed = (downloaded / 1024 / 1024) / elapsed if elapsed > 0 else 0
                        percent = (downloaded / total_size * 100) if total_size > 0 else 0
                        speed_str = f"{speed:.2f} MB/s"

                        self.progress.emit(downloaded, total_size, percent, speed_str)

                if self._is_cancelled:
                    if os.path.exists(self.save_path):
                        try:
                            os.remove(self.save_path)
                        except Exception:
                            pass
                    self.error.emit("Download cancelled")
                else:
                    self.finished.emit(self.save_path)
        except Exception as e:
            self.error.emit(str(e))

class UpdaterDialog(QDialog):
    def __init__(self, release_info: dict, parent=None):
        super().__init__(parent)
        self.release_info = release_info
        self.download_thread = None
        self.downloaded_installer_path = None
        self.setWindowTitle(tr("update.title", "OptiPixel In-App Auto Update"))
        self.resize(520, 420)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Header Box
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1B4B;
                border: 1px solid #4F46E5;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(6)

        title = QLabel(f"⚡ {tr('update.available', 'New Update Available')}: v{self.release_info.get('tag_name', '0.0.0')}")
        title.setStyleSheet("font-size: 17px; font-weight: 800; color: #818CF8;")

        subtitle = QLabel(f"{tr('update.current', 'Current Version')}: v{APP_VERSION}")
        subtitle.setStyleSheet("font-size: 12px; color: #94A3B8;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_frame)

        # Release Notes
        notes_label = QLabel(tr("update.notes", "Changelog & Release Notes:"))
        notes_label.setStyleSheet("font-weight: 700; color: #CBD5E1;")
        layout.addWidget(notes_label)

        self.notes_text = QTextEdit()
        self.notes_text.setReadOnly(True)
        self.notes_text.setText(self.release_info.get("body", "No release notes provided."))
        self.notes_text.setStyleSheet("""
            QTextEdit {
                background-color: #0F172A;
                border: 1px solid #1E293B;
                border-radius: 10px;
                color: #E2E8F0;
                font-size: 12px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.notes_text)

        # Progress Section
        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(6)

        self.lbl_status = QLabel(tr("update.status_downloading", "Downloading update package..."))
        self.lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #38BDF8;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 8px;
                height: 22px;
                text-align: center;
                color: #FFFFFF;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #06B6D4);
                border-radius: 7px;
            }
        """)

        progress_layout.addWidget(self.lbl_status)
        progress_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_frame)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_action = QPushButton(tr("update.btn_start", "Start In-App Update"))
        self.btn_action.setObjectName("PrimaryButton")
        self.btn_action.setStyleSheet("font-weight: bold; padding: 10px 20px; font-size: 13px;")
        self.btn_action.clicked.connect(self.on_action_clicked)

        self.btn_cancel = QPushButton(tr("button.cancel", "Cancel"))
        self.btn_cancel.clicked.connect(self.close)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_action)
        layout.addLayout(btn_layout)

    def on_action_clicked(self):
        if self.downloaded_installer_path and os.path.exists(self.downloaded_installer_path):
            self.install_and_restart()
            return

        installer_url = self.release_info.get("installer_url")
        if not installer_url or not installer_url.startswith("http"):
            QMessageBox.warning(self, "Update Error", "Installer URL is not valid.")
            return

        tag = self.release_info.get("tag_name", "latest")
        filename = f"OptiPixel-Installer-v{tag}.exe"
        import tempfile
        save_path = os.path.join(tempfile.gettempdir(), filename)

        self.btn_action.setEnabled(False)
        self.btn_cancel.setText(tr("button.cancel", "Cancel"))
        self.progress_frame.setVisible(True)

        self.download_thread = UpdateDownloadThread(installer_url, save_path)
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()

    def on_download_progress(self, downloaded: int, total: int, percent: float, speed_str: str):
        self.progress_bar.setValue(int(percent))
        dl_mb = downloaded / (1024 * 1024)
        tot_mb = total / (1024 * 1024) if total > 0 else 0
        if tot_mb > 0:
            self.lbl_status.setText(f"⏳ Downloading: {dl_mb:.1f} MB / {tot_mb:.1f} MB ({int(percent)}%) - {speed_str}")
        else:
            self.lbl_status.setText(f"⏳ Downloading: {dl_mb:.1f} MB - {speed_str}")

    def on_download_finished(self, file_path: str):
        self.downloaded_installer_path = file_path
        self.progress_bar.setValue(100)
        self.lbl_status.setText("✅ Download Complete! Click 'Install & Launch Setup' to apply update.")
        self.lbl_status.setStyleSheet("font-size: 12px; font-weight: 700; color: #10B981;")

        self.btn_action.setEnabled(True)
        self.btn_action.setText(tr("update.btn_install", "Install & Launch Setup"))
        self.btn_action.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 10px 20px;")

    def on_download_error(self, err_msg: str):
        self.lbl_status.setText(f"❌ Error: {err_msg}")
        self.lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #EF4444;")
        self.btn_action.setEnabled(True)
        self.btn_action.setText(tr("update.btn_retry", "Retry Download"))

    def install_and_restart(self):
        if not self.downloaded_installer_path or not os.path.exists(self.downloaded_installer_path):
            return

        try:
            if sys.platform == "win32":
                os.startfile(self.downloaded_installer_path)
            else:
                subprocess.Popen(["xdg-open", self.downloaded_installer_path], **_get_subproc_kwargs())

            QApplication.quit()
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Failed to launch installer: {e}")

    def closeEvent(self, event):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.cancel()
            self.download_thread.wait(1000)
        event.accept()
