from app.services.imagemagick_service import ImageMagickService
from app.core.converter import ImageConverter
from app.core.formats import ImageFormat

def test_converter_initialization():
    im_service = ImageMagickService()
    converter = ImageConverter(im_service)
    assert converter is not None
