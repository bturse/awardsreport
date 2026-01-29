import logging.config
from awardsreport.log_config import LOGGING_CONFIG


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
