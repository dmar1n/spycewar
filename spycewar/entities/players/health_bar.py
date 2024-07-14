"""Module for the health bar of the players."""

from loguru import logger
from pygame import Surface
from pygame.draw import rect
from pygame.event import Event

from spycewar.assets.fonts.utils import initialise_font
from spycewar.config import get_cfg
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


class HealthBar(GameObject):
    """Represents the health bar of a player."""

    __empty_color = (120, 120, 120)

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        super().__init__()
        self.player_id = player_id
        self.__x = x
        self.__y = y
        self.__width = 150
        self.__height = 15
        self.__max_hp = get_cfg("entities", "players", player_id.value, "max_health")
        self.__hp = self.__max_hp
        self.__font = initialise_font("eurostile.ttf", 12)

    @property
    def ratio(self) -> float:
        """The ratio of the current health to the maximum health."""

        return self.__hp / self.__max_hp

    def handle_input(self, key: int, is_pressed: bool) -> None:
        pass

    def process_events(self, event: Event) -> None:
        if event.event == Events.PLAYER_HIT and event.player.state.player_id == self.player_id:
            self.__take_damage(event.damage)
        if event.event == Events.HEALTH_POWERUP_PICKUP and event.player.state.player_id == self.player_id:
            self.__restore_health(event.value)

    def update(self, delta_time: float) -> None:
        """Update the health bar."""

    def render(self, surface_dst: Surface) -> None:
        """Render the health bar on the screen.

        Args:
            surface_dst: the surface to render the health bar on.
        """
        color = (220, 220, 220) if self.ratio > 0.2 else ("red")
        rect(surface_dst, self.__empty_color, (self.__x, self.__y, self.__width, self.__height))
        rect(surface_dst, color, (self.__x + 1, self.__y + 1, self.__width * self.ratio - 2, self.__height - 2))
        surface_dst.blit(self.__font.render(f"{self.player_id.name}", True, (0, 0, 0)), (self.__x + 5, self.__y + 2))

    def release(self) -> None:
        """Release the health bar."""

    def __take_damage(self, damage: int) -> None:
        """Cause the player to take damage.

        Args:
            damage: the amount of damage to take.
        """

        self.__hp -= damage
        self.__hp = max(0, self.__hp)
        logger.info(f"Player {self.player_id} took {damage} damage, health is now {self.__hp}")

    def __restore_health(self, heal: int) -> None:
        """Restore health to the player.

        Args:
            heal: the amount of health to restore.
        """

        self.__hp += heal
        self.__hp = min(self.__max_hp, self.__hp)
        logger.info(f"Player {self.player_id} healed {heal} health, health is now {self.__hp}")
