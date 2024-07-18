"""Module for powerups."""

import os
import random
from importlib import resources

import pygame
from loguru import logger
from pygame import Surface, Vector2
from pygame.event import Event
from pygame.locals import USEREVENT

from spycewar.assets.images.utils import load_image
from spycewar.config import get_cfg
from spycewar.entities.game_object import GameObject
from spycewar.events import Events


class Powerup(GameObject):
    """Represents the health bar of a player."""

    __image: Surface | None = None

    def __init__(self) -> None:
        super().__init__()
        self.__load_powerup_image()
        self._position = None
        self.__value = get_cfg("entities", "powerups", "health", "base_value") + random.randint(-10, 10)
        self.__spawned = False
        self.__duration = get_cfg("entities", "powerups", "health", "base_duration") + random.randint(0, 2000)
        self.__probability = get_cfg("entities", "powerups", "health", "probability")

    @property
    def image(self) -> Surface | None:
        """Image of the powerup."""

        return Powerup.__image

    @property
    def value(self) -> int:
        """Value of the powerup."""

        return self.__value

    def handle_input(self, key: int, is_pressed: bool) -> None:
        pass

    def process_events(self, event: Event) -> None:
        if event.event == Events.HEALTH_POWERUP_PICKUP:
            logger.info("Health power-up collected!")
            self.__spawned = False
        if event.event == Events.HEALTH_POWERUP_REMOVAL:
            logger.info("Health power-up removed!")
            self.__spawned = False

    def update(self, delta_time: float) -> None:
        """Update the powerup."""

        if not self.__spawned and random.random() < self.__probability:
            logger.info("Spawning health power-up...")
            screen_width, screen_height = os.getenv("SCREEN_WIDTH") or 800, os.getenv("SCREEN_HEIGHT") or 600
            position = Vector2(random.randint(50, int(screen_width) - 50), random.randint(50, int(screen_height) - 50))
            self._position = position
            self.__spawned = True
            powerup_removal_event = Event(USEREVENT, event=Events.HEALTH_POWERUP_REMOVAL)
            pygame.time.set_timer(powerup_removal_event, self.__duration)
            self.rect = self.image.get_rect() if self.image else None
            self.rect.topleft = self._position

    def render(self, surface_dst: Surface) -> None:
        """Render the health powerup on the screen.

        Args:
            surface_dst: the surface to render the health powerup on.
        """
        if self.__spawned:
            surface_dst.blit(Powerup.__image, self._position)

    def release(self) -> None:
        """Release the health bar."""

    def __load_powerup_image(self) -> Surface:
        """Load the powerup image.

        Returns:
            The powerup image as a pygame Surface.
        """
        if Powerup.__image is None:
            file_dir, filename = get_cfg("entities", "powerups", "health", "file")
            file_path = resources.files(file_dir).joinpath(filename)
            Powerup.__image = load_image(file_path)
            logger.info(f"Powerup image loaded: {Powerup.__image}")
