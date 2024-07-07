"""Module for the player object in the game."""

import math
from functools import cached_property

import pygame
from loguru import logger
from pygame import Surface
from pygame.event import Event
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP, USEREVENT, K_a, K_d, K_s, K_w
from pygame.math import Vector2

from spacewar.assets.fonts.utils import initialise_font, render_text
from spacewar.config import get_cfg
from spacewar.entities.gameobject import GameObject
from spacewar.entities.ships.specs import ShipSpecs
from spacewar.entities.ships.state import ShipState
from spacewar.events import Events


#
class Player1(GameObject):
    """Represents the player object in the game.

    The player object is controlled by the user and can move around the screen, rotate, and shoot projectiles.

    Attributes:
        __position: The player's position as a pygame Vector2.
        __is_accelerating: A boolean indicating whether the player is accelerating or not.
        __is_turning_left: A boolean indicating whether the player is turning left or not.
        __is_turning_right: A boolean indicating whether the player is turning right or not.
        __velocity: The player's velocity as a pygame Vector2.
        __max_speed: The maximum speed of the player.
        __current_speed: The current speed of the player.
        __turning_speed: The speed at which the player can turn.
        __acceleration: The acceleration of the player.
        __cool_down: The cool down time between shots.
        __angle: The angle of the player.
        __image: The player's image.
        __rotated_image: The rotated player image.
        __last_angle: The last angle of the player.
    """

    def __init__(self) -> None:
        super().__init__()

        self.__state = ShipState()
        self.__specs = ShipSpecs.load_ship_specs("player1")

        # Projectiles
        self.__cooldown = 0.0

        # Caches
        self.__rotated_image = self.image  # Cache the rotated image
        self.__last_angle = self.__state.angle

        self.rect_sync()

    @cached_property
    def image(self) -> Surface:
        """Image of the player."""

        return self.__specs.image

    @cached_property
    def max_speed(self) -> float:
        """Maximum speed of the ship."""

        return self.__specs.max_speed

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handles the player input events to control the player object.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

        if key in [K_DOWN, K_s]:
            self.__state.is_accelerating = is_pressed
        if key in [K_LEFT, K_a]:
            self.__state.is_turning_left = is_pressed
        if key in [K_RIGHT, K_d]:
            self.__state.is_turning_right = is_pressed
        if key in [K_UP, K_w]:  # and self.__cool_down <= 0.0:
            self.__fire()

    def process_events(self, event: Event) -> None:
        """Process events for other parts of the app."""

    def update(self, delta_time: float) -> None:
        """Updates the player's position based on the input and the time passed since the last frame.

        Velocity is a vector quantity that describes the rate of change of position of an object. It is defined by both
        a magnitude (the speed) and a direction.

        Args:
            delta_time: the time passed since the last frame.
        """
        if not self.__state.position:
            return

        if self.__state.is_accelerating:
            self.__update_velocity()
        if self.__state.is_turning_left:
            self.__state.angle += self.__specs.rotation_speed
        if self.__state.is_turning_right:
            self.__state.angle -= self.__specs.rotation_speed

        self.__state.position += self.__state.velocity * delta_time
        self.__state.speed = self.__state.velocity.length()

        if self.__cooldown >= 0.0:
            self.__cooldown -= delta_time

        self.rect_sync()

    def render(self, surface_dst: Surface) -> None:
        """Renders the player to the given surface at the player's position.

        It rotates always the original image to the current angle to avoid distortion.

        The image is rendered as a rectangle with the center at the player's position to rotate it around the center.

        Args:
            surface_dst: The surface to render the player to.
        """
        if not self.__state.position:
            self.__state.position = Vector2(surface_dst.get_width() // 3, surface_dst.get_height() // 2)

        self.__render_player_info(surface_dst)  # For debugging purposes
        self.__normalise_angle()
        self.__rotate_image()
        self.__wrap_position(surface_dst)

        image_rect = self.__rotated_image.get_rect(center=self.__state.position)
        surface_dst.blit(self.__rotated_image, image_rect)

    def release(self) -> None:
        pass

    def __render_player_info(self, surface_dst: Surface) -> None:
        """Renders the player's information to the given surface for debugging purposes.

        Args:
            surface_dst: The surface to render the player's information to.
        """

        font = initialise_font("eurostile.ttf", 14)
        surface_dst.blit(render_text(font, "Player 1"), (10, 10))
        surface_dst.blit(render_text(font, f"Speed: {self.__state.speed:.2f}"), (10, 30))
        surface_dst.blit(render_text(font, f"Angle: {self.__state.angle:.2f}"), (10, 50))
        surface_dst.blit(render_text(font, f"Position: {self.__state.position}"), (10, 90))
        surface_dst.blit(render_text(font, f"Velocity: {self.__state.velocity}"), (10, 110))
        surface_dst.blit(render_text(font, f"Cool down: {self.__cooldown:.2f}"), (10, 70))

    def __wrap_position(self, surface_dst: Surface) -> None:
        """Wraps the player's position around the screen if it goes out of bounds.

        Args:
            surface_dst: The surface to wrap the player around.
        """
        if not self.__state.position:
            return

        if self.__state.position.x > surface_dst.get_width():
            self.__state.position.x = 0
        elif self.__state.position.x < 0:
            self.__state.position.x = surface_dst.get_width()
        if self.__state.position.y > surface_dst.get_height():
            self.__state.position.y = 0
        elif self.__state.position.y < 0:
            self.__state.position.y = surface_dst.get_height()

    def __rotate_image(self) -> None:
        """Rotates the player image to the current angle if it has changed since the last frame."""
        if self.__last_angle != self.__state.angle:
            self.__rotated_image = pygame.transform.rotate(self.image, self.__state.angle)
            self.__last_angle = self.__state.angle

    def __normalise_angle(self) -> None:
        """Normalises the angle to be between 0 and 360 degrees."""

        if self.__state.angle > 360:
            self.__state.angle -= 360
        elif self.__state.angle < 0:
            self.__state.angle += 360

    def __fire(self) -> None:
        """Fires a projectile from the player's position."""

        logger.info("Player 1 fires...")
        speed = get_cfg("entities", "projectiles", "player1", "speed")

        angle_radians = math.radians(self.__state.angle)
        direction_vector = -Vector2(math.sin(angle_radians), math.cos(angle_radians))
        projectile_velocity = self.__state.velocity + direction_vector * speed

        fire_event = Event(USEREVENT, event=Events.PLAYER1_FIRES, pos=self.__state.position, vel=projectile_velocity)
        pygame.event.post(fire_event)
        logger.info(f"Player 1 fired at {self.__state.position} with velocity {self.__state.velocity * speed}")

    def __update_velocity(self) -> None:
        """Updates the player's velocity based on the current angle and acceleration.

        Speed should be limited to the maximum speed, and the acceleration vector should be rotated
        to match the angle.
        """
        acceleration_vector = Vector2(self.__specs.acceleration, 0)
        acceleration_vector.rotate_ip(-self.__state.angle - 90)
        velocity = self.__state.velocity + acceleration_vector
        self.__state.velocity = (
            velocity if velocity.length() <= self.max_speed else velocity.normalize() * self.max_speed
        )
