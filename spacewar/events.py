"""Module for event types in the game."""

from enum import Enum


class Events(Enum):
    """Represents the different types of events in the game."""

    PLAYER1_FIRES = (0,)  # pos = position of projectile to spawn
