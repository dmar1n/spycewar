"""Module for event types in the game."""

from enum import Enum, auto


class Events(Enum):
    """Represents the different types of events in the game.

    Attributes:
    `PLAYER1_FIRES`: Player 1 fires a projectile. Params: `pos` (position) and `vel` (velocity).
    `PLAYER2_FIRES`: Player 2 fires a projectile. Params: `pos` (position) and `vel` (velocity).
    `THRUST`: A player is thrusting. Params: `pos` (position) and `dir_` (velocity).
    `THRUST_EXHAUSTED`: A player stopped thrusting. Params: thrust.
    `PROJECTILE_OUT_OF_SCREEN`: A projectile went out of the screen. Params: projectile (projectile).
    `EXPLOSION_OVER`: An explosion is over. Params: explosion.
    `GAMEOVER`: The game is over. Params: RGB.
    `INTRO`: The game is in the intro screen. Params: RGB
    """

    PLAYER1_FIRES = 1
    PLAYER2_FIRES = 2
    THRUST = auto()
    THRUST_EXHAUSTED = auto()
    PROJECTILE_OUT_OF_SCREEN = auto()
    EXPLOSION_OVER = auto()
    GAMEOVER = auto()
    INTRO = auto()
