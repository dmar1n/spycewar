"""Module for the introduction state of the game."""

from importlib import resources

import pygame
from loguru import logger

from spacewar.config import cfg
from spacewar.enums.states import GameState
from spacewar.states.state import State


class Intro(State):
    """Represents the introduction state of the game.

    This state is responsible for displaying the introductory text and transitioning to the
    gameplay state.
    """

    def __init__(self) -> None:
        """Initializes the introduction state, setting up the text to be displayed and the next state."""
        super().__init__()

        file_path = resources.files("spacewar.assets.fonts").joinpath("microgramma.ttf")
        with resources.as_file(file_path) as font_image_path:
            font = pygame.font.Font(str(font_image_path), 18)

        text = cfg("states", "intro", "text")
        logger.info(f"Intro text: {text}")

        self.__text = font.render(text, True, (255, 255, 255), None)
        self.next_state = GameState.GAMEPLAY
        self.done = False

    def enter(self) -> None:
        """Ensures the state is not done when entering the introduction state."""
        self.done = False

    def exit(self) -> None:
        """Exits the introduction state, currently doing nothing."""

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles input events to transition to the next state."""
        if event.type == pygame.KEYDOWN:
            self.done = True

    def process_events(self, event: pygame.event.Event) -> None:
        """Processes events in the introduction state, currently doing nothing."""

    def update(self, delta_time: float) -> None:
        """Updates the introduction state, currently doing nothing."""

    def render(self, surface_dst: pygame.Surface) -> None:
        """Renders the introduction text to the given surface."""
        surface_dst.blit(self.__text, cfg("states", "intro", "position"))

    def release(self) -> None:
        """Releases resources used by the introduction state, currently doing nothing."""
