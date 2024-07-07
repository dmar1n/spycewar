"""Module for ship specifications."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources

from pygame import Surface

from spacewar.assets.images.utils import load_image
from spacewar.config import get_cfg


@dataclass
class ShipSpecs:
    """Represents the specifications of a ship.

    Attributes:
        max_speed: the maximum speed of the ship.
        acceleration: the acceleration of the ship.
        rotation_speed: the rotation speed of the ship.
        projectile_speed: the speed of the projectile fired by the ship.
        projectile_cooldown: the cooldown between shots.
    """

    image: Surface
    max_speed: float
    acceleration: float
    rotation_speed: float
    projectile_speed: float
    projectile_cooldown: float

    @classmethod
    def load_ship_specs(cls, ship_name: str) -> ShipSpecs:
        """Loads the ship specifications from the configuration file.

        Args:
            ship_name: the name of the ship to load the specifications for.
        """
        file_dir, filename = get_cfg("entities", "ships", "player1", "file")
        file_path = resources.files(file_dir).joinpath(filename)
        image = load_image(file_path)

        max_speed = get_cfg("entities", "ships", ship_name, "max_speed")
        acceleration = get_cfg("entities", "ships", ship_name, "acceleration")
        rotation_speed = get_cfg("entities", "ships", ship_name, "rotation_speed")
        projectile_speed = get_cfg("entities", "projectiles", ship_name, "speed")
        projectile_cooldown = get_cfg("entities", "projectiles", ship_name, "cooldown")

        return cls(
            image,
            max_speed,
            acceleration,
            rotation_speed,
            projectile_speed,
            projectile_cooldown,
        )
