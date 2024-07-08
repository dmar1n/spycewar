"""Module for the Projectile class."""

from pygame import Surface
from pygame.event import Event
from pygame.math import Vector2

from spacewar.entities.gameobject import GameObject


class Projectile(GameObject):
    """Represents a projectile in the game.

    The projectile object is a game object that moves in a straight line across the screen,
    following the same angle of the player's ship.

    Attributes:
        _position: the projectile's position as a pygame Vector2.
        __velocity: the projectile's velocity as a pygame Vector2.
    """

    def __init__(self, position: Vector2, velocity: Vector2) -> None:
        super().__init__()
        self.__position = Vector2(position)
        self.__velocity = Vector2(velocity)
        # self.rect_sync()

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handles the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for other parts of the app.

        Args:
            event: the event to process.
        """

    def update(self, delta_time: float) -> None:
        """Updates the projectile's position based on its velocity and the time passed.

        The projectile should be kept on the screen a given time before being released. If it goes out of bounds,
        it should reappear on the other side of the screen.

        Args:
            delta_time: the time passed since the last frame.
        """

        distance = self.__velocity * delta_time
        self.__position += distance
        # self.rect_sync()

    def render(self, surface_dst: Surface) -> None:
        """Renders the projectile to the given surface at the projectile's position."""

        surface_dst.blit(self.image, self.__position)

    def release(self) -> None:
        """Releases any resources from the projectile."""
