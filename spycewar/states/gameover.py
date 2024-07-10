"""Module for the gameover state."""

import pygame
from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import KEYDOWN, USEREVENT

from spycewar.assets.fonts.utils import initialise_font, render_text
from spycewar.constants import GAME_OVER
from spycewar.enums.states import GameState
from spycewar.events import Events
from spycewar.states.state import State


class GameOver(State):
    """Represents the gameover state of the game.

    This state is responsible for showing the gameover page.
    """

    def __init__(self) -> None:
        """Initializes the gameover state, setting up the text to be displayed and the next state."""
        super().__init__()

        self.__render_game_title()
        self.__render_subtext()
        self.next_state = GameState.INTRO
        self.done = False

        logger.info("Gameover state initialised.")

    def __render_subtext(self) -> None:
        """Renders the subtitle text to be displayed on the gameover screen."""

        font = initialise_font("eurostile.ttf", 18)
        self.__sub = render_text(font, "Press any key to continue...")

    def __render_game_title(self) -> None:
        """Renders the game title text to be displayed on the gameover screen."""

        font = initialise_font("microgramma.ttf", 36)
        self.__title = render_text(font, " ".join(f"{GAME_OVER}"))

    def enter(self) -> None:
        """Ensures the state is not done when entering the gameover state."""
        gameover_event = Event(USEREVENT, event=Events.GAMEOVER, color=(0, 50, 0))
        pygame.event.post(gameover_event)
        self.done = False

    def exit(self) -> None:
        """Exits the gameover state, currently doing nothing."""

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles input events to transition to the next state."""

        if event.type == KEYDOWN:
            self.done = True

    def process_events(self, event: pygame.event.Event) -> None:
        """Processes events in the gameover state, currently doing nothing."""

    def update(self, delta_time: float) -> None:
        """Updates the gameover state, currently doing nothing."""

    def render(self, surface_dst: pygame.Surface) -> None:
        """Renders the gameover text to the given surface.

        Args:
            surface_dst: the surface to render the gameover text to.
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
        """Releases resources used by the gameover state, currently doing nothing."""
