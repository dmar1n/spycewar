"""A simple logger module using the standard Python logging package."""

import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logger = logging.getLogger("spycewar")
logger.setLevel(logging.INFO)


def get_logger() -> logging.Logger:
    """Return the logger instance for the spycewar application."""
    return logger
