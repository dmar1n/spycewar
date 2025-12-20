"""Module for the Projectile class."""

from random import randint, random

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import USEREVENT
from pygame.math import Vector2

from spycewar.entities.game_object import GameObject
from spycewar.events import Events
from spycewar.logger import get_logger

CRITICAL_HIT_CHANCE = 0.1

logger = get_logger()


class Projectile(GameObject):
    """Represents a projectile in the game.

    The projectile object is a game object that moves in a straight line across the screen,
    following the same angle of the player's ship.

    Attributes:
        _position: the projectile's position as a pygame Vector2.
        __velocity: the projectile's velocity as a pygame Vector2.

    Methods:
        handle_input(key, is_pressed):
            Handles the input of the player.
        process_events(event):
            Process events for other parts of the app.
        update(delta_time):
            Updates the projectile's position based on its velocity and the time passed.
        render(surface_dst):
            Renders the projectile to the given surface at the projectile's position.
        release():
            Releases any resources from the projectile.
    """

    def __init__(self, position: Vector2, velocity: Vector2) -> None:
        """Initialise the projectile."""
        super().__init__()
        self._position = Vector2(position)
        self.__velocity = Vector2(velocity)
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for other parts of the app.

        Args:
            event: the event to process.
        """

    def update(self, delta_time: float) -> None:
        """Update the projectile's position based on its velocity and the time passed.

        The projectile should be kept on the screen a given time before being released. If it goes out of bounds,
        it should reappear on the other side of the screen.

        Args:
            delta_time: the time passed since the last frame.
        """
        distance = self.__velocity * delta_time
        if self._in_bounds(distance):
            self._position += distance
        else:
            kill_event = Event(
                USEREVENT,
                event=Events.PROJECTILE_OUT_OF_SCREEN,
                projectile=self,
            )
            pygame.event.post(kill_event)
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

    def calculate_damage(self, base_damage: int) -> int:
        """Calculate the damage of the projectile.

        Args:
            base_damage: the base damage of the projectile.

        Returns:
            The calculated damage of the projectile.
        """
        critical_hit = random() <= CRITICAL_HIT_CHANCE
        modifier = randint(-2, 3)
        if critical_hit:
            damage = (base_damage * 2) + modifier
            logger.info("Critical hit!!! Damage: %d", damage)
        else:
            damage = base_damage + modifier
        return damage

    def render(self, surface_dst: Surface) -> None:
        """Render the projectile to the given surface at the projectile's position."""
        surface_dst.blit(self.image, self._position)

    def release(self) -> None:
        """Release any resources from the projectile."""
