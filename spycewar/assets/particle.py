"""Module for rendering a particle in the game."""

from pygame import Surface
from pygame.draw import circle
from pygame.math import Vector2
from pygame.sprite import Group, Sprite


class Particle(Sprite):
    """Particle class to represent an explosion particle in the game."""

    def __init__(self, groups: Group, position: Vector2, color: tuple, direction: Vector2, speed: int) -> None:

        super().__init__(groups)

        self.__position = position
        self.__color = color
        self.__direction = direction
        self.__speed = speed
        self.__create_surface()

    def update(self, delta_time: int) -> None:
        """Updates the particle's position based on the direction and speed."""

        self.__move(delta_time)

    def __create_surface(self) -> None:
        """Creates a surface for the particle."""

        self.image = Surface((4, 4)).convert_alpha()
        self.image.set_colorkey("black")
        circle(surface=self.image, color=self.__color, center=(2, 2), radius=2)
        self.rect = self.image.get_rect(center=self.__position)

    def __move(self, delta_time: int) -> None:
        """Moves the particle based on the direction and speed."""

        self.__position += self.__direction * self.__speed * delta_time
        self.rect.center = self.__position
