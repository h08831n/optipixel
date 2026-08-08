import subprocess
import shutil
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from app.core.exceptions import ImageMagickNotFoundError

def _subproc_kwargs() -> dict:
    kwargs = {}
    if sys.platform == "win32" or os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    return kwargs

class ImageMagickService:
    def __init__(self, custom_path: Optional[str] = None):
        self.executable = self._detect_executable(custom_path)
        self.version_info = self._get_version()
        self.supported_formats = self._detect_formats()

    def _is_valid_imagemagick(self, exe: str) -> bool:
        if not exe:
            return False
        # Do not use Windows system convert.exe
        if os.name == "nt" and "system32" in exe.lower() and "convert.exe" in exe.lower():
            return False
        try:
            res = subprocess.run([exe, "-version"], capture_output=True, text=True, timeout=3, **_subproc_kwargs())
            if res.returncode == 0 and "imagemagick" in res.stdout.lower():
                return True
            res2 = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=3, **_subproc_kwargs())
            if res2.returncode == 0 and "imagemagick" in res2.stdout.lower():
                return True
        except Exception:
            pass
        return False

    def _detect_executable(self, custom_path: Optional[str] = None) -> str:
        # 1. Check custom path if provided
        if custom_path and self._is_valid_imagemagick(custom_path):
            return custom_path

        # 2. Check PATH for 'magick'
        magick_path = shutil.which("magick")
        if magick_path and self._is_valid_imagemagick(magick_path):
            return magick_path

        # 3. Check PATH for 'convert' (fallback for Linux/Mac or older ImageMagick)
        convert_path = shutil.which("convert")
        if convert_path and self._is_valid_imagemagick(convert_path):
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
                    if cmd.exists() and self._is_valid_imagemagick(str(cmd)):
                        return str(cmd)

        return ""

    def is_available(self) -> bool:
        return bool(self.executable and (Path(self.executable).exists() or shutil.which(self.executable)) and self._is_valid_imagemagick(self.executable))

    def _get_version(self) -> str:
        if not self.executable:
            return "Not Installed"
        try:
            res = subprocess.run([self.executable, "--version"], capture_output=True, text=True, timeout=5, **_subproc_kwargs())
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
            # Standard formats natively supported by Pillow engine even without ImageMagick
            return {
                "WEBP": True,
                "AVIF": True,
                "HEIC": True,
                "JPEG": True,
                "PNG": True,
                "TIFF": True,
                "BMP": True,
                "GIF": True,
                "JPEG_XL": False
            }

        try:
            res = subprocess.run([self.executable, "-list", "format"], capture_output=True, text=True, timeout=10, **_subproc_kwargs())
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
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **_subproc_kwargs())
            return res.returncode == 0, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Operation timed out after {timeout} seconds"
        except Exception as e:
            return False, "", str(e)
