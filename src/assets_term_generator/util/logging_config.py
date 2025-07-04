import logging
from logging.handlers import RotatingFileHandler

from assets_term_generator.core.config_manager import LOGS_DIR


def configure_logging() -> None:
    log_file = LOGS_DIR / "app.log"

    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setFormatter(log_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, stream_handler],
    )
