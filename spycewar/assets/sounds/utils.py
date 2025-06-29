"""Module for helper methods and utilities for images."""

from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

import pygame

from spycewar.logger import get_logger

logger = get_logger()


def load_music(file_path: Path | Traversable) -> None:
    """Load the music from the given file path.

    Args:
        file_path: The path of the music file.
    """
    logger.info("Loading music from %s...", file_path)
    with resources.as_file(file_path) as file:
        pygame.mixer.music.load(file)
