"""Module for the AI badge of players."""

import pygame
from pygame import Surface
from pygame.event import Event

from spycewar.assets.fonts.utils import initialise_font
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId


class AIBadge(GameObject):
    """Represents the AI badge shown for AI-controlled players."""

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        """Initialise the AI badge."""
        super().__init__()
        self.player_id = player_id
        self._x = x
        self._y = y
        self._width = 24
        self._height = 15
        self.__font = initialise_font("microgramma.ttf", 11)

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for the AI badge.

        Args:
            event: the event to process.
        """

    def update(self, delta_time: float) -> None:
        """Update the AI badge."""

    def render(self, surface_dst: Surface) -> None:
        """Render the AI badge on the screen.

        Args:
            surface_dst: the surface to render the AI badge on.
        """
        badge_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        pygame.draw.rect(surface_dst, (255, 215, 0), badge_rect)
        text_surface = self.__font.render("AI", True, (0, 0, 0))
        x, y = badge_rect.center
        text_rect = text_surface.get_rect(center=(x - 2, y))
        surface_dst.blit(text_surface, text_rect)
        self.rect = badge_rect

    def release(self) -> None:
        """Release the AI badge."""
