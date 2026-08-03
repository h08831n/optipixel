import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from app.core.formats import ImageFormat

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

@dataclass
class ImageInfo:
    file_path: Path
    file_size_bytes: int
    width: int
    height: int
    format: ImageFormat
    mime_type: str
    has_alpha: bool = False
    color_space: str = "sRGB"

    @property
    def file_size_kb(self) -> float:
        return self.file_size_bytes / 1024.0

    @property
    def file_size_mb(self) -> float:
        return self.file_size_bytes / (1024.0 * 1024.0)

    @classmethod
    def extract(cls, file_path: Path) -> 'ImageInfo':
        size = file_path.stat().st_size if file_path.exists() else 0
        fmt = ImageFormat.from_extension(file_path.suffix)
        width, height = 0, 0
        has_alpha = False
        mime_type = f"image/{fmt.value.lower()}"

        if HAS_PIL and file_path.exists():
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
                    color_space = img.mode
            except Exception:
                pass

        return cls(
            file_path=file_path,
            file_size_bytes=size,
            width=width,
            height=height,
            format=fmt,
            mime_type=mime_type,
            has_alpha=has_alpha
        )
