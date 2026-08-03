import sys
import os
from pathlib import Path

# Ensure root directory is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from app.utils.logging_utils import setup_logger, setup_excepthook, get_logger

def main():
    setup_logger(debug_mode=True)
    setup_excepthook()
    logger = get_logger()
    logger.info("Starting OptiPixel application...")

    app = QApplication(sys.argv)
    app.setApplicationName("OptiPixel")
    app.setOrganizationName("Ahaninja")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
