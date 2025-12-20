"""Module defining control state for player inputs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ControlState:
    """Represents the desired control state for a player."""

    thrust: bool = False
    left: bool = False
    right: bool = False
    fire: bool = False
    hyperspace: bool = False
    shield: bool = False
