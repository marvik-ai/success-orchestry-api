import logging
import os

from common.config import settings


def configure_logging() -> None:
    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(),
        ],
    )
