"""Module for rendering a particle in the game."""

import os
from functools import cached_property
from random import choice, uniform

from pygame import Surface
from pygame.draw import circle
from pygame.math import Vector2
from pygame.sprite import Group, Sprite

from spycewar.config import get_cfg
from spycewar.constants import SCREEN_HEIGHT_ENV_VAR, SCREEN_WIDTH_ENV_VAR


class Particle(Sprite):
    """Particle class to represent an explosion particle in the game."""

    def __init__(self, groups: Group, position: Vector2, direction: Vector2, radius: int) -> None:

        super().__init__(groups)
        self.__alpha = 255
        self.__position = position.xy
        self.__direction = direction
        self.__radius = radius
        self.__create_surface()

    @property
    def color(self) -> tuple[int, int, int]:
        """Returns the color of the particle."""

        return choice([(69, 177, 200), (80, 175, 220), (60, 165, 195), (50, 155, 185), (90, 180, 230)])

    @cached_property
    def speed(self) -> float:
        """Returns the speed of the particle."""

        return uniform(0.02, 0.07)

    @property
    def alpha(self) -> int:
        """Returns the alpha value of the particle."""

        return self.__alpha

    @property
    def fade_rate(self) -> float:
        """Returns the fade rate of the particle."""

        return 0.1

    def update(self, delta_time: int) -> None:
        """Updates the particle's position based on the direction and speed."""

        self.__move(delta_time)
        self.__fade(delta_time)
        self.__check_alpha()
        self.__check_position()

    def __create_surface(self) -> None:
        """Creates a surface for the particle."""

        self.image = Surface((4, 4)).convert_alpha()
        self.image.set_colorkey("black")
        circle(surface=self.image, color=self.color, center=(2, 2), radius=self.__radius)
        self.rect = self.image.get_rect(center=self.__position)

    def __move(self, delta_time: float) -> None:
        """Moves the particle based on the direction and speed."""

        self.__position += self.__direction * self.speed * delta_time
        self.rect.center = self.__position

    def __fade(self, delta_time: float) -> None:
        """Fades the particle over time."""

        self.__alpha -= round(self.fade_rate * delta_time)
        self.image.set_alpha(self.alpha)

    def __check_alpha(self) -> None:
        """Checks if the particle is transparent and removes it if it is."""

        if self.alpha <= 0:
            self.kill()

    def __check_position(self) -> None:
        """Checks if the particle is off-screen and removes it if it is."""

        screen_width = os.environ.get(SCREEN_WIDTH_ENV_VAR) or get_cfg("game", "screen_size")[0]
        screen_height = os.environ.get(SCREEN_HEIGHT_ENV_VAR) or get_cfg("game", "screen_size")[1]

        if (
            self.rect.centerx < 0
            or self.rect.centerx > int(screen_width)
            or self.rect.centery < 0
            or self.rect.centery > int(screen_height)
        ):
            self.kill()
