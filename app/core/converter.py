from pathlib import Path
from typing import Dict, Any, Tuple, TYPE_CHECKING
from app.core.formats import ImageFormat
from app.core.optimizer import ImageOptimizer

if TYPE_CHECKING:
    from app.services.imagemagick_service import ImageMagickService

class ImageConverter:
    def __init__(self, im_service: 'ImageMagickService'):
        self.optimizer = ImageOptimizer(im_service)

    def convert(
        self,
        input_path: Path,
        target_format: ImageFormat,
        settings: Dict[str, Any]
    ) -> Tuple[bool, Path, str]:
        conv_settings = settings.copy()
        conv_settings["threshold_enabled"] = False
        conv_settings["keep_original_if_larger"] = False
        return self.optimizer.optimize(input_path, target_format, conv_settings)
