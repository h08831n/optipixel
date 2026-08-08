import os
from pathlib import Path

APP_NAME = "OptiPixel"
APP_TAGLINE = "Web Image Optimizer & Converter"
APP_PUBLISHER = "Ahaninja"
APP_WEBSITE = "https://ahaninja.com"
APP_VERSION = "1.0.0"

SUPPORTED_INPUT_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic", ".heif",
    ".tif", ".tiff", ".bmp", ".gif", ".jxl", ".svg"
}

SUPPORTED_OUTPUT_FORMATS = ["WEBP", "AVIF", "JPEG", "PNG", "TIFF", "BMP", "ORIGINAL"]

DEFAULT_QUALITY = 82
DEFAULT_SIZE_THRESHOLD_KB = 400

# Output Modes
OUTPUT_MODE_REPLACE = "replace"
OUTPUT_MODE_FOLDER = "folder"
OUTPUT_MODE_NEXT_TO_ORIGINAL = "next_to_original"

# User Data Dir
USER_DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / APP_PUBLISHER / APP_NAME
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
SETTINGS_FILE = USER_DATA_DIR / "settings.json"
HISTORY_FILE = USER_DATA_DIR / "history.json"
BACKUP_DIR = USER_DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
