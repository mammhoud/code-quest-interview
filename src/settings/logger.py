import os
import sys
from . import DEBUG

import structlog

from . import BASE_DIR

# from src.config.base import MIDDLEWARE

# Paths
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs directory exists
logger_middleware = [
    "django_structlog.middlewares.RequestMiddleware",
    # "core.base.middlewares.tracking.LoggerRequestMiddleware",
    # "core.base.middlewares.tracking.ResponseDataRequestIDMiddleware",
]

# Logging Configurations
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored_console": {
            "()": "colorlog.ColoredFormatter",
            "format": ("%(log_color)s[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"),
            "log_colors": {
                "DEBUG": "bold_white",
                "INFO": "bold_cyan",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_purple",
            },
        },
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "key_value_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored_console",
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "key_value_formatter",
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "info.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "json_formatter",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "json_formatter",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_info"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "file_error", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "api": {
            "handlers": ["console", "file_debug"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# structlog.configure(
#     processors=[
#         structlog.contextvars.merge_contextvars,
#         structlog.stdlib.filter_by_level,
#         structlog.processors.TimeStamper(fmt="iso"),
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#         structlog.processors.UnicodeDecoder(),
#         structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
#     ],
#     context_class=dict,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     cache_logger_on_first_use=True,
# )

# Structlog Configuration
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        # structlog.stdlib.add_logger_name,
        # structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.dict_tracebacks,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        structlog.dev.set_exc_info,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


if DEBUG:
    from .debug_toolbar.setup import DebugToolbarSetup
    from .middleware import MIDDLEWARE

    MIDDLEWARE = DebugToolbarSetup.update_middleware(MIDDLEWARE)
