"""This module initializes and runs the main game application using Pygame.

It sets up the game window, manages game states, and controls the game loop.
"""

import os
from random import randint

import pygame
from loguru import logger
from pygame.event import Event
from pygame.locals import (
    DOUBLEBUF,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RESIZABLE,
    USEREVENT,
    VIDEORESIZE,
)
from pygame.time import Clock

from spycewar.config import get_cfg, set_cfg
from spycewar.constants import GAME_NAME, SCREEN_HEIGHT_ENV_VAR, SCREEN_WIDTH_ENV_VAR
from spycewar.events import Events
from spycewar.states.state_manager import StateManager

DEFAULT_COLOUR = (100, 100, 50)


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

        self.__background_colour = DEFAULT_COLOUR
        self.__screen = self.__initialise_screen()
        self.__clock = Clock()
        self.__state_manager = StateManager()
        self.__running = False
        self.__starfield = self.__generate_starfield()

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
        flags = RESIZABLE | DOUBLEBUF  # FULLSCREEN | DOUBLEBUF
        resolution = get_cfg("game", "screen_size")
        screen = pygame.display.set_mode(resolution, flags, 32)
        pygame.display.set_caption(GAME_NAME)  # Set the window title
        pygame.mouse.set_visible(False)
        os.environ[SCREEN_WIDTH_ENV_VAR] = str(resolution[0])
        os.environ[SCREEN_HEIGHT_ENV_VAR] = str(resolution[1])
        return screen

    def __process_events(self) -> None:
        """Handles all events captured from the Pygame event queue.

        This includes checking for the quitting events to stop the game, and passing other events
        to the state manager for further processing.
        """

        for event in pygame.event.get():
            self.__handle_quit_event(event)
            self.__handle_resize_event(event)
            self.__state_manager.process_events(event)
            self.__handle_background_color(event)

    def __handle_resize_event(self, event: Event) -> None:
        if event.type == VIDEORESIZE:
            screen_size = event.size
            logger.debug(f"Resizing screen to: {screen_size}")
            set_cfg("game", "screen_size", value=screen_size)
            os.environ[SCREEN_WIDTH_ENV_VAR] = str(screen_size[0])
            os.environ[SCREEN_HEIGHT_ENV_VAR] = str(screen_size[1])
            self.__starfield = self.__generate_starfield()
            self.__draw_starfield()

    def __handle_background_color(self, event: Event) -> None:
        """Handles the gameover event to stop the game.

        Args:
            event: a Pygame event to be handled.
        """
        if event.type == USEREVENT:
            if event.event == Events.INTRO:
                self.__background_colour = event.color
            if event.event == Events.GAMEOVER:
                self.__background_colour = event.color

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

        self.__screen.fill(self.__background_colour)
        self.__draw_starfield()
        self.__state_manager.render(self.__screen)
        pygame.display.update()

    def __draw_starfield(self) -> None:
        """Draws the starfield background for the game."""

        for star in self.__starfield:
            x, y, color = star
            pygame.draw.circle(self.__screen, (color, color, color), (x, y), 1)

    def __release(self) -> None:
        """Cleans up resources.

        Calls the release method of the state manager and quits Pygame.
        """

        self.__state_manager.release()
        pygame.quit()
        logger.info("Game stopped.")

    def __generate_starfield(self) -> list[tuple[int, int, int]]:
        """Generates a starfield background for the game."""

        stars = []
        num_stars = 50
        for _ in range(num_stars):
            x = randint(0, self.__screen.get_width())
            y = randint(0, self.__screen.get_height())
            stars.append((x, y, randint(50, 255)))
        return stars
