import logging.config


LOGGING_CONFIG = {
    "version" : 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard" : {
            "format": "%(asctime)s - %(levelname)s - %(name)s => %(message)s"
            },
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "level": "DEBUG",
            "formatter": "json",
            "class": "logging.FileHandler",
            "filename": "production.log",
            # "maxBytes": 10485760,
            # "backupCount": 5,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "DEBUG"
        },
        "third_party_library": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False
        }
    }
}


logging.config.dictConfig(LOGGING_CONFIG)
logger_root = logging.getLogger(__name__)
logger_base = logging.getLogger("third_party_library")