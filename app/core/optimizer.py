import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.imagemagick_service import ImageMagickService

from app.core.formats import ImageFormat
from app.core.image_info import ImageInfo
from app.core.exceptions import ImageProcessingError, UnsupportedFormatError

class ImageOptimizer:
    def __init__(self, im_service: 'ImageMagickService'):
        self.im_service = im_service

    def build_command_args(
        self,
        input_path: Path,
        temp_output_path: Path,
        target_format: ImageFormat,
        settings: Dict[str, Any]
    ) -> list:
        args = [str(input_path)]

        # Strip metadata
        if settings.get("strip_metadata", True):
            args.append("-strip")

        # Resize
        if settings.get("enable_resize", False):
            max_w = settings.get("max_width", 2000)
            max_h = settings.get("max_height", 2000)
            only_shrink = settings.get("only_shrink", True)
            resize_str = f"{max_w}x{max_h}"
            if only_shrink:
                resize_str += ">"
            if not settings.get("keep_aspect_ratio", True):
                resize_str += "!"
            args.extend(["-resize", resize_str])

        # Format-specific quality settings
        quality = settings.get("quality", 82)

        if target_format in (ImageFormat.WEBP, ImageFormat.JPEG, ImageFormat.AVIF):
            args.extend(["-quality", str(quality)])

        if target_format == ImageFormat.WEBP:
            if settings.get("webp_mode") == "lossless":
                args.extend(["-define", "webp:lossless=true"])
            else:
                args.extend(["-define", "webp:method=6"])

        elif target_format == ImageFormat.JPEG:
            args.extend(["-interlace", "JPEG", "-sampling-factor", "4:2:0"])

        elif target_format == ImageFormat.PNG:
            args.extend(["-quality", "95"])

        args.append(str(temp_output_path))
        return args

    def optimize(
        self,
        input_path: Path,
        target_format: ImageFormat,
        settings: Dict[str, Any]
    ) -> Tuple[bool, Path, str]:
        if not input_path.exists():
            return False, input_path, "File does not exist"

        # Check threshold
        src_size_bytes = input_path.stat().st_size
        src_size_kb = src_size_bytes / 1024.0

        if settings.get("threshold_enabled", True):
            min_threshold_kb = settings.get("size_threshold_kb", 400)
            if src_size_kb <= min_threshold_kb:
                return False, input_path, f"Skipped: File size ({src_size_kb:.1f} KB) <= threshold ({min_threshold_kb} KB)"

        # Create temporary file for processing
        target_ext = target_format.to_extension() if target_format != ImageFormat.ORIGINAL else input_path.suffix
        temp_dir = Path(tempfile.gettempdir()) / "optipixel_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_output = temp_dir / f"temp_{os.urandom(8).hex()}{target_ext}"

        actual_format = target_format if target_format != ImageFormat.ORIGINAL else ImageFormat.from_extension(input_path.suffix)

        args = self.build_command_args(input_path, temp_output, actual_format, settings)

        try:
            success, stdout, stderr = self.im_service.execute(args)
            if not success or not temp_output.exists() or temp_output.stat().st_size == 0:
                if temp_output.exists():
                    temp_output.unlink()
                return False, input_path, f"ImageMagick failed: {stderr or 'Empty output'}"

            opt_size_bytes = temp_output.stat().st_size

            # Check if output is larger
            if settings.get("keep_original_if_larger", True) and opt_size_bytes >= src_size_bytes:
                temp_output.unlink()
                return False, input_path, f"Skipped: Optimized file ({opt_size_bytes/1024:.1f} KB) >= Original ({src_size_kb:.1f} KB)"

            return True, temp_output, "Successfully optimized"

        except Exception as e:
            if temp_output.exists():
                temp_output.unlink()
            return False, input_path, f"Processing exception: {str(e)}"
