"""Module to encapsulate the health of the players."""

from dataclasses import dataclass

from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId


@dataclass
class PlayerState:
    """Represents the state of a player.

    Attributes:
        health: the health of the player.
        max_health: the maximum health of the player.
    """

    player_id: PlayerId
    __health: int
    __max_health: int

    @property
    def health(self) -> int:
        """Return the health of the player."""
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        """Set the health of the player."""

        self.__health = max(0, min(self.__max_health, value))

    def __init__(self, player_id: PlayerId):
        self.player_id = player_id
        self.__max_health = get_cfg("entities", "players", player_id.value, "max_health")
        self.__health = self.__max_health

    def is_alive(self) -> bool:
        """Return whether the player is alive."""
        return self.__health > 0

    def take_damage(self, damage: int) -> None:
        """Take damage from the player.

        Args:
            damage: the amount of damage to take.
        """
        self.health -= damage

    def heal(self, amount: int) -> None:
        """Heal the player.

        Intended for power-ups.
        """

        self.__health = min(self.__max_health, self.__health + amount)
