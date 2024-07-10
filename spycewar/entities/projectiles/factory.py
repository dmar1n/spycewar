"""Module for the ProjectileFactory class."""

from pygame import Vector2

from spycewar.entities.players.enums import PlayerId
from spycewar.entities.projectiles.player_projectile1 import PlayerProjectile1
from spycewar.entities.projectiles.player_projectile2 import PlayerProjectile2
from spycewar.entities.projectiles.projectile import Projectile


class ProjectileFactory:
    """Represents a factory for creating projectiles."""

    @staticmethod
    def create_projectile(player: PlayerId, position: Vector2, velocity: Vector2) -> Projectile:
        """Creates a projectile of the given type at the given position.

        Args:
            projectile_type: the type of projectile to create.
            position: the position to create the projectile at.

        Returns:
            A new projectile of the given type at the given position.
        """
        if player == PlayerId.PLAYER1:
            return PlayerProjectile1(position, velocity)
        if player == PlayerId.PLAYER2:
            return PlayerProjectile2(position, velocity)
        raise ValueError(f"Invalid player id: {player}")
