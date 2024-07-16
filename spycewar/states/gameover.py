"""Module for the gameover state."""

from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import KEYDOWN

from spycewar.assets.fonts.utils import initialise_font, render_text
from spycewar.constants import GAME_OVER
from spycewar.enums.states import GameState
from spycewar.states.game_context import GameContext
from spycewar.states.state import State


class GameOver(State):
    """Represents the gameover state of the game.

    This state is responsible for showing the gameover page.
    """

    def __init__(self) -> None:
        """Initializes the gameover state, setting up the text to be displayed and the next state."""
        super().__init__()

        self.next_state = GameState.INTRO
        self.done = False
        self.context: GameContext = GameContext()
        self.__title = Surface((0, 0))
        self.__result = Surface((0, 0))
        self.__subtitle = Surface((0, 0))
        logger.info("Gameover state initialised.")

    def __render_game_title(self) -> None:
        """Renders the game title text to be displayed on the gameover screen."""

        font = initialise_font("eurostile.ttf", 36)
        self.__title = render_text(font, " ".join(f"{GAME_OVER}"))

    def __render_result_text(self) -> None:
        """Renders the result text to be displayed on the gameover screen."""

        font = initialise_font("eurostile.ttf", 24)
        logger.debug(f"Current context data: {self.context.data}")
        result = f"{self.context.data.get('winner')} wins!" if self.context.data.get("winner") else "It's a draw!"
        self.__result = render_text(font, result)

    def __render_subtext(self) -> None:
        """Renders the subtitle text to be displayed on the gameover screen."""

        font = initialise_font("eurostile.ttf", 18)
        self.__subtitle = render_text(font, "Press any key to continue...")

    def enter(self, context: GameContext) -> None:
        """Ensures the state is not done when entering the gameover state."""
        self.done = False
        self.context = context
        self.__render_game_title()
        self.__render_result_text()
        self.__render_subtext()

    def exit(self) -> GameContext:
        """Exits the gameover state, currently doing nothing."""
        return self.context

    def handle_input(self, event: Event) -> None:
        """Handles input events to transition to the next state."""

        if event.type == KEYDOWN:
            self.done = True

    def process_events(self, event: Event) -> None:
        """Processes events in the gameover state, currently doing nothing."""

    def update(self, delta_time: float) -> None:
        """Updates the gameover state, currently doing nothing."""

    def render(self, surface_dst: Surface) -> None:
        """Renders the gameover text to the given surface.

        Args:
            surface_dst: the surface to render the gameover text to.
        """

        self.__display_title(surface_dst)
        self.__display_result(surface_dst)
        self.__display_subtitle(surface_dst)

    def __display_title(self, surface_dst: Surface) -> None:
        """Displays the title text on the given surface.

        Args:
            surface_dst: the surface to render the title text to.
        """

        position = surface_dst.get_width() // 2, surface_dst.get_height() // 2
        rect = self.__title.get_rect(center=position)
        surface_dst.blit(self.__title, rect.topleft)

    def __display_subtitle(self, surface_dst: Surface) -> None:
        """Displays the subtitle text on the given surface.

        Args:
            surface_dst: the surface to render the subtitle text to.
        """

        position = surface_dst.get_width() // 2, surface_dst.get_height() // 1.1
        rect = self.__subtitle.get_rect(center=position)
        surface_dst.blit(self.__subtitle, rect.topleft)

    def __display_result(self, surface_dst: Surface) -> None:
        """Displays the result text on the given surface.

        Args:
            surface_dst: the surface to render the result text to.
        """

        position = surface_dst.get_width() // 2, surface_dst.get_height() // 1.5
        rect = self.__result.get_rect(center=position)
        surface_dst.blit(self.__result, rect.topleft)

    def release(self) -> None:
        """Releases resources used by the gameover state, currently doing nothing."""
