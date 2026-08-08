from enum import Enum, auto
from typing import Dict, List, Optional

class ImageFormat(Enum):
    ORIGINAL = "ORIGINAL"
    WEBP = "WEBP"
    AVIF = "AVIF"
    JPEG = "JPEG"
    PNG = "PNG"
    TIFF = "TIFF"
    BMP = "BMP"
    HEIC = "HEIC"
    JXL = "JXL"
    GIF = "GIF"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_extension(cls, ext: str) -> 'ImageFormat':
        ext = ext.lower().lstrip('.')
        mapping = {
            'original': cls.ORIGINAL,
            'jpg': cls.JPEG,
            'jpeg': cls.JPEG,
            'jfif': cls.JPEG,
            'pjpeg': cls.JPEG,
            'pjp': cls.JPEG,
            'png': cls.PNG,
            'webp': cls.WEBP,
            'avif': cls.AVIF,
            'heic': cls.HEIC,
            'heif': cls.HEIC,
            'tif': cls.TIFF,
            'tiff': cls.TIFF,
            'bmp': cls.BMP,
            'gif': cls.GIF,
            'jxl': cls.JXL
        }
        return mapping.get(ext, cls.UNKNOWN)

    def to_extension(self) -> str:
        ext_map = {
            ImageFormat.ORIGINAL: "",
            ImageFormat.WEBP: ".webp",
            ImageFormat.AVIF: ".avif",
            ImageFormat.JPEG: ".jpg",
            ImageFormat.PNG: ".png",
            ImageFormat.TIFF: ".tif",
            ImageFormat.BMP: ".bmp",
            ImageFormat.HEIC: ".heic",
            ImageFormat.JXL: ".jxl",
            ImageFormat.GIF: ".gif"
        }
        return ext_map.get(self, ".jpg")
