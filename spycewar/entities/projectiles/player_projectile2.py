"""Module for the projectile class."""

from pygame import Surface, Vector2

from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId
from spycewar.entities.projectiles.projectile import Projectile
from spycewar.entities.projectiles.projectile_utils import load_player_projectile_image
from spycewar.logger import get_logger

logger = get_logger()


class PlayerProjectile2(Projectile):
    """Represents a projectile fired by the player 2's ship."""

    __image: Surface | None = None
    __mid_width: int = 0
    __mid_height: int = 0
    __player = PlayerId.PLAYER2
    __base_damage = get_cfg("entities", "projectiles", __player.value, "base_damage")

    def __init__(self, position: Vector2, velocity: Vector2) -> None:
        """Initialise the projectile."""
        if PlayerProjectile2.__image is None:
            img, mid_w, mid_h = load_player_projectile_image(self.__player)
            PlayerProjectile2.__image = img
            PlayerProjectile2.__mid_width = mid_w
            PlayerProjectile2.__mid_height = mid_h
            logger.info("PlayerProjectile2 image loaded: %s", PlayerProjectile2.__image)
        position = (position.x - self.__mid_width, position.y - self.__mid_height)
        super().__init__(position, velocity)

    @property
    def image(self) -> Surface | None:
        """Image of the projectile."""
        return PlayerProjectile2.__image

    @property
    def damage(self) -> int:
        """Damage of the projectile."""
        return self.__base_damage

    def render(self, surface_dst: Surface) -> None:
        """Render the projectile on the given surface."""
        surface_dst.blit(self.image, self._position)
