"""Main module for the spycewar application."""

from spycewar.logger import get_logger

logger = get_logger()


def main() -> None:
    """Initialise and starts the spycewar application, logging a startup message."""

    logger.info("Hello from spycewar!")


if __name__ == "__main__":
    main()
