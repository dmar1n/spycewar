"""Module for helper methods and utilities for images."""

from importlib import resources
from importlib.abc import Traversable
from pathlib import Path

import pygame
from loguru import logger
from pygame import Surface


def load_music(file_path: Path | Traversable) -> Surface:
    """Loads the music from the given file path.

    Args:
        file_path: The path of the music file.
    """
    logger.info(f"Loading music from {file_path}...")
    with resources.as_file(file_path) as file:
        pygame.mixer.music.load(file)
