"""Module for the introduction state of the game."""

import pygame
from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import KEYDOWN, USEREVENT

from spycewar.assets.fonts.utils import initialise_font, render_text
from spycewar.constants import GAME_NAME
from spycewar.enums.states import GameState
from spycewar.events import Events
from spycewar.states.game_context import GameContext
from spycewar.states.state import State


class Intro(State):
    """Represents the introduction state of the game.

    This state is responsible for displaying the introductory text and transitioning to the
    gameplay state.
    """

    def __init__(self) -> None:
        """Initializes the introduction state, setting up the text to be displayed and the next state."""
        super().__init__()

        self.__render_game_title()
        self.__render_subtext()
        self.next_state = GameState.GAMEPLAY
        self.done = False
        self.context = GameContext()

        logger.info("Introduction state initialized.")

    def __render_subtext(self) -> None:
        """Renders the subtitle text to be displayed on the introduction screen."""

        font = initialise_font("eurostile.ttf", 18)
        self.__sub = render_text(font, "Press any key to continue...")

    def __render_game_title(self) -> None:
        """Renders the game title text to be displayed on the introduction screen."""

        font = initialise_font("microgramma.ttf", 48)
        self.__title = render_text(font, " ".join(f"{GAME_NAME}"))

    def enter(self, context: GameContext) -> None:
        """Ensures the state is not done when entering the introduction state."""
        logger.info("Entering introduction state...")
        intro_event = Event(USEREVENT, event=Events.INTRO, color=(0, 0, 0))
        pygame.event.post(intro_event)
        self.done = False

    def exit(self) -> GameContext:
        """Exits the introduction state, currently doing nothing."""
        return self.context

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles input events to transition to the next state."""

        if event.type == KEYDOWN:
            self.done = True

    def process_events(self, event: pygame.event.Event) -> None:
        """Processes events in the introduction state, currently doing nothing."""

    def update(self, delta_time: float) -> None:
        """Updates the introduction state, currently doing nothing."""

    def render(self, surface_dst: pygame.Surface) -> None:
        """Renders the introduction text to the given surface.

        Args:
            surface_dst: the surface to render the introduction text to.
        """

        self.__display_title(surface_dst)
        self.__display_subtitle(surface_dst)

    def __display_subtitle(self, surface_dst: Surface) -> None:
        """Displays the subtitle text on the given surface.

        Args:
            surface_dst: the surface to render the subtitle text to.
        """

        position = surface_dst.get_width() // 2, surface_dst.get_height() // 1.6
        rect = self.__sub.get_rect(center=position)
        surface_dst.blit(self.__sub, rect.topleft)

    def __display_title(self, surface_dst: Surface) -> None:
        """Displays the title text on the given surface.

        Args:
            surface_dst: the surface to render the title text to.
        """

        position = surface_dst.get_width() // 2, surface_dst.get_height() // 2
        rect = self.__title.get_rect(center=position)
        surface_dst.blit(self.__title, rect.topleft)

    def release(self) -> None:
        """Releases resources used by the introduction state, currently doing nothing."""
