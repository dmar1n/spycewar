"""Module for the game object class."""

from abc import ABC, abstractmethod

import pygame
from pygame import Surface, Vector2
from pygame.sprite import Sprite
from yaml import Event

from spacewar.config import get_cfg


class GameObject(Sprite, ABC):
    """An abstract class to represent a virtual game object.

    Attributes
    ----------
    _position : pygame.math.Vector2
        position of the game object in the screen
    _image : pygame.Surface
        loaded image of the game object

    Methods
    -------
    handle_input(key, is_pressed):
        Abstract, handles the input of the player
    process_events(event):
        Abstract, process events for other parts of the app
    update(delta_time):
        Abstract, updates the game object for a period of time
    release():
        Abstract, releases any resource from the game object
    _in_bounds(distance):
        Checks if game object is inside the screen
    """

    def __init__(self) -> None:
        """Abstract, Constructs the game object class."""

        super().__init__()
        self._position = pygame.math.Vector2(0.0, 0.0)
        self.rect = pygame.Rect(0, 0, 0, 0)

    @abstractmethod
    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Abstract, handles the input of the player.

        Parameters
        ----------
        key : pygame.key
            key pressed by the player
        is_pressed : boolean
            if key is pressed or released
        """

    @abstractmethod
    def process_events(self, event: Event) -> None:
        """Process events for other parts of the app.

        Args:
            event: the event to process.
        """

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Updates the game object for a period of time.

        Args:
            delta_time: _description_
        """

    @abstractmethod
    def render(self, surface_dst: Surface) -> None:
        """Renders the game object to the screen."""

    @abstractmethod
    def release(self) -> None:
        """Releases game object resources."""

    @property
    def pos(self) -> Vector2:
        """Property to get the position of the game object."""

        return self._position

    def _in_bounds(self, distance: Vector2) -> bool:
        """Checks if the game object is inside the screen.

        Args:
            distance: the distance to check if the game object is inside the screen.

        Returns:
            `True` if the game object is inside the screen, `False` otherwise.
        """
        new_pos = self._position + distance
        width, height = get_cfg("game", "screen_size")

        return new_pos.x >= 0 and new_pos.x <= width and new_pos.y >= 0 and new_pos.y <= height

    def _is_alive(self) -> bool:
        """Checks if the game object is alive.

        Returns:
            `True` if the game object is alive, `False` otherwise.
        """
        return True

    # def rect_sync(self) -> None:
    #     """Syncs the rect position with the game object position."""

    #     self.rect.x = self._position.x
    #     self.rect.y = self._position.y
    #     self.rect.height = self.image.get_height()
    #     self.rect.width = self.image.get_width()
