from pathlib import Path
from app.core.output_manager import OutputManager
from app.core.formats import ImageFormat
from app.config.constants import OUTPUT_MODE_REPLACE, OUTPUT_MODE_FOLDER, OUTPUT_MODE_NEXT_TO_ORIGINAL

def test_output_manager_replace():
    out_mgr = OutputManager(mode=OUTPUT_MODE_REPLACE)
    src = Path("/images/photo.jpg")
    res = out_mgr.resolve_output_path(src, ImageFormat.WEBP)
    assert res == Path("/images/photo.webp")

def test_output_manager_next_to_original():
    out_mgr = OutputManager(mode=OUTPUT_MODE_NEXT_TO_ORIGINAL)
    src = Path("/images/photo.jpg")
    res = out_mgr.resolve_output_path(src, ImageFormat.WEBP)
    assert res == Path("/images/photo_optimized.webp")

def test_output_manager_folder_preserve_structure():
    out_dir = Path("/output")
    base_dir = Path("/images")
    out_mgr = OutputManager(
        mode=OUTPUT_MODE_FOLDER,
        output_folder=out_dir,
        base_input_folder=base_dir,
        preserve_structure=True
    )
    src = Path("/images/2026/08/photo.jpg")
    res = out_mgr.resolve_output_path(src, ImageFormat.WEBP)
    assert res == Path("/output/2026/08/photo.webp")
