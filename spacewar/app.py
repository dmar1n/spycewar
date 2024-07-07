"""This module initializes and runs the main game application using Pygame.

It sets up the game window, manages game states, and controls the game loop.
"""

import pygame
from loguru import logger
from pygame.event import Event
from pygame.locals import DOUBLEBUF, K_ESCAPE, KEYDOWN, QUIT
from pygame.time import Clock

from spacewar.config import get_cfg
from spacewar.constants import GAME_NAME
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
        logger.info("Initializing game...")
        pygame.init()
        # pygame.event.set_blocked(None)
        # pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])

        self.__screen = self.__initialise_screen()
        self.__clock = Clock()
        self.__state_manager = StateManager()
        self.__running = False

    def run(self) -> None:
        """Runs the game loop."""

        self.__running = True
        logger.info("Starting game loop...")

        while self.is_running:
            delta_time = self.__clock.tick(60)  # 60 fps = 1000 / 60 = 16 msecs
            self.__process_events()
            self.__update(delta_time)
            self.__render()

        self.__release()

    @property
    def is_running(self) -> bool:
        """Indicates whether the game is running or not."""
        return self.__running

    def __initialise_screen(self) -> pygame.Surface:
        """Initialises the game window with the screen size, resizable, and 32-bit color (with transparency)."""

        logger.info("Setting up game window...")
        flags = DOUBLEBUF  # FULLSCREEN | DOUBLEBUF
        resolution = get_cfg("game", "screen_size")
        screen = pygame.display.set_mode(resolution, flags, 32)
        pygame.display.set_caption(GAME_NAME)  # Set the window title
        pygame.mouse.set_visible(False)
        return screen

    def __process_events(self) -> None:
        """Handles all events captured from the Pygame event queue.

        This includes checking for the quitting events to stop the game, and passing other events
        to the state manager for further processing.
        """

        for event in pygame.event.get():
            self.__handle_quit_event(event)
            self.__state_manager.process_events(event)

    def __handle_quit_event(self, event: Event) -> None:
        """Handles events to stop the game.

        Args:
            event: a Pygame event to be handled.
        """
        if event.type != QUIT and event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
            self.__running = False

    def __update(self, delta_time: int) -> None:
        """Updates the game objects.

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
        logger.info("Game stopped.")
