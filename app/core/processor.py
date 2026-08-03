import shutil
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.imagemagick_service import ImageMagickService

from app.core.optimizer import ImageOptimizer
from app.core.output_manager import OutputManager
from app.core.backup_manager import BackupManager
from app.core.formats import ImageFormat
from app.core.image_info import ImageInfo
from app.config.constants import OUTPUT_MODE_REPLACE

@dataclass
class ProcessingResult:
    source_path: Path
    output_path: Path = Path("")
    original_size_bytes: int = 0
    new_size_bytes: int = 0
    original_format: ImageFormat = ImageFormat.UNKNOWN
    output_format: ImageFormat = ImageFormat.UNKNOWN
    width: int = 0
    height: int = 0
    status: str = "failed"  # "optimized", "converted", "skipped", "failed"
    message: str = ""
    duration_seconds: float = 0.0
    backup_path: Optional[Path] = None

    @property
    def saved_bytes(self) -> int:
        if self.status in ("optimized", "converted") and self.new_size_bytes < self.original_size_bytes:
            return self.original_size_bytes - self.new_size_bytes
        return 0

    @property
    def reduction_percentage(self) -> float:
        if self.original_size_bytes > 0 and self.saved_bytes > 0:
            return (self.saved_bytes / self.original_size_bytes) * 100.0
        return 0.0

class ImageProcessor:
    def __init__(
        self,
        im_service: 'ImageMagickService',
        backup_manager: Optional[BackupManager] = None
    ):
        self.im_service = im_service
        self.optimizer = ImageOptimizer(im_service)
        self.backup_manager = backup_manager or BackupManager()

    def process_single(
        self,
        image_info: ImageInfo,
        target_format: ImageFormat,
        settings: Dict[str, Any],
        output_manager: OutputManager
    ) -> ProcessingResult:
        start_time = time.time()
        src_path = image_info.file_path
        src_size = image_info.file_size_bytes

        actual_target_fmt = target_format if target_format != ImageFormat.ORIGINAL else image_info.format

        if settings.get("skip_already_target_format", False) and image_info.format == actual_target_fmt:
            return ProcessingResult(
                source_path=src_path,
                output_path=src_path,
                original_size_bytes=src_size,
                new_size_bytes=src_size,
                original_format=image_info.format,
                output_format=actual_target_fmt,
                width=image_info.width,
                height=image_info.height,
                status="skipped",
                message="Skipped: Already in target format",
                duration_seconds=time.time() - start_time
            )

        try:
            final_output_path = output_manager.resolve_output_path(src_path, actual_target_fmt)
            final_output_path = output_manager.handle_collision(final_output_path)
        except Exception as e:
            return ProcessingResult(
                source_path=src_path,
                output_path=src_path,
                original_size_bytes=src_size,
                new_size_bytes=src_size,
                original_format=image_info.format,
                output_format=actual_target_fmt,
                width=image_info.width,
                height=image_info.height,
                status="failed",
                message=f"Path resolution error: {e}",
                duration_seconds=time.time() - start_time
            )

        success, temp_output_path, msg = self.optimizer.optimize(src_path, actual_target_fmt, settings)

        if not success:
            return ProcessingResult(
                source_path=src_path,
                output_path=final_output_path,
                original_size_bytes=src_size,
                new_size_bytes=src_size,
                original_format=image_info.format,
                output_format=actual_target_fmt,
                width=image_info.width,
                height=image_info.height,
                status="skipped" if "Skipped" in msg else "failed",
                message=msg,
                duration_seconds=time.time() - start_time
            )

        new_size = temp_output_path.stat().st_size
        backup_created: Optional[Path] = None

        try:
            if output_manager.mode == OUTPUT_MODE_REPLACE:
                if settings.get("backup", {}).get("enabled", True):
                    backup_created = self.backup_manager.create_backup(src_path)

                shutil.move(str(temp_output_path), str(final_output_path))
            else:
                final_output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(temp_output_path), str(final_output_path))

            out_info = ImageInfo.extract(final_output_path)
            status_str = "converted" if image_info.format != actual_target_fmt else "optimized"

            return ProcessingResult(
                source_path=src_path,
                output_path=final_output_path,
                original_size_bytes=src_size,
                new_size_bytes=new_size,
                original_format=image_info.format,
                output_format=actual_target_fmt,
                width=out_info.width or image_info.width,
                height=out_info.height or image_info.height,
                status=status_str,
                message="Successfully processed",
                duration_seconds=time.time() - start_time,
                backup_path=backup_created
            )

        except Exception as e:
            if temp_output_path.exists():
                temp_output_path.unlink()
            return ProcessingResult(
                source_path=src_path,
                output_path=final_output_path,
                original_size_bytes=src_size,
                new_size_bytes=src_size,
                original_format=image_info.format,
                output_format=actual_target_fmt,
                width=image_info.width,
                height=image_info.height,
                status="failed",
                message=f"Output placement error: {e}",
                duration_seconds=time.time() - start_time
            )
