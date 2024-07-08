"""Module for helper methods and utilities for images."""

from importlib import resources
from importlib.abc import Traversable
from pathlib import Path

import pygame
from pygame import Surface


def load_image(file_path: Path | Traversable) -> Surface:
    """Loads the player image from the given file path and converts it to alpha.

    Args:
        file_path: The path of the image file.

    Returns:
        The image as a pygame Surface.
    """

    with resources.as_file(file_path) as file:
        return pygame.image.load(file).convert()
