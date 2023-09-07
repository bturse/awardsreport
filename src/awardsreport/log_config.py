LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {funcName} {lineno} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": "awardsreport.log",
        },
    },
    "loggers": {
        "awardsreport": {  # root logger
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    },
}
