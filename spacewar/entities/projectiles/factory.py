"""Module for the ProjectileFactory class."""

from pygame import Vector2

from spacewar.entities.projectiles.player1_projectile import Player1Projectile
from spacewar.entities.projectiles.types import ProjectileType


class ProjectileFactory:
    """Represents a factory for creating projectiles."""

    @staticmethod
    def create_projectile(projectile_type: ProjectileType, position: Vector2, velocity: Vector2) -> Player1Projectile:
        """Creates a projectile of the given type at the given position.

        Args:
            projectile_type: the type of projectile to create.
            position: the position to create the projectile at.

        Returns:
            A new projectile of the given type at the given position.
        """
        if projectile_type == ProjectileType.PLAYER1:
            return Player1Projectile(position, velocity)

        raise ValueError(f"Invalid projectile type: {projectile_type}")
