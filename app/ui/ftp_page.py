import threading
from pathlib import Path
from typing import List, Dict, Any, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit,
    QSpinBox, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QObject

from app.services.ftp_service import FTPService
from app.core.scanner import ImageScanner
from app.core.image_info import ImageInfo
from app.utils.size_utils import format_size
from app.i18n.i18n_manager import tr


class FTPWorker(QObject):
    finished = Signal(list)
    progress = Signal(int, int, str)
    error = Signal(str)
    status_msg = Signal(str)

    def __init__(self, ftp_service: FTPService, conn_params: dict, action: str, remote_paths: Optional[List[str]] = None):
        super().__init__()
        self.ftp_service = ftp_service
        self.params = conn_params
        self.action = action
        self.remote_paths = remote_paths or []

    def run(self):
        try:
            ok, msg = self.ftp_service.connect(
                host=self.params["host"],
                port=self.params["port"],
                user=self.params["user"],
                password=self.params["password"],
                use_tls=self.params["use_tls"],
                passive=self.params["passive"]
            )
            if not ok:
                self.error.emit(msg)
                return

            if self.action == "test":
                self.finished.emit([])
                self.status_msg.emit(tr("ftp.status_connected", "Connected successfully!"))

            elif self.action == "scan":
                self.status_msg.emit(tr("ftp.status_scanning", "Scanning remote server..."))
                images = self.ftp_service.list_remote_images(self.params["remote_dir"])
                self.finished.emit(images)

            elif self.action == "download":
                self.status_msg.emit(tr("ftp.status_downloading", "Downloading images..."))
                downloaded_files = []
                total = len(self.remote_paths)
                for idx, r_path in enumerate(self.remote_paths):
                    self.progress.emit(idx + 1, total, Path(r_path).name)
                    local_path = self.ftp_service.download_file(r_path)
                    downloaded_files.append({
                        "remote_path": r_path,
                        "local_path": local_path
                    })
                self.finished.emit(downloaded_files)

        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.ftp_service.disconnect()


class FTPPage(QWidget):
    images_downloaded_for_processing = Signal(list, dict)  # (List[ImageInfo], ftp_config_for_autoupload)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ftp_service = FTPService()
        self.scanned_remote_images: List[Dict[str, Any]] = []
        self.downloaded_map: Dict[str, str] = {}  # local_path -> remote_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        self.title_label = QLabel(tr("ftp.title", "FTP Remote Optimization & Sync"))
        self.title_label.setStyleSheet("font-size: 20px; font-weight: 800; color: #818CF8;")
        
        self.subtitle_label = QLabel(tr("ftp.subtitle", "Connect directly to your FTP server, download images, optimize, and auto-upload processed results"))
        self.subtitle_label.setStyleSheet("font-size: 13px; color: #94A3B8; margin-bottom: 4px;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)

        # Config Box
        self.cfg_box = QGroupBox(tr("ftp.config_box", "FTP Server Connection Details"))
        cfg_layout = QVBoxLayout(self.cfg_box)

        r1 = QHBoxLayout()
        self.lbl_host = QLabel(tr("ftp.host", "Server Host:"))
        self.txt_host = QLineEdit()
        self.txt_host.setPlaceholderText("ftp.example.com")

        self.lbl_port = QLabel(tr("ftp.port", "Port:"))
        self.spn_port = QSpinBox()
        self.spn_port.setRange(1, 65535)
        self.spn_port.setValue(21)

        r1.addWidget(self.lbl_host)
        r1.addWidget(self.txt_host, 3)
        r1.addWidget(self.lbl_port)
        r1.addWidget(self.spn_port, 1)

        r2 = QHBoxLayout()
        self.lbl_user = QLabel(tr("ftp.user", "Username:"))
        self.txt_user = QLineEdit()

        self.lbl_pass = QLabel(tr("ftp.pass", "Password:"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)

        r2.addWidget(self.lbl_user)
        r2.addWidget(self.txt_user, 1)
        r2.addWidget(self.lbl_pass)
        r2.addWidget(self.txt_pass, 1)

        r3 = QHBoxLayout()
        self.lbl_dir = QLabel(tr("ftp.remote_dir", "Remote Directory Path:"))
        self.txt_dir = QLineEdit("/")

        self.chk_tls = QCheckBox(tr("ftp.use_tls", "Use Secure Connection (FTPS / TLS)"))
        self.chk_passive = QCheckBox(tr("ftp.passive", "Passive Mode"))
        self.chk_passive.setChecked(True)

        r3.addWidget(self.lbl_dir)
        r3.addWidget(self.txt_dir, 2)
        r3.addWidget(self.chk_tls)
        r3.addWidget(self.chk_passive)

        r4 = QHBoxLayout()
        self.btn_test = QPushButton(f"⚡ {tr('ftp.test_btn', 'Test Connection')}")
        self.btn_test.clicked.connect(self.test_connection)

        self.btn_scan = QPushButton(f"🔍 {tr('ftp.scan_btn', 'Scan Remote Images')}")
        self.btn_scan.setObjectName("PrimaryButton")
        self.btn_scan.clicked.connect(self.scan_remote_images)

        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("font-weight: 700; font-size: 13px;")

        r4.addWidget(self.btn_test)
        r4.addWidget(self.btn_scan)
        r4.addWidget(self.lbl_status, 1)

        cfg_layout.addLayout(r1)
        cfg_layout.addLayout(r2)
        cfg_layout.addLayout(r3)
        cfg_layout.addLayout(r4)

        layout.addWidget(self.cfg_box)

        # Table & Actions
        self.files_box = QGroupBox(tr("ftp.remote_files", "Remote Image Files Found"))
        files_layout = QVBoxLayout(self.files_box)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([
            tr("header.filename", "Filename"),
            tr("header.path", "Remote Path"),
            tr("header.size", "Size")
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        files_layout.addWidget(self.table)

        # Sync Options
        opt_layout = QHBoxLayout()
        self.chk_auto_upload = QCheckBox(tr("ftp.auto_upload", "Auto-upload optimized images back to FTP server"))
        self.chk_auto_upload.setChecked(True)

        self.btn_dl_process = QPushButton(f"🚀 {tr('ftp.download_optimize', 'Download & Send to Optimize Page')}")
        self.btn_dl_process.setObjectName("PrimaryButton")
        self.btn_dl_process.clicked.connect(self.download_and_process)

        opt_layout.addWidget(self.chk_auto_upload)
        opt_layout.addStretch()
        opt_layout.addWidget(self.btn_dl_process)

        files_layout.addLayout(opt_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        files_layout.addWidget(self.progress_bar)

        layout.addWidget(self.files_box)

    def get_conn_params(self) -> dict:
        return {
            "host": self.txt_host.text().strip(),
            "port": self.spn_port.value(),
            "user": self.txt_user.text().strip(),
            "password": self.txt_pass.text(),
            "remote_dir": self.txt_dir.text().strip() or "/",
            "use_tls": self.chk_tls.isChecked(),
            "passive": self.chk_passive.isChecked()
        }

    def test_connection(self):
        params = self.get_conn_params()
        if not params["host"]:
            QMessageBox.warning(self, "Error", "Please enter FTP server host.")
            return

        self.lbl_status.setText(f"⏳ {tr('ftp.status_testing', 'Testing connection...')}")
        self.lbl_status.setStyleSheet("color: #3B82F6;")

        self._start_worker(params, "test")

    def scan_remote_images(self):
        params = self.get_conn_params()
        if not params["host"]:
            QMessageBox.warning(self, "Error", "Please enter FTP server host.")
            return

        self.lbl_status.setText(f"⏳ {tr('ftp.status_scanning', 'Scanning remote server...')}")
        self.lbl_status.setStyleSheet("color: #3B82F6;")

        self._start_worker(params, "scan")

    def download_and_process(self):
        if not self.scanned_remote_images:
            QMessageBox.information(self, "Info", "No remote images available to download. Please scan first.")
            return

        params = self.get_conn_params()
        remote_paths = [img["remote_path"] for img in self.scanned_remote_images]

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText(f"⏳ {tr('ftp.status_downloading', 'Downloading images...')}")

        self._start_worker(params, "download", remote_paths)

    def _start_worker(self, params: dict, action: str, remote_paths: Optional[List[str]] = None):
        self._thread = threading.Thread(target=self._run_worker_thread, args=(params, action, remote_paths), daemon=True)
        self._thread.start()

    def _run_worker_thread(self, params: dict, action: str, remote_paths: Optional[List[str]]):
        worker = FTPWorker(self.ftp_service, params, action, remote_paths)
        worker.finished.connect(lambda res: self._on_worker_finished(action, res))
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_msg.connect(lambda msg: self.lbl_status.setText(msg))
        worker.run()

    def _on_worker_progress(self, current: int, total: int, filename: str):
        if total > 0:
            pct = int((current / total) * 100)
            self.progress_bar.setValue(pct)

    def _on_worker_error(self, err_msg: str):
        self.progress_bar.setVisible(False)
        self.lbl_status.setText(f"❌ {err_msg}")
        self.lbl_status.setStyleSheet("color: #EF4444;")

    def _on_worker_finished(self, action: str, results: list):
        self.progress_bar.setVisible(False)
        if action == "test":
            self.lbl_status.setText(f"✅ {tr('ftp.status_connected', 'Connected successfully!')}")
            self.lbl_status.setStyleSheet("color: #10B981;")

        elif action == "scan":
            self.scanned_remote_images = results
            self.lbl_status.setText(f"✅ Found {len(results)} remote images.")
            self.lbl_status.setStyleSheet("color: #10B981;")

            self.table.setRowCount(0)
            for img in results:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(img["name"]))
                self.table.setItem(row, 1, QTableWidgetItem(img["remote_path"]))
                self.table.setItem(row, 2, QTableWidgetItem(format_size(img["size"])))

        elif action == "download":
            self.lbl_status.setText(f"✅ Downloaded {len(results)} images.")
            self.lbl_status.setStyleSheet("color: #10B981;")

            scanner = ImageScanner()
            image_infos = []
            for item in results:
                l_path = item["local_path"]
                r_path = item["remote_path"]
                self.downloaded_map[str(l_path)] = r_path
                info = scanner.scan_path(l_path)
                if info:
                    image_infos.extend(info)

            ftp_config = {
                "auto_upload": self.chk_auto_upload.isChecked(),
                "params": self.get_conn_params(),
                "map": self.downloaded_map
            }

            self.images_downloaded_for_processing.emit(image_infos, ftp_config)

    def retranslate_ui(self):
        self.title_label.setText(tr("ftp.title", "FTP Remote Optimization & Sync"))
        self.subtitle_label.setText(tr("ftp.subtitle", "Connect directly to your FTP server, download images, optimize, and auto-upload processed results"))
        self.cfg_box.setTitle(tr("ftp.config_box", "FTP Server Connection Details"))
        self.lbl_host.setText(tr("ftp.host", "Server Host:"))
        self.lbl_port.setText(tr("ftp.port", "Port:"))
        self.lbl_user.setText(tr("ftp.user", "Username:"))
        self.lbl_pass.setText(tr("ftp.pass", "Password:"))
        self.lbl_dir.setText(tr("ftp.remote_dir", "Remote Directory Path:"))
        self.chk_tls.setText(tr("ftp.use_tls", "Use Secure Connection (FTPS / TLS)"))
        self.chk_passive.setText(tr("ftp.passive", "Passive Mode"))
        self.btn_test.setText(f"⚡ {tr('ftp.test_btn', 'Test Connection')}")
        self.btn_scan.setText(f"🔍 {tr('ftp.scan_btn', 'Scan Remote Images')}")
        self.files_box.setTitle(tr("ftp.remote_files", "Remote Image Files Found"))
        self.chk_auto_upload.setText(tr("ftp.auto_upload", "Auto-upload optimized images back to FTP server"))
        self.btn_dl_process.setText(f"🚀 {tr('ftp.download_optimize', 'Download & Send to Optimize Page')}")
