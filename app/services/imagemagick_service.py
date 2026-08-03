import subprocess
import shutil
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from app.core.exceptions import ImageMagickNotFoundError

class ImageMagickService:
    def __init__(self, custom_path: Optional[str] = None):
        self.executable = self._detect_executable(custom_path)
        self.version_info = self._get_version()
        self.supported_formats = self._detect_formats()

    def _detect_executable(self, custom_path: Optional[str] = None) -> str:
        # 1. Check custom path if provided
        if custom_path and Path(custom_path).exists():
            return custom_path

        # 2. Check PATH for 'magick'
        magick_path = shutil.which("magick")
        if magick_path:
            return magick_path

        # 3. Check PATH for 'convert' (fallback for Linux/Mac or older ImageMagick)
        convert_path = shutil.which("convert")
        if convert_path:
            return convert_path

        # 4. Check Common Windows Installation Paths
        program_files = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        ]
        for pf in program_files:
            if not pf:
                continue
            im_dir = Path(pf)
            if im_dir.exists():
                for sub in im_dir.glob("ImageMagick*"):
                    cmd = sub / "magick.exe"
                    if cmd.exists():
                        return str(cmd)

        return ""

    def is_available(self) -> bool:
        return bool(self.executable and Path(self.executable).exists() or shutil.which(self.executable))

    def _get_version(self) -> str:
        if not self.executable:
            return "Not Installed"
        try:
            res = subprocess.run([self.executable, "--version"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                first_line = res.stdout.splitlines()[0] if res.stdout else ""
                return first_line
        except Exception:
            pass
        return "Unknown"

    def _detect_formats(self) -> Dict[str, bool]:
        formats = {
            "WEBP": False,
            "AVIF": False,
            "HEIC": False,
            "JPEG": False,
            "PNG": False,
            "TIFF": False,
            "BMP": False,
            "GIF": False,
            "JPEG_XL": False
        }
        if not self.is_available():
            return formats

        try:
            res = subprocess.run([self.executable, "-list", "format"], capture_output=True, text=True, timeout=10)
            output = res.stdout.upper() if res.returncode == 0 else ""
            
            formats["WEBP"] = "WEBP" in output
            formats["AVIF"] = "AVIF" in output or "HEIC" in output
            formats["HEIC"] = "HEIC" in output
            formats["JPEG"] = "JPEG" in output or "JPG" in output
            formats["PNG"] = "PNG" in output
            formats["TIFF"] = "TIFF" in output
            formats["BMP"] = "BMP" in output
            formats["GIF"] = "GIF" in output
            formats["JPEG_XL"] = "JXL" in output or "JPEG-XL" in output
        except Exception:
            # Fallback assumption for standard ImageMagick builds
            formats["JPEG"] = True
            formats["PNG"] = True
            formats["WEBP"] = True
            formats["BMP"] = True
            formats["TIFF"] = True

        return formats

    def execute(self, args: List[str], timeout: int = 60) -> Tuple[bool, str, str]:
        if not self.is_available():
            raise ImageMagickNotFoundError("ImageMagick executable not found. Please install ImageMagick 7+.")

        cmd = [self.executable] + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return res.returncode == 0, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Operation timed out after {timeout} seconds"
        except Exception as e:
            return False, "", str(e)
