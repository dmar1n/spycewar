"""Module for helper methods and utilities for fonts."""

from importlib import resources

from pygame import Surface
from pygame.font import Font


def initialise_font(filename: str, size: int) -> Font:
    """Initialises a font from the given filename and size.

    Args:
        filename: the name of the font file to load (e.g. "microgramma.ttf").
        size: the size of the font to render.

    Returns:
        A Pygame Font object initialised with the given font file and size.
    """

    file_path = resources.files("spycewar.assets.fonts").joinpath(filename)
    with resources.as_file(file_path) as font_image_path:
        font = Font(str(font_image_path), size)
    return font


def render_text(font: Font, text: str) -> Surface:
    """Returns the text rendered with the given font.

    It applies anti-aliasing and uses white color.
    """
    return font.render(text, True, (200, 180, 160), None)
