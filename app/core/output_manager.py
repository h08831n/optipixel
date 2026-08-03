from pathlib import Path
from typing import Optional
from app.config.constants import (
    OUTPUT_MODE_REPLACE,
    OUTPUT_MODE_FOLDER,
    OUTPUT_MODE_NEXT_TO_ORIGINAL
)
from app.core.formats import ImageFormat

class OutputManager:
    def __init__(
        self,
        mode: str = OUTPUT_MODE_FOLDER,
        output_folder: Optional[Path] = None,
        base_input_folder: Optional[Path] = None,
        preserve_structure: bool = True,
        collision_strategy: str = "skip"
    ):
        self.mode = mode
        self.output_folder = Path(output_folder) if output_folder else None
        self.base_input_folder = Path(base_input_folder) if base_input_folder else None
        self.preserve_structure = preserve_structure
        self.collision_strategy = collision_strategy

    def resolve_output_path(self, source_path: Path, target_format: ImageFormat) -> Path:
        target_ext = target_format.to_extension()

        if self.mode == OUTPUT_MODE_REPLACE:
            if target_format == ImageFormat.ORIGINAL:
                return source_path
            return source_path.with_suffix(target_ext)

        elif self.mode == OUTPUT_MODE_NEXT_TO_ORIGINAL:
            new_name = f"{source_path.stem}_optimized{target_ext}"
            return source_path.parent / new_name

        elif self.mode == OUTPUT_MODE_FOLDER:
            if not self.output_folder:
                raise ValueError("Output folder must be specified for 'folder' mode.")

            if self.preserve_structure and self.base_input_folder and source_path.is_relative_to(self.base_input_folder):
                rel_path = source_path.relative_to(self.base_input_folder)
                target_path = self.output_folder / rel_path.with_suffix(target_ext)
            else:
                target_path = self.output_folder / source_path.name
                target_path = target_path.with_suffix(target_ext)

            target_path.parent.mkdir(parents=True, exist_ok=True)
            return target_path

        return source_path.with_suffix(target_ext)

    def handle_collision(self, target_path: Path) -> Path:
        if not target_path.exists():
            return target_path

        if self.collision_strategy == "overwrite":
            return target_path
        elif self.collision_strategy == "rename":
            count = 1
            stem = target_path.stem
            ext = target_path.suffix
            parent = target_path.parent
            while True:
                candidate = parent / f"{stem}_{count}{ext}"
                if not candidate.exists():
                    return candidate
                count += 1

        return target_path
