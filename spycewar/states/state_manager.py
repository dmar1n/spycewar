"""Module for managing game states."""

from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import USEREVENT

from spycewar.enums.states import GameState
from spycewar.states.game_context import GameContext
from spycewar.states.gameover import GameOver
from spycewar.states.gameplay import Gameplay
from spycewar.states.intro import Intro


class StateManager:
    """Manages the game states and transitions between them.

    Attributes:
        __states: A dictionary mapping game state names to their corresponding state objects.
        __current_state_name: The name of the current state.
        __current_state: The current state object.
    """

    def __init__(self) -> None:
        """Initializes the StateManager with predefined states."""
        self.__states = {
            GameState.INTRO: Intro(),
            GameState.GAMEPLAY: Gameplay(),
            GameState.GAMEOVER: GameOver(),
        }

        self.__current_state_name = GameState.INTRO
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.enter(GameContext())

    def process_events(self, event: Event) -> None:
        """Processes events by passing them to the current state.

        Differentiates between USEREVENT and other events, handling them appropriately.

        Args:
            event: The event to process.
        """
        if event.type == USEREVENT:
            self.__current_state.process_events(event)
        else:
            self.__current_state.handle_input(event)

    def update(self, delta_time: int) -> None:
        """Updates the current state.

        Should be called every frame to update the state logic.

        Args:
            delta_time: The time elapsed since the last frame.
        """
        if self.__current_state.done:
            self.__change_state()

        self.__current_state.update(delta_time)

    def render(self, surface_dst: Surface) -> None:
        """Renders the current state to the given surface."""
        self.__current_state.render(surface_dst)

    def release(self) -> None:
        """Releases resources associated with the current state."""
        self.__current_state.release()
        self.__current_state.exit()

    def __change_state(self) -> None:
        context = self.__current_state.exit()
        logger.info(f"Changing state from {self.__current_state_name} to {self.__current_state.next_state}")
        logger.info(f"Context: {context.data}")
        previous_state = self.__current_state_name
        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.previous_state = previous_state
        self.__current_state.enter(context)
