"""Module for the projectile class."""

from pygame import Surface, Vector2

from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId
from spycewar.entities.projectiles.projectile import Projectile
from spycewar.entities.projectiles.projectile_utils import load_player_projectile_image
from spycewar.logger import get_logger

logger = get_logger()


class PlayerProjectile1(Projectile):
    """Represents a projectile fired by the player 1's ship.

    The velocity must be given by the player's ship, who knows the direction of the projectile.

    The image is centred at the given position, so the position must be the center of the
    projectile.
    """

    __image: Surface | None = None
    __mid_width: int = 0
    __mid_height: int = 0
    __player = PlayerId.PLAYER1
    __base_damage = get_cfg("entities", "projectiles", __player.value, "base_damage")

    def __init__(self, position: Vector2, velocity: Vector2) -> None:
        """Initialise the projectile."""
        if PlayerProjectile1.__image is None:
            img, mid_w, mid_h = load_player_projectile_image(self.__player)
            PlayerProjectile1.__image = img
            PlayerProjectile1.__mid_width = mid_w
            PlayerProjectile1.__mid_height = mid_h
            logger.info("PlayerProjectile1 image loaded: %s", PlayerProjectile1.__image)
        position = (position.x - self.__mid_width, position.y - self.__mid_height)
        super().__init__(position, velocity)

    @property
    def image(self) -> Surface | None:
        """Image of the projectile."""
        return PlayerProjectile1.__image

    @property
    def damage(self) -> int:
        """Damage of the projectile."""
        return self.__base_damage
