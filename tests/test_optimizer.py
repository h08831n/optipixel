import unittest
from pathlib import Path
from app.services.imagemagick_service import ImageMagickService
from app.core.optimizer import ImageOptimizer
from app.core.formats import ImageFormat

class TestOptimizer(unittest.TestCase):
    def test_optimizer_threshold(self):
        small_file = Path("small_test.jpg")
        small_file.write_bytes(b"0" * 50 * 1024)

        try:
            im_service = ImageMagickService()
            optimizer = ImageOptimizer(im_service)

            settings = {
                "threshold_enabled": True,
                "size_threshold_kb": 400
            }

            success, out_path, msg = optimizer.optimize(small_file, ImageFormat.WEBP, settings)
            self.assertFalse(success)
            self.assertIn("Skipped", msg)
        finally:
            if small_file.exists():
                small_file.unlink()

if __name__ == "__main__":
    unittest.main()
