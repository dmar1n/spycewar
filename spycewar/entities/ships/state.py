"""Module for encapsulating the different states of the ships."""

from dataclasses import dataclass, field

from pygame import Vector2


@dataclass
class ShipState:
    """Represents the state of a ship.

    Attributes:
        position: the position of the ship.
        velocity: the velocity of the ship. Stationary at the start.
        angle: the angle of the ship.
        is_accelerating: a boolean indicating whether the ship is accelerating.
        is_turning_left: a boolean indicating whether the ship is turning left.
        is_turning_right: a boolean indicating whether the ship is turning right.
    """

    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    speed: float = 0.0
    angle: float = 0.0
    is_accelerating: bool = False
    is_turning_left: bool = False
    is_turning_right: bool = False
    is_shield_enabled: bool = False
