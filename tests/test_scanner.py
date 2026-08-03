import unittest
from pathlib import Path
from app.core.scanner import ImageScanner
from app.core.formats import ImageFormat

class TestScanner(unittest.TestCase):
    def test_scanner_valid_file(self):
        img_file = Path("test_dummy.jpg")
        img_file.write_bytes(b"fake image data")
        try:
            scanner = ImageScanner()
            self.assertTrue(scanner.is_valid_image_file(img_file))
        finally:
            if img_file.exists():
                img_file.unlink()

    def test_scanner_ignored_file(self):
        tmp_file = Path("test_dummy.tmp")
        tmp_file.write_bytes(b"temp data")
        try:
            scanner = ImageScanner()
            self.assertFalse(scanner.is_valid_image_file(tmp_file))
        finally:
            if tmp_file.exists():
                tmp_file.unlink()

if __name__ == "__main__":
    unittest.main()
