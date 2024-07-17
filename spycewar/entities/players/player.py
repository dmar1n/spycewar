"""Module for the player object in the game."""

import math
from functools import cached_property
from random import randint

import pygame
from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import USEREVENT
from pygame.math import Vector2

from spycewar.assets.fonts.utils import initialise_font, render_text
from spycewar.config import get_cfg
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.controls import PlayerControls
from spycewar.entities.players.enums import PlayerId
from spycewar.entities.players.state import PlayerState
from spycewar.entities.ships.specs import ShipSpecs
from spycewar.entities.ships.state import ShipState
from spycewar.events import Events


#
class Player(GameObject):
    """Represents the player object in the game.

    The player object is controlled by the user and can move around the screen, rotate, and shoot projectiles.

    Attributes:
        player: the player id of the player object.
        state: the state of the player object.
        specs: the specifications of the player object.
        controls: the controls of the player object.
        cooldown: the cooldown time between shots.
        hyperspace_cooldown: the cooldown time between hyperspaceation.
    """

    def __init__(self, player: PlayerId) -> None:
        super().__init__()

        self.state = PlayerState(player)
        self._position = Vector2()
        self.__ship_state = ShipState()
        self.__specs = ShipSpecs.load_ship_specs(player)
        self.__controls = PlayerControls.load_controls(player)

        # Cooldown
        self.__cooldown = 0.0
        self.__hyperspace_cooldown = 0.0

        # Caches
        self.__rotated_image = self.image  # Cache the rotated image
        self.__last_angle = self.__ship_state.angle

        logger.info(f"{player} created with specs: {self.__specs}")

        self.__get_mask()

    def __str__(self) -> str:
        return f"{self.state.player_id.name} (health: {self.state.health}, position: {self._position})."

    @cached_property
    def player_id(self) -> PlayerId:
        """The player id of the player object."""

        return self.state.player_id

    @cached_property
    def image(self) -> Surface:
        """Image of the player."""

        return self.__specs.image

    @cached_property
    def max_speed(self) -> float:
        """Maximum speed of the ship."""

        return self.__specs.max_speed

    @property
    def cooldown(self) -> float:
        """Cooldown time between shots."""

        return self.__cooldown

    @cooldown.setter
    def cooldown(self, value: float) -> None:
        """Sets the cooldown time between shots."""

        self.__cooldown = max(value, 0.0)

    @property
    def hyperspace_cooldown(self) -> float:
        """Cooldown time between hyperspaceation."""

        return self.__hyperspace_cooldown

    @hyperspace_cooldown.setter
    def hyperspace_cooldown(self, value: float) -> None:
        """Sets the cooldown time between hyperspaceation."""

        self.__hyperspace_cooldown = max(value, 0.0)

    @property
    def specs(self) -> ShipSpecs:
        """Specifications of the player."""

        return self.__specs

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handles the player input events to control the player object.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

        if key == self.__controls.thrust:
            self.__ship_state.is_accelerating = is_pressed
        if key == self.__controls.left:
            self.__ship_state.is_turning_left = is_pressed
        if key == self.__controls.right:
            self.__ship_state.is_turning_right = is_pressed
        if key == self.__controls.hyperspace and is_pressed and self.hyperspace_cooldown <= 0.0:
            self.__hyperspace()
        if key == self.__controls.fire and self.cooldown <= 0.0 and is_pressed:
            self.__fire()

    def process_events(self, event: Event) -> None:
        """Process events for other parts of the app."""

        if event.event == Events.PLAYER_HIT and event.player == self:
            self.state.take_damage(event.damage)
        if event.event == Events.HEALTH_POWERUP_PICKUP:
            self.state.heal(event.value)

    def update(self, delta_time: float) -> None:
        """Updates the player's position based on the input and the time passed since the last frame.

        Velocity is a vector quantity that describes the rate of change of position of an object. It is defined by both
        a magnitude (the speed) and a direction.

        Args:
            delta_time: the time passed since the last frame.
        """
        if not self._position:
            return

        if self.__ship_state.is_accelerating:
            self.__update_velocity()
            self.__thrust()
        if self.__ship_state.is_turning_left:
            self.__ship_state.angle += self.__specs.rotation_speed
        if self.__ship_state.is_turning_right:
            self.__ship_state.angle -= self.__specs.rotation_speed

        self._position += self.__ship_state.velocity * delta_time
        self.__ship_state.speed = self.__ship_state.velocity.length()

        if self.cooldown >= 0.0:
            self.cooldown -= delta_time

        if self.hyperspace_cooldown >= 0.0:
            self.hyperspace_cooldown -= delta_time

        self.__get_mask()

        if self.state.health <= 0:
            logger.debug(f"{self} died.")
            dead_event = Event(USEREVENT, event=Events.PLAYER_DIED, player=self)
            pygame.event.post(dead_event)

    def render(self, surface_dst: Surface) -> None:
        """Renders the player to the given surface at the player's position.

        It rotates always the original image to the current angle to avoid distortion.

        The image is rendered as a rectangle with the center at the player's position to rotate it around the center.

        Args:
            surface_dst: The surface to render the player to.
        """
        if not self._position:
            if get_cfg("entities", "players", "random_start_position"):
                self._position = Vector2(
                    randint(20, surface_dst.get_width() - 20),
                    randint(20, surface_dst.get_height()) - 20,
                )
            elif self.state.player_id == PlayerId.PLAYER1:
                self._position = Vector2(100, 100)
                self.__ship_state.angle = 180
            elif self.state.player_id == PlayerId.PLAYER2:
                self._position = Vector2(surface_dst.get_width() - 100, surface_dst.get_height() - 100)

        self.__normalise_angle()
        self.__rotate_image()
        self.__wrap_position(surface_dst)

        image_rect = self.__rotated_image.get_rect(center=self._position)
        surface_dst.blit(self.__rotated_image, image_rect)

        if get_cfg("game", "debug_mode"):
            self.__render_player_info(surface_dst)
            pygame.draw.rect(surface_dst, (255, 0, 0), self.rect, 1)

    def release(self) -> None:
        pass

    def __get_mask(self) -> None:
        """Gets the mask of the player's image."""

        self.rect = self.__rotated_image.get_rect()
        self.rect.topleft = self._position.x - self.rect.width // 2, self._position.y - self.rect.height // 2
        self.mask = pygame.mask.from_surface(self.__rotated_image)

    def __render_player_info(self, surface_dst: Surface) -> None:
        """Renders the player's information to the given surface for debugging purposes.

        Args:
            surface_dst: The surface to render the player's information to.
        """

        x = 10 if self.state.player_id == PlayerId.PLAYER1 else surface_dst.get_width() - 250

        font = initialise_font("eurostile.ttf", 14)
        surface_dst.blit(render_text(font, self.state.player_id.value), (x, 10))
        surface_dst.blit(render_text(font, f"Speed: {self.__ship_state.speed:.2f}"), (x, 30))
        surface_dst.blit(render_text(font, f"Angle: {self.__ship_state.angle:.2f}"), (x, 50))
        surface_dst.blit(render_text(font, f"Position: {self._position}"), (x, 90))
        surface_dst.blit(render_text(font, f"Velocity: {self.__ship_state.velocity}"), (x, 110))
        surface_dst.blit(render_text(font, f"Cooldown: {self.cooldown:.2f}"), (x, 70))
        surface_dst.blit(render_text(font, f"hyperspace Cooldown: {self.hyperspace_cooldown:.2f}"), (x, 170))
        surface_dst.blit(render_text(font, f"Rect: {self.rect}"), (x, 130))
        surface_dst.blit(render_text(font, f"Health: {self.state.health}"), (x, 150))

    def __wrap_position(self, surface_dst: Surface) -> None:
        """Wraps the player's position around the screen if it goes out of bounds.

        Args:
            surface_dst: The surface to wrap the player around.
        """
        if not self._position:
            return

        if self._position.x > surface_dst.get_width():
            self._position.x = 0
        elif self._position.x < 0:
            self._position.x = surface_dst.get_width()
        if self._position.y > surface_dst.get_height():
            self._position.y = 0
        elif self._position.y < 0:
            self._position.y = surface_dst.get_height()

    def __rotate_image(self) -> None:
        """Rotates the player image to the current angle if it has changed since the last frame."""
        if self.__last_angle != self.__ship_state.angle:
            self.__rotated_image = pygame.transform.rotate(self.image, self.__ship_state.angle)
            self.__last_angle = self.__ship_state.angle

    def __normalise_angle(self) -> None:
        """Normalises the angle to be between 0 and 360 degrees."""

        if self.__ship_state.angle > 360:
            self.__ship_state.angle -= 360
        elif self.__ship_state.angle < 0:
            self.__ship_state.angle += 360

    def __hyperspace(self) -> None:
        """Hyperspaces the player to a random position on the screen."""

        self.hyperspace_cooldown = self.__specs.hyperspace_cooldown
        self.__ship_state.velocity = Vector2(0, 0)
        self._position = Vector2(
            randint(20, get_cfg("game", "screen_size")[0] - 20),
            randint(20, get_cfg("game", "screen_size")[1] - 20),
        )

    def __fire(self) -> None:
        """Fires a projectile from the player's position.

        It resets the cooldown time between shots and creates a new projectile event to be
        processed by the game.
        """
        self.cooldown = self.__specs.projectile_cooldown
        projectile_velocity, fire_position = self.__compute_trajectory(speed=self.__specs.projectile_speed)
        fire_event = Event(USEREVENT, event=self.__specs.fire_event, pos=fire_position, vel=projectile_velocity)
        pygame.event.post(fire_event)

    def __thrust(self) -> None:
        """Applies full thrust to the player's velocity."""

        velocity, position = self.__compute_trajectory(backwards=True, offset=-5, speed=2.5)
        thrust_event = Event(USEREVENT, event=Events.THRUST, pos=position, dir_=2 * velocity)
        pygame.event.post(thrust_event)

    def __compute_trajectory(self, speed: float, backwards: bool = False, offset: int = 10) -> tuple[Vector2, Vector2]:
        """Computes the trajectory of the object based on the player's position and angle.

        Args:
            backwards: a boolean indicating whether the object should go backwards.
            offset: the offset from the player's position to spawn the object.
        """
        angle_radians = math.radians(self.__ship_state.angle)
        direction_vector = -Vector2(math.sin(angle_radians), math.cos(angle_radians))
        direction_vector = -direction_vector if backwards else direction_vector
        velocity = self.__ship_state.velocity + direction_vector * speed
        position = direction_vector * (self.image.get_height() // 2 + offset) + self._position
        return velocity, position

    def __update_velocity(self) -> None:
        """Updates the player's velocity based on the current angle and acceleration.

        Speed should be limited to the maximum speed, and the acceleration vector should be rotated
        to match the angle.
        """
        acceleration_vector = Vector2(self.__specs.acceleration, 0)
        acceleration_vector.rotate_ip(-self.__ship_state.angle - 90)
        velocity = self.__ship_state.velocity + acceleration_vector
        self.__ship_state.velocity = (
            velocity if velocity.length() <= self.max_speed else velocity.normalize() * self.max_speed
        )
