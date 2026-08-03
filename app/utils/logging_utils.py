import sys
import os
import logging
import traceback
from pathlib import Path
from typing import List
from app.config.constants import USER_DATA_DIR

LOG_FILE = USER_DATA_DIR / "optipixel.log"

class LogBufferHandler(logging.Handler):
    """Custom in-memory log handler to store recent logs for developer UI viewing."""
    def __init__(self, capacity: int = 1000):
        super().__init__()
        self.capacity = capacity
        self.records: List[str] = []

    def emit(self, record):
        try:
            msg = self.format(record)
            self.records.append(msg)
            if len(self.records) > self.capacity:
                self.records.pop(0)
        except Exception:
            self.handleError(record)

    def get_logs(self) -> str:
        return "\n".join(self.records)

    def clear(self):
        self.records.clear()

_log_buffer_handler = LogBufferHandler()

def setup_logger(debug_mode: bool = True) -> logging.Logger:
    logger = logging.getLogger("OptiPixel")
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Avoid duplicate handlers if setup_logger called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (for terminal debugging)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. File Handler (saved to USER_DATA_DIR/optipixel.log)
    try:
        USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"Failed to create file logger: {e}\n")

    # 3. In-Memory Buffer Handler (for UI Log Viewer)
    _log_buffer_handler.setLevel(logging.DEBUG)
    _log_buffer_handler.setFormatter(formatter)
    logger.addHandler(_log_buffer_handler)

    logger.info("OptiPixel Logging Subsystem initialized.")
    return logger

def get_logger() -> logging.Logger:
    logger = logging.getLogger("OptiPixel")
    if not logger.handlers:
        return setup_logger()
    return logger

def get_log_buffer() -> LogBufferHandler:
    return _log_buffer_handler

def setup_excepthook():
    """Catch unhandled exceptions and log them before app crash."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger = get_logger()
        logger.critical("Unhandled Exception caught!", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
