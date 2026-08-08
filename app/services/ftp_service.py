import os
import tempfile
from pathlib import Path
from ftplib import FTP, FTP_TLS
from typing import List, Dict, Any, Callable, Optional, Tuple


class FTPService:
    def __init__(self):
        self.ftp: Optional[FTP] = None
        self.temp_dir = Path(tempfile.gettempdir()) / "optipixel_ftp_cache"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def connect(self, host: str, port: int = 21, user: str = "", password: str = "", use_tls: bool = False, passive: bool = True, timeout: int = 15) -> Tuple[bool, str]:
        self.disconnect()
        try:
            if use_tls:
                self.ftp = FTP_TLS(timeout=timeout)
                self.ftp.connect(host=host, port=port)
                self.ftp.auth()
                if user:
                    self.ftp.login(user=user, passwd=password)
                else:
                    self.ftp.login()
                self.ftp.prot_p()
            else:
                self.ftp = FTP(timeout=timeout)
                self.ftp.connect(host=host, port=port)
                if user:
                    self.ftp.login(user=user, passwd=password)
                else:
                    self.ftp.login()

            self.ftp.set_pasv(passive)
            return True, "Connected successfully"
        except Exception as e:
            self.ftp = None
            return False, str(e)

    def disconnect(self):
        if self.ftp:
            try:
                self.ftp.quit()
            except Exception:
                try:
                    self.ftp.close()
                except Exception:
                    pass
            self.ftp = None

    def list_remote_images(self, remote_dir: str, recursive: bool = True) -> List[Dict[str, Any]]:
        if not self.ftp:
            raise RuntimeError("FTP client is not connected")

        IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic", ".heif", ".bmp", ".tiff", ".tif", ".gif"}
        images = []

        def _scan_dir(current_dir: str):
            try:
                entries = []
                self.ftp.retrlines(f"LIST {current_dir}", entries.append)
            except Exception:
                return

            for entry in entries:
                parts = entry.split()
                if not parts:
                    continue
                name = parts[-1]
                if name in (".", ".."):
                    continue

                is_dir = entry.startswith("d") or (len(parts) > 2 and "<DIR>" in entry)
                full_remote_path = f"{current_dir.rstrip('/')}/{name}"

                if is_dir and recursive:
                    _scan_dir(full_remote_path)
                elif not is_dir:
                    ext = Path(name).suffix.lower()
                    if ext in IMAGE_EXTS:
                        # Try parsing file size if available
                        size = 0
                        try:
                            size = self.ftp.size(full_remote_path) or 0
                        except Exception:
                            pass
                        images.append({
                            "name": name,
                            "remote_path": full_remote_path,
                            "size": size
                        })

        clean_dir = remote_dir.strip() if remote_dir else "/"
        if not clean_dir.startswith("/"):
            clean_dir = "/" + clean_dir
        _scan_dir(clean_dir)
        return images

    def download_file(self, remote_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> Path:
        if not self.ftp:
            raise RuntimeError("FTP client is not connected")

        filename = Path(remote_path).name
        local_path = self.temp_dir / filename
        
        total_size = 0
        try:
            total_size = self.ftp.size(remote_path) or 0
        except Exception:
            pass

        downloaded = 0

        with open(local_path, "wb") as f:
            def _callback(chunk: bytes):
                nonlocal downloaded
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total_size)

            self.ftp.retrbinary(f"RETR {remote_path}", _callback)

        return local_path

    def upload_file(self, local_path: Path, remote_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> bool:
        if not self.ftp:
            raise RuntimeError("FTP client is not connected")

        # Ensure directory exists on remote if possible
        remote_dir = str(Path(remote_path).parent).replace("\\", "/")
        try:
            self.ensure_remote_dir(remote_dir)
        except Exception:
            pass

        total_size = local_path.stat().st_size
        uploaded = 0

        with open(local_path, "rb") as f:
            def _callback(chunk: bytes):
                nonlocal uploaded
                uploaded += len(chunk)
                if progress_callback:
                    progress_callback(uploaded, total_size)

            self.ftp.storbinary(f"STOR {remote_path}", f, callback=_callback)

        return True

    def ensure_remote_dir(self, remote_dir: str):
        if not self.ftp or not remote_dir or remote_dir == "/":
            return

        parts = [p for p in remote_dir.split("/") if p]
        current = ""
        for part in parts:
            current += "/" + part
            try:
                self.ftp.cwd(current)
            except Exception:
                try:
                    self.ftp.mkd(current)
                except Exception:
                    pass
