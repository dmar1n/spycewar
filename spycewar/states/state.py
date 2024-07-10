"""Module for the State class."""

from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event

from spycewar.enums.states import GameState


class State(ABC):
    """Represents a generic state in a state machine framework.

    This class provides the basic structure for state management including entering and exiting
    states, and handling input.
    """

    def __init__(self) -> None:
        """Initializes the state with default values.

        Sets the state as not done, with no next or previous state defined.
        """
        self.done = False
        self.next_state = GameState.NONE
        self.previous_state = GameState.NONE

    @abstractmethod
    def enter(self) -> None:
        """Abstract method to be implemented by subclasses for actions to perform when entering the state."""

    @abstractmethod
    def exit(self) -> None:
        """Abstract method to be implemented by subclasses for actions to perform when exiting the state."""

    @abstractmethod
    def handle_input(self, event: Event) -> None:
        """Abstract method to be implemented by subclasses for handling input events.

        Args:
            key: The key associated with the input event.
            is_pressed: Indicates whether the key is pressed or not.
        """

    @abstractmethod
    def process_events(self, event: Event) -> None:
        """Processes Pygame events."""

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Updates the state logic."""

    @abstractmethod
    def render(self, surface_dst: Surface) -> None:
        """Renders the state to the given surface."""

    @abstractmethod
    def release(self) -> None:
        """Releases resources associated with the state."""
