"""Base class for bar UI elements (health, shield, etc)."""

from pygame import Surface
from pygame.draw import rect


class BarBase:
    """Base class for bar UI elements (health, shield, etc)."""

    def __init__(  # pylint:disable=too-many-arguments, too-many-positional-arguments
        self, x: int, y: int, width: int, height: int, empty_color: tuple
    ) -> None:
        """Initialise the bar with position, size, and empty color.

        Args:
            x: The x-coordinate of the bar's top-left corner.
            y: The y-coordinate of the bar's top-left corner.
            width: The width of the bar.
            height: The height of the bar.
            empty_color: The color of the empty part of the bar.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._empty_color = empty_color

    def render_bar(self, surface_dst: Surface, ratio: float, color: tuple[int, int, int] | str) -> None:
        """Render the bar on the given surface.

        Args:
            surface_dst: The surface to render the bar on.
            ratio: The ratio of the filled part of the bar (0.0 to 1.0).
            color: The color of the filled part of the bar.
        """

        rect(
            surface_dst,
            self._empty_color,
            (self._x, self._y, self._width, self._height),
        )
        rect(
            surface_dst,
            color,
            (
                self._x + 1,
                self._y + 1,
                self._width * ratio - 2,
                self._height - 2,
            ),
        )
