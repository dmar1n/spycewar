"""Module for event types in the game."""

from enum import Enum, auto


class Events(Enum):
    """Represents the different types of events in the game.

    Attributes:
    `PLAYER1_FIRES`: Player 1 fires a projectile. Params: pos (position) and vel (velocity).
    `PROJECTILE_OUT_OF_SCREEN`: A projectile went out of the screen. Params: projectile (projectile).
    """

    PLAYER1_FIRES = 1
    PLAYER2_FIRES = 2
    PROJECTILE_OUT_OF_SCREEN = auto()
