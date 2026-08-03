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
from app.utils.logging_utils import get_logger

logger = get_logger()

try:
    from PIL import Image as PILImage, ImageOps
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

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

    def _optimize_with_pillow(
        self,
        input_path: Path,
        temp_output: Path,
        target_format: ImageFormat,
        settings: Dict[str, Any]
    ) -> Tuple[bool, str]:
        if not HAS_PILLOW:
            return False, "Pillow library is not installed"

        try:
            with PILImage.open(input_path) as img:
                try:
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                save_ext = target_format.to_extension().lstrip(".").upper() if target_format != ImageFormat.ORIGINAL else input_path.suffix.lstrip(".").upper()
                if save_ext in ("JPG", "JPEG"):
                    save_fmt = "JPEG"
                else:
                    save_fmt = save_ext

                # Handle color modes
                if save_fmt == "JPEG" and img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")
                elif save_fmt == "WEBP" and img.mode in ("P", "LA"):
                    img = img.convert("RGBA")

                # Resize logic
                if settings.get("enable_resize", False):
                    max_w = settings.get("max_width", 2000)
                    max_h = settings.get("max_height", 2000)
                    only_shrink = settings.get("only_shrink", True)
                    
                    cur_w, cur_h = img.size
                    should_resize = True
                    if only_shrink and cur_w <= max_w and cur_h <= max_h:
                        should_resize = False

                    if should_resize:
                        img.thumbnail((max_w, max_h), PILImage.Resampling.LANCZOS)

                quality = settings.get("quality", 82)
                save_kwargs = {}

                if save_fmt == "WEBP":
                    save_kwargs["quality"] = quality
                    save_kwargs["method"] = 6
                elif save_fmt == "JPEG":
                    save_kwargs["quality"] = quality
                    save_kwargs["optimize"] = True
                    save_kwargs["progressive"] = True
                elif save_fmt == "PNG":
                    save_kwargs["optimize"] = True

                temp_output.parent.mkdir(parents=True, exist_ok=True)
                img.save(temp_output, format=save_fmt, **save_kwargs)
                if temp_output.exists() and temp_output.stat().st_size > 0:
                    return True, "Successfully processed with Pillow"
                return False, "Pillow produced empty file"
        except Exception as e:
            return False, f"Pillow processing error: {e}"

    def optimize(
        self,
        input_path: Path,
        target_format: ImageFormat,
        settings: Dict[str, Any]
    ) -> Tuple[bool, Path, str]:
        logger.debug(f"Starting optimization for file: {input_path} -> target_format: {target_format.value}")
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_path}")
            return False, input_path, "File does not exist"

        # Check threshold
        src_size_bytes = input_path.stat().st_size
        src_size_kb = src_size_bytes / 1024.0

        if settings.get("threshold_enabled", True):
            min_threshold_kb = settings.get("size_threshold_kb", 400)
            if src_size_kb <= min_threshold_kb:
                msg = f"Skipped: File size ({src_size_kb:.1f} KB) <= threshold ({min_threshold_kb} KB)"
                logger.info(f"{input_path.name}: {msg}")
                return False, input_path, msg

        # Create temporary file for processing
        target_ext = target_format.to_extension() if target_format != ImageFormat.ORIGINAL else input_path.suffix
        temp_dir = Path(tempfile.gettempdir()) / "optipixel_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_output = temp_dir / f"temp_{os.urandom(8).hex()}{target_ext}"

        actual_format = target_format if target_format != ImageFormat.ORIGINAL else ImageFormat.from_extension(input_path.suffix)

        # 1. Try ImageMagick if available
        im_error_msg = ""
        if self.im_service.is_available():
            args = self.build_command_args(input_path, temp_output, actual_format, settings)
            logger.debug(f"Executing ImageMagick with args: {args}")
            try:
                success, stdout, stderr = self.im_service.execute(args)
                if success and temp_output.exists() and temp_output.stat().st_size > 0:
                    opt_size_bytes = temp_output.stat().st_size
                    if settings.get("keep_original_if_larger", True) and opt_size_bytes >= src_size_bytes:
                        temp_output.unlink()
                        msg = f"Skipped: Optimized file ({opt_size_bytes/1024:.1f} KB) >= Original ({src_size_kb:.1f} KB)"
                        logger.info(f"{input_path.name}: {msg}")
                        return False, input_path, msg
                    logger.info(f"ImageMagick successfully optimized {input_path.name} -> {opt_size_bytes/1024:.1f} KB")
                    return True, temp_output, "Successfully optimized"
                else:
                    im_error_msg = stderr or "Empty output"
                    logger.warning(f"ImageMagick execution failed for {input_path.name}: {im_error_msg}")
            except Exception as e:
                im_error_msg = str(e)
                logger.warning(f"ImageMagick exception for {input_path.name}: {im_error_msg}")

        # 2. Fallback to Pillow
        logger.info(f"Using Pillow fallback for {input_path.name}...")
        pil_ok, pil_msg = self._optimize_with_pillow(input_path, temp_output, actual_format, settings)
        if pil_ok:
            opt_size_bytes = temp_output.stat().st_size
            if settings.get("keep_original_if_larger", True) and opt_size_bytes >= src_size_bytes:
                if temp_output.exists():
                    temp_output.unlink()
                msg = f"Skipped: Optimized file ({opt_size_bytes/1024:.1f} KB) >= Original ({src_size_kb:.1f} KB)"
                logger.info(f"{input_path.name}: {msg}")
                return False, input_path, msg
            logger.info(f"Pillow successfully processed {input_path.name} -> {opt_size_bytes/1024:.1f} KB")
            return True, temp_output, "Successfully optimized (Pillow engine)"

        if temp_output.exists():
            temp_output.unlink()

        err_detail = im_error_msg or pil_msg or "Unknown error"
        logger.error(f"Processing failed for {input_path.name}: {err_detail}")
        return False, input_path, f"Processing failed: {err_detail}"

