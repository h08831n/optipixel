class OptiPixelException(Exception):
    """Base exception class for OptiPixel."""
    pass

class ImageMagickNotFoundError(OptiPixelException):
    """Raised when ImageMagick executable is not found."""
    pass

class ImageProcessingError(OptiPixelException):
    """Raised when image optimization or conversion fails."""
    pass

class InvalidImageError(OptiPixelException):
    """Raised when the target file is not a valid image."""
    pass

class UnsupportedFormatError(OptiPixelException):
    """Raised when requested target format is unsupported by detected ImageMagick delegates."""
    pass
