"""Module to encapsulate the different controls of the players."""

from __future__ import annotations

from dataclasses import dataclass

from pygame.event import Event
from pygame.locals import K_a, K_d, K_i, K_j, K_k, K_l, K_q, K_s, K_u, K_w

from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId

KEY_MAPPING = {
    "a": K_a,
    "d": K_d,
    "i": K_i,
    "j": K_j,
    "k": K_k,
    "l": K_l,
    "s": K_s,
    "w": K_w,
    "q": K_q,
    "u": K_u,
}


@dataclass
class PlayerControls:
    """Represents the controls of a player.

    Attributes:
        up: fire.
        left: rotate left.
        right: rotate right.
        down: thrust.
    """

    fire: Event
    left: Event
    right: Event
    thrust: Event
    stop: Event

    @classmethod
    def load_controls(cls, player: PlayerId) -> PlayerControls:
        """Loads the controls from the configuration file.

        Args:
            player: the player id to load the controls for.
        """

        controls = get_cfg("entities", "players", player.value, "controls")
        return cls(
            KEY_MAPPING[controls["fire"]],
            KEY_MAPPING[controls["left"]],
            KEY_MAPPING[controls["right"]],
            KEY_MAPPING[controls["thrust"]],
            KEY_MAPPING[controls["stop"]],
        )
