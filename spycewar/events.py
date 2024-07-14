"""Module for event types in the game."""

from enum import Enum, auto


class Events(Enum):
    """Represents the different types of events in the game.

    Attributes:
    `PLAYER1_FIRES`: Player 1 fires a projectile. Params: `pos` (position) and `vel` (velocity).
    `PLAYER2_FIRES`: Player 2 fires a projectile. Params: `pos` (position) and `vel` (velocity).
    `PLAYER_HIT`: A player is hit. Params: player (`Player`) and damage (int).
    `PLAYER_DIED`: A player died. Params: player (Player).
    `THRUST`: A player is thrusting. Params: `pos` (position) and `dir_` (velocity).
    `THRUST_EXHAUSTED`: A player stopped thrusting. Params: thrust.
    `PROJECTILE_OUT_OF_SCREEN`: A projectile went out of the screen. Params: projectile (`Projectile`).
    `EXPLOSION_OVER`: An explosion is over. Params: explosion.
    `HEALTH_POWERUP_PICKUP`: A health power-up is spawned. Params: power-up (`PowerUp`) and player (`Player`).
    `HEALTH_POWERUP_REMOVAL`: A health power-up is removed. Params: power-up.
    `GAMEOVER`: The game is over. Params: RGB.
    `INTRO`: The game is in the intro screen. Params: RGB
    """

    PLAYER1_FIRES = auto()
    PLAYER2_FIRES = auto()
    PLAYER_HIT = auto()
    PLAYER_DIED = auto()
    THRUST = auto()
    THRUST_EXHAUSTED = auto()
    PROJECTILE_OUT_OF_SCREEN = auto()
    EXPLOSION_OVER = auto()
    HEALTH_POWERUP_PICKUP = auto()
    HEALTH_POWERUP_REMOVAL = auto()
    GAMEOVER = auto()
    INTRO = auto()
