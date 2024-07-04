"""Module for the RenderGroup class.

It extends the Pygame sprite group class to add game-specific functionality.
"""

import pygame
from loguru import logger


class RenderGroup(pygame.sprite.Group):
    """A custom group class for managing and rendering sprites.

    This class extends pygame.sprite.Group to add game-specific functionality for handling input,
    processing events, rendering, and releasing resources.
    """

    def __init__(self) -> None:
        """Initializes the RenderGroup."""

        super().__init__()
        logger.info("RenderGroup initialized.")

    def handle_input(self, key: pygame.key, is_pressed: bool) -> None:
        """Passes input events to all sprites in the group.

        Iterates through all sprites, calling their handle_input method.

        Args:
            key: The key associated with the input event.
            is_pressed: Boolean indicating if the key is pressed.
        """
        for sprite in self.sprites():
            sprite.handle_input(key, is_pressed)

    def process_events(self, event: pygame.event) -> None:
        """Passes Pygame events to all sprites in the group.

        Iterates through all sprites, calling their process_events method.

        Args:
            event: The Pygame event to process.
        """
        for sprite in self.sprites():
            sprite.process_events(event)

    def render(self, surface_dst: pygame.Surface) -> None:
        """Renders all sprites in the group to the given surface.

        Iterates through all sprites, calling their render method.

        Args:
            surface_dst: The Pygame surface to render sprites onto.
        """
        for sprite in self.sprites():
            sprite.render(surface_dst)

    def release(self) -> None:
        """Calls the release method of all sprites in the group.

        Used for cleaning up resources.
        """
        for sprite in self.sprites():
            sprite.release()
