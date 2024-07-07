"""Module for the projectile class."""

from importlib import resources

from pygame import Surface, Vector2

from spacewar.assets.images.utils import load_image
from spacewar.config import get_cfg
from spacewar.entities.projectiles.projectile import Projectile


class Player1Projectile(Projectile):
    """Represents a projectile fired by the player 1's ship.

    The velocity must be given by the player's ship, who knows the direction of the projectile.
    """

    __image: Surface | None = None

    def __init__(self, position: Vector2, velocity: Vector2) -> None:

        if Player1Projectile.__image is None:
            Player1Projectile.__image = self.__load_projectile()

        super().__init__(position, velocity)

    @property
    def image(self) -> Surface | None:
        """Image of the projectile."""

        return Player1Projectile.__image

    def __load_projectile(self) -> Surface:
        """Loads the player image from the given file path and converts it to alpha.

        Returns:
            The player image as a pygame Surface.
        """

        file_dir, filename = get_cfg("entities", "projectiles", "player1", "file")
        file_path = resources.files(file_dir).joinpath(filename)
        return load_image(file_path)
