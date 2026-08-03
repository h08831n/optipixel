import logging
from app.config.constants import USER_DATA_DIR

def setup_logger():
    log_file = USER_DATA_DIR / "optipixel.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("OptiPixel")
