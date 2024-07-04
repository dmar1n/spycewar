"""This module initializes and runs the main game application using Pygame.

It sets up the game window, manages game states, and controls the game loop.
"""

import pygame

from spacewar.config import cfg
from spacewar.states.state_manager import StateManager


class App:
    """The main application class that runs the game loop and handles events, updates, and rendering.

    Attributes:
        __screen: The Pygame screen surface.
        __clock: The Pygame clock object.
        __state_manager: The state manager object.
        __running: A boolean indicating whether the game is running or not.
    """

    def __init__(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode(cfg("game", "screen_size"), pygame.RESIZABLE, 32)
        pygame.display.set_caption("Spacewar!")
        pygame.mouse.set_visible(False)

        self.__clock = pygame.time.Clock()
        self.__state_manager = StateManager()
        self.__running = False

    def run(self) -> None:
        """Runs the game loop."""

        self.__running = True

        while self.__running:
            delta_time = self.__clock.tick(60)  # 60 fps = 1000 / 60 = 16 msecs
            self.__process_events()
            self.__update(delta_time)
            self.__render()

        self.__release()

    @property
    def running(self) -> bool:
        """Indicates whether the game is running or not."""
        return self.__running

    def __process_events(self) -> None:
        """Handles all events captured from the Pygame event queue.

        This includes checking for the QUIT event or the ESCAPE key press to stop the game, and
        passing other events to the state manager for further processing.
        """

        for event in pygame.event.get():
            if (
                event.type != pygame.QUIT
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                or event.type == pygame.QUIT
            ):
                self.__running = False
            self.__state_manager.process_events(event)

    def __update(self, delta_time: int) -> None:
        """Updates the game state.

        Calls the update method of the state manager with the time passed since the last frame.

        Args:
            delta_time: The time elapsed since the last frame.
        """

        self.__state_manager.update(delta_time)

    def __render(self) -> None:
        """Renders the current game state.

        Fills the screen with black, then calls the render method of the state manager, and finally
        updates the display.
        """

        self.__screen.fill((0, 0, 0))
        self.__state_manager.render(self.__screen)
        pygame.display.update()

    def __release(self) -> None:
        """Cleans up resources.

        Calls the release method of the state manager and quits Pygame.
        """

        self.__state_manager.release()
        pygame.quit()
