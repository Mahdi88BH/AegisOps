import json
import logging
import logging.config


class JSONFormatter(logging.Formatter):
    """Convert The LogRecord to a convenient Json Structure"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


LOGGING_CONFIG = {
    "version" : 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard" : {
            "format": "%(asctime)s - %(levelname)s - %(name)s => %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        "json": {
            (): JSONFormatter,
            "datefmt": "%Y-%m-%d %H:%M:%S"
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
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "production.log",
            "maxBytes": 10485760, #10 MB
            "backupCount": 5,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "": { # Root Logger
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

# Initialize Configuration
logging.config.dictConfig(LOGGING_CONFIG)