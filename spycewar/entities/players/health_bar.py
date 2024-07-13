"""Module for the health bar of the players."""

import pygame
from loguru import logger
from pygame.event import Event

from spycewar.config import get_cfg
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


class HealthBar(GameObject):
    """Represents the health bar of a player."""

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        super().__init__()
        self.player_id = player_id
        self.__x = x
        self.__y = y
        self.__width = 150
        self.__height = 15
        self.__max_hp = get_cfg("entities", "players", player_id.value, "max_health")
        self.__hp = self.__max_hp
        self.__ratio = 1.0

    def handle_input(self, key: int, is_pressed: bool) -> None:
        pass

    def process_events(self, event: Event) -> None:
        if event.event == Events.PLAYER_HIT and event.player.state.player_id == self.player_id:
            self.__take_damage(event.damage)

    def update(self, delta_time: float) -> None:
        """Update the health bar."""

        self.__ratio = self.__hp / self.__max_hp

    def render(self, surface_dst: pygame.Surface) -> None:
        """Render the health bar on the screen.

        Args:
            surface_dst: the surface to render the health bar on.
        """

        pygame.draw.rect(surface_dst, (90, 90, 90), (self.__x, self.__y, self.__width, self.__height))
        pygame.draw.rect(surface_dst, (210, 210, 210), (self.__x, self.__y, self.__width * self.__ratio, self.__height))

    def release(self) -> None:
        """Release the health bar."""

    def __take_damage(self, damage: int) -> None:
        """Cause the player to take damage.

        Args:
            damage: the amount of damage to take.
        """

        self.__hp -= damage
        self.__hp = max(0, self.__hp)
        self.__ratio = self.__hp / self.__max_hp
        logger.info(f"Player {self.player_id} took {damage} damage, health is now {self.__hp}")
