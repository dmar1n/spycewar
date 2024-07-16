"""Module for the GameState enum class."""

from enum import Enum


class GameState(Enum):
    """Represents the different states of the game.

    Attributes:
        INTRO: The state when the game is in the introduction phase.
        GAMEPLAY: The state when the game is being played.
        GAME_OVER: The state when the game is over.
    """

    NONE = -1
    INTRO = 0
    GAMEPLAY = 1
    GAMEOVER = 2
