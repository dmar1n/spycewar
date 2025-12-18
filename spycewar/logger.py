"""A simple logger module using the standard Python logging package."""

import atexit
import json
import logging
from logging.config import dictConfig
from pathlib import Path

APP_NAME = "spycewar"
STD_LOG_FIELD = [
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
]


def get_logger() -> logging.Logger:
    """Return the logger instance for the spycewar application."""
    return logging.getLogger(APP_NAME)


def setup_logging() -> None:
    """Set up logging configuration from a JSON file."""
    config_path = Path("config") / "logging.json"
    logger = get_logger()
    if not config_path.exists():
        logger.warning("Logging configuration file not found at %s", config_path)
    with config_path.open(encoding="utf-8") as file:
        cfg = json.load(file)
    dictConfig(cfg)
    logger.debug("Logging is set up using configuration from %s", config_path)

    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore[attr-defined]
        atexit.register(queue_handler.listener.stop)  # type: ignore[attr-defined]
