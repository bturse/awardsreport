import os

LOG_FILE = os.getenv("LOG_FILE", "/app/logs/awardsreport.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": LOG_FILE,
            "mode": "a",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "file"]},
}
