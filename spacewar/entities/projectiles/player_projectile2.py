"""Module for the projectile class."""

from importlib import resources

from loguru import logger
from pygame import Surface, Vector2

from spacewar.assets.images.utils import load_image
from spacewar.config import get_cfg
from spacewar.entities.players.enums import PlayerId
from spacewar.entities.projectiles.projectile import Projectile


class PlayerProjectile2(Projectile):
    """Represents a projectile fired by the player 1's ship.

    The velocity must be given by the player's ship, who knows the direction of the projectile.

    The image is centred at the given position, so the position must be the center of the
    projectile.
    """

    __image: Surface | None = None
    __mid_width: int = 0
    __mid_height: int = 0
    __player = PlayerId.PLAYER2

    def __init__(self, position: Vector2, velocity: Vector2) -> None:

        if PlayerProjectile2.__image is None:
            PlayerProjectile2.__image = self.__load_projectile()
            PlayerProjectile2.__mid_width = PlayerProjectile2.__image.get_width() / 2
            PlayerProjectile2.__mid_height = PlayerProjectile2.__image.get_height() / 2
            logger.info(f"PlayerProjectile2 image loaded: {PlayerProjectile2.__image}")

        position = (position.x - self.__mid_width, position.y - self.__mid_height)
        super().__init__(position, velocity)

    @property
    def image(self) -> Surface | None:
        """Image of the projectile."""

        return PlayerProjectile2.__image

    def __load_projectile(self) -> Surface:
        """Loads the player image from the given file path and converts it to alpha.

        Returns:
            The player image as a pygame Surface.
        """

        file_dir, filename = get_cfg("entities", "projectiles", self.__player.value, "file")
        file_path = resources.files(file_dir).joinpath(filename)
        return load_image(file_path)
