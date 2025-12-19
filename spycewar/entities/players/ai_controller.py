"""Module defining AI controllers for players."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol

from pygame import Vector2

from spycewar.config import get_cfg
from spycewar.entities.players.control_state import ControlState
from spycewar.entities.players.enums import PlayerId
from spycewar.entities.players.player import Player
from spycewar.logger import get_logger

logger = get_logger()


class PlayerController(Protocol):
    """Interface for player controllers."""

    def decide(self, player: Player, opponent: Player, delta_time: float) -> ControlState:
        """Return desired control state for the player."""


class PredictiveAIController:
    """AI controller that predicts opponent trajectory and adjusts strategy by aggression.

    Attributes:
        aggression: indicates how aggressively the AI behaves (0.0 = passive, 1.0 = aggressive).
        angle_tolerance: angle tolerance for turning decisions. It is higher for less aggressive AIs.
        max_lead_time: maximum time to lead shots when predicting opponent position.
    """

    def __init__(self, aggression: float) -> None:
        """Initialize the AI controller."""
        self.__aggression = self.__clamp(aggression, 0.0, 1.0)
        self.__angle_tolerance = 2.0
        self.__max_lead_time = 1500.0
        self.__max_reaction_time = 250.0

    def decide(self, player: Player, opponent: Player, delta_time: float) -> ControlState:
        """Decide on control state based on opponent's predicted position.

        Args:
            player: The AI-controlled player.
            opponent: The opponent player.
            delta_time: Time elapsed since last decision (in milliseconds).

        Returns:
            The desired ControlState for the player.
        """
        decision = self.__build_decision_context(player, opponent, delta_time)
        if decision is None:
            return ControlState()
        if self.__should_hyperspace(decision.player, decision.should_evade):
            logger.debug(
                "%s hyperspace evasion (distance %.1f, closing %.3f).",
                decision.player.player_id.name,
                decision.targeting.distance,
                decision.targeting.closing_speed,
            )
            return ControlState(hyperspace=True, shield=self.__aggression < 0.6)
        return self.__control_state(decision)

    def __build_decision_context(
        self,
        player: Player,
        opponent: Player,
        delta_time: float,
    ) -> DecisionContext | None:
        reaction_time = self.__reaction_time(delta_time)
        targeting = self.__compute_targeting(player, opponent, reaction_time)
        if targeting is None:
            return None
        profile = self.__distance_profile()
        should_evade = self.__should_evade(targeting, profile)
        lead_dir = self.__lead_direction(player, opponent, targeting)
        return DecisionContext(
            player=player,
            opponent=opponent,
            targeting=targeting,
            profile=profile,
            should_evade=should_evade,
            lead_dir=lead_dir,
        )

    def __control_state(self, decision: DecisionContext) -> ControlState:
        desired_dir = self.__desired_direction(
            decision.targeting,
            decision.profile,
            decision.lead_dir,
            decision.should_evade,
        )
        turn_left, turn_right = self.__turn_controls(decision.player.angle, desired_dir)
        engagement = EngagementContext(
            player=decision.player,
            opponent=decision.opponent,
            targeting=decision.targeting,
            profile=decision.profile,
            should_evade=decision.should_evade,
        )
        thrust = self.__should_thrust(engagement)
        fire = self.__should_fire(
            AimContext(
                current_angle=decision.player.angle,
                lead_dir=decision.lead_dir,
                distance=decision.targeting.distance,
                preferred_distance=decision.profile.preferred_distance,
                min_dim=decision.profile.min_dim,
                should_evade=decision.should_evade,
            ),
        )
        shield = (
            decision.should_evade
            and self.__aggression < 0.6
            and decision.player.state.shield > 0
        )
        return ControlState(
            thrust=thrust,
            left=turn_left,
            right=turn_right,
            fire=fire,
            hyperspace=False,
            shield=shield,
        )

    def __compute_targeting(
        self,
        player: Player,
        opponent: Player,
        reaction_time: float,
    ) -> TargetingInfo | None:
        if player.pos.length_squared() <= 0.0 or opponent.pos.length_squared() <= 0.0:
            return None
        target_pos = opponent.pos + opponent.velocity * reaction_time
        to_target = target_pos - player.pos
        distance = to_target.length()
        if distance <= 0.0:
            return None
        to_target_dir = to_target.normalize()
        relative_velocity = opponent.velocity - player.velocity
        closing_speed = relative_velocity.dot(to_target_dir)
        return TargetingInfo(
            direction=to_target_dir,
            target_pos=target_pos,
            distance=distance,
            closing_speed=closing_speed,
        )

    def __distance_profile(self) -> DistanceProfile:
        min_dim = min(get_cfg("game", "screen_size"))
        preferred_distance = self.__lerp(min_dim * 0.45, min_dim * 0.2, self.__aggression)
        distance_band = min_dim * 0.05
        evade_distance = min_dim * (0.14 + 0.08 * (1.0 - self.__aggression))
        return DistanceProfile(
            min_dim=min_dim,
            preferred_distance=preferred_distance,
            distance_band=distance_band,
            evade_distance=evade_distance,
        )

    @staticmethod
    def __should_evade(targeting: TargetingInfo, profile: DistanceProfile) -> bool:
        return targeting.distance < profile.evade_distance and targeting.closing_speed < -0.02

    @staticmethod
    def __should_hyperspace(player: Player, should_evade: bool) -> bool:
        return should_evade and player.hyperspace_cooldown <= 0.0

    def __lead_direction(
        self,
        player: Player,
        opponent: Player,
        targeting: TargetingInfo,
    ) -> Vector2:
        lead_dir = self.__predict_lead_direction(
            player.pos,
            targeting.target_pos,
            opponent.velocity,
            player.specs.projectile_speed,
        )
        return targeting.direction if lead_dir is None else lead_dir

    @staticmethod
    def __desired_direction(
        targeting: TargetingInfo,
        profile: DistanceProfile,
        lead_dir: Vector2,
        should_evade: bool,
    ) -> Vector2:
        if should_evade or targeting.distance < (profile.preferred_distance - profile.distance_band):
            return -targeting.direction
        return lead_dir

    def __turn_controls(self, current_angle: float, desired_dir: Vector2) -> tuple[bool, bool]:
        desired_angle = self.__angle_from_direction(desired_dir)
        angle_delta = self.__angle_delta(current_angle, desired_angle)
        return (
            angle_delta > self.__angle_tolerance,
            angle_delta < -self.__angle_tolerance,
        )

    def __should_thrust(
        self,
        engagement: EngagementContext,
    ) -> bool:
        distance = engagement.targeting.distance
        preferred_distance = engagement.profile.preferred_distance
        distance_band = engagement.profile.distance_band
        if engagement.should_evade or distance > (preferred_distance + distance_band):
            return True
        if distance < (preferred_distance - distance_band):
            return True
        return self.__aggression > 0.7

    def __should_fire(
        self,
        aim: AimContext,
    ) -> bool:
        aim_angle = self.__angle_from_direction(aim.lead_dir)
        aim_delta = abs(self.__angle_delta(aim.current_angle, aim_angle))
        fire_tolerance = self.__lerp(4.0, 12.0, self.__aggression)
        fire_distance = aim.preferred_distance + aim.min_dim * 0.2 * self.__aggression
        return (
            not aim.should_evade
            and aim.distance <= fire_distance
            and aim_delta <= fire_tolerance
            and (self.__aggression >= 0.35 or aim.distance >= aim.preferred_distance)
        )

    def __reaction_time(self, delta_time: float) -> float:
        return max(0.0, min(delta_time, self.__max_reaction_time))

    @staticmethod
    def __lerp(min_value: float, max_value: float, t: float) -> float:
        return min_value + (max_value - min_value) * t

    @staticmethod
    def __clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(max_value, value))

    def __predict_lead_direction(
        self,
        shooter_pos: Vector2,
        target_pos: Vector2,
        target_velocity: Vector2,
        projectile_speed: float,
    ) -> Vector2 | None:
        to_target = target_pos - shooter_pos
        a = target_velocity.dot(target_velocity) - projectile_speed**2
        b = 2.0 * to_target.dot(target_velocity)
        c = to_target.dot(to_target)

        t = self.__solve_intercept_time(a, b, c)
        if t is None:
            return None

        intercept_point = target_pos + target_velocity * t
        direction = intercept_point - shooter_pos
        return None if direction.length_squared() <= 0.0 else direction.normalize()

    def __solve_intercept_time(self, a: float, b: float, c: float) -> float | None:
        if abs(a) < 1e-6:
            if abs(b) < 1e-6:
                return None
            t = -c / b
            return t if t > 0.0 else None
        discriminant = b**2 - 4.0 * a * c
        if discriminant < 0.0:
            return None
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)
        candidates = [t for t in (t1, t2) if t > 0.0]
        if not candidates:
            return None
        t = min(candidates)
        return min(t, self.__max_lead_time)

    @staticmethod
    def __angle_from_direction(direction: Vector2) -> float:
        return math.degrees(math.atan2(-direction.x, -direction.y))

    @staticmethod
    def __angle_delta(current: float, target: float) -> float:
        return (target - current + 540.0) % 360.0 - 180.0


@dataclass(frozen=True)
class TargetingInfo:
    """Encapsulate target direction and movement information."""

    direction: Vector2
    target_pos: Vector2
    distance: float
    closing_speed: float


@dataclass(frozen=True)
class DistanceProfile:
    """Encapsulate distance preferences based on screen size and aggression."""

    min_dim: float
    preferred_distance: float
    distance_band: float
    evade_distance: float


@dataclass(frozen=True)
class EngagementContext:
    """Encapsulate engagement parameters used for movement decisions."""

    player: Player
    opponent: Player
    targeting: TargetingInfo
    profile: DistanceProfile
    should_evade: bool


@dataclass(frozen=True)
class AimContext:
    """Encapsulate aiming parameters used for firing decisions."""

    current_angle: float
    lead_dir: Vector2
    distance: float
    preferred_distance: float
    min_dim: float
    should_evade: bool


@dataclass(frozen=True)
class DecisionContext:
    """Encapsulate decision data used to build control states."""

    player: Player
    opponent: Player
    targeting: TargetingInfo
    profile: DistanceProfile
    should_evade: bool
    lead_dir: Vector2


AI_CONTROLLER_REGISTRY: dict[str, type[PredictiveAIController]] = {
    "predictive": PredictiveAIController,
}


def ai_is_enabled(player_id: PlayerId) -> bool:
    """Return True if AI is enabled for a player."""
    ai_cfg = get_cfg("entities", "players", player_id.value, "ai")
    return bool(ai_cfg.get("enabled", False))


def build_ai_controller(player_id: PlayerId) -> PlayerController:
    """Build the configured AI controller for a player."""
    ai_cfg = get_cfg("entities", "players", player_id.value, "ai")
    controller_name = ai_cfg.get("controller", "predictive")
    aggression = ai_cfg.get("aggression", 0.5)
    controller_cls = AI_CONTROLLER_REGISTRY.get(controller_name)
    if controller_cls is None:
        logger.error("Unknown AI controller '%s' for %s.", controller_name, player_id)
        controller_cls = PredictiveAIController
    return controller_cls(aggression)
