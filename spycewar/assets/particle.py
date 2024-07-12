"""Module for rendering a particle in the game."""

from functools import cached_property
from random import choice, uniform

from loguru import logger
from pygame import Surface
from pygame.draw import circle
from pygame.math import Vector2
from pygame.sprite import Group, Sprite


class Particle(Sprite):
    """Particle class to represent an explosion particle in the game."""

    def __init__(self, groups: Group, position: Vector2) -> None:

        super().__init__(groups)
        self.__alpha = 255
        self.__position = position.xy
        self.__create_surface()
        logger.info(f"Position type: {type(self.__position)}")

    @property
    def color(self) -> tuple[int, int, int]:
        """Returns the color of the particle."""

        return choice([(69, 177, 200), (80, 175, 220), (60, 165, 195), (50, 155, 185)])

    @cached_property
    def speed(self) -> float:
        """Returns the speed of the particle."""

        return uniform(0.01, 0.08)

    @cached_property
    def direction(self) -> Vector2:
        """Returns the direction of the particle."""

        return Vector2(uniform(-1, 1), uniform(-1, 1)).normalize()

    @property
    def alpha(self) -> int:
        """Returns the alpha value of the particle."""

        return self.__alpha

    @property
    def fade_rate(self) -> float:
        """Returns the fade rate of the particle."""

        return 0.01

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
        circle(surface=self.image, color=self.color, center=(2, 2), radius=2)
        self.rect = self.image.get_rect(center=self.__position)

    def __move(self, delta_time: float) -> None:
        """Moves the particle based on the direction and speed."""

        self.__position += self.direction * self.speed * delta_time
        self.rect.center = self.__position

    def __fade(self, delta_time: float) -> None:
        """Fades the particle over time."""

        self.__alpha -= int(self.fade_rate * delta_time)
        self.image.set_alpha(self.alpha)

    def __check_alpha(self) -> None:
        """Checks if the particle is transparent and removes it if it is."""

        if self.alpha <= 0:
            self.kill()

    def __check_position(self) -> None:
        """Checks if the particle is off-screen and removes it if it is."""

        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()
