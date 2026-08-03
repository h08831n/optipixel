from app.core.formats import ImageFormat

def test_format_from_extension():
    assert ImageFormat.from_extension("jpg") == ImageFormat.JPEG
    assert ImageFormat.from_extension(".JPEG") == ImageFormat.JPEG
    assert ImageFormat.from_extension("webp") == ImageFormat.WEBP
    assert ImageFormat.from_extension("avif") == ImageFormat.AVIF
    assert ImageFormat.from_extension("png") == ImageFormat.PNG

def test_format_to_extension():
    assert ImageFormat.WEBP.to_extension() == ".webp"
    assert ImageFormat.JPEG.to_extension() == ".jpg"
    assert ImageFormat.AVIF.to_extension() == ".avif"
