"""Module for managing game states."""

import pygame
from loguru import logger
from pygame.locals import USEREVENT, VIDEORESIZE

from spacewar.config import get_cfg, set_cfg
from spacewar.enums.states import GameState
from spacewar.states.gameplay import Gameplay
from spacewar.states.intro import Intro


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
        }

        self.__current_state_name = GameState.INTRO
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.enter()

    def process_events(self, event: pygame.event.Event) -> None:
        """Processes events by passing them to the current state.

        Differentiates between USEREVENT and other events, handling them appropriately.

        Args:
            event: The event to process.
        """
        if event.type == USEREVENT:
            self.__current_state.process_events(event)
        else:
            self.__current_state.handle_input(event)

        if event.type == VIDEORESIZE:
            screen_size = event.size
            logger.debug(f"Resizing screen to: {screen_size}")
            set_cfg("game", "screen_size", value=screen_size)
            logger.debug(f"New screen size: {get_cfg('game', 'screen_size')}")

    def update(self, delta_time: int) -> None:
        """Updates the current state.

        Should be called every frame to update the state logic.

        Args:
            delta_time: The time elapsed since the last frame.
        """
        if self.__current_state.done:
            self.__change_state()

        self.__current_state.update(delta_time)

    def render(self, surface_dst: pygame.Surface) -> None:
        """Renders the current state to the given surface."""
        self.__current_state.render(surface_dst)

    def release(self) -> None:
        """Releases resources associated with the current state."""
        self.__current_state.release()
        self.__current_state.exit()

    def __change_state(self) -> None:
        self.__current_state.exit()

        previous_state = self.__current_state_name
        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.previous_state = previous_state

        self.__current_state.enter()
