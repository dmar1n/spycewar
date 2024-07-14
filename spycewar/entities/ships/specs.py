"""Module for ship specifications."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources

from pygame import Surface

from spycewar.assets.images.utils import load_image
from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


@dataclass
class ShipSpecs:
    """Represents the specifications of a ship.

    Attributes:
        player: the player id of the ship.
        image: the image of the ship.
        max_speed: the maximum speed of the ship.
        acceleration: the acceleration of the ship.
        rotation_speed: the rotation speed of the ship.
        projectile_speed: the speed of the projectile fired by the ship.
        projectile_cooldown: the cooldown between shots.
        hyperspace_cooldown: the cooldown between teleports.
    """

    player: PlayerId
    fire_event: Events
    image: Surface
    max_speed: float
    acceleration: float
    rotation_speed: float
    projectile_speed: float
    projectile_cooldown: float
    hyperspace_cooldown: float

    @classmethod
    def load_ship_specs(cls, player: PlayerId) -> ShipSpecs:
        """Loads the ship specifications from the configuration file.

        Args:
            ship_name: the name of the ship to load the specifications for.
        """
        file_dir, filename = get_cfg("entities", "ships", player.value, "file")
        file_path = resources.files(file_dir).joinpath(filename)
        image = load_image(file_path)

        fire_event = Events(get_cfg("entities", "players", player.value, "fire_event"))
        max_speed = get_cfg("entities", "ships", player.value, "max_speed")
        acceleration = get_cfg("entities", "ships", player.value, "acceleration")
        rotation_speed = get_cfg("entities", "ships", player.value, "rotation_speed")
        projectile_speed = get_cfg("entities", "projectiles", player.value, "speed")
        projectile_cooldown = get_cfg("entities", "projectiles", player.value, "cooldown")
        hyperspace_cooldown = get_cfg("entities", "ships", player.value, "hyperspace_cooldown")

        return cls(
            player,
            fire_event,
            image,
            max_speed,
            acceleration,
            rotation_speed,
            projectile_speed,
            projectile_cooldown,
            hyperspace_cooldown,
        )
