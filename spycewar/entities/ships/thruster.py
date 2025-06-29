"""Module for the thruster entity."""

import pygame
from pygame import USEREVENT, Surface
from pygame.event import Event
from pygame.math import Vector2
from pygame.sprite import Group

from spycewar.assets.particle import Particle
from spycewar.entities.game_object import GameObject
from spycewar.events import Events


class Thrust(GameObject):
    """Represent a particle explosion entity in the game."""

    def __init__(self, position: list[int], direction: Vector2) -> None:
        """Initialise the thrust entity."""
        super().__init__()
        self.particle_group = Group()
        self.__spawn_thrust(position, direction, 2)

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input for the explosion entity."""

    def process_events(self, event: Event) -> None:
        """Process the events for the explosion entity."""

    def update(self, delta_time: float) -> None:
        """Update the explosion entity."""
        self.particle_group.update(delta_time)
        if len(self.particle_group) <= 0:
            kill_event = Event(USEREVENT, event=Events.THRUST_EXHAUSTED, thrust=self)
            pygame.event.post(kill_event)

    def render(self, surface_dst: Surface) -> None:
        """Render the explosion entity."""
        self.particle_group.draw(surface_dst)

    def release(self) -> None:
        """Releases the resources for the explosion entity."""

    def __spawn_thrust(
        self,
        position: list[int],
        direction: Vector2,
        num_particles: int,
    ) -> None:
        """Spawns particles for the explosion.

        Args:
            position: The position where the particles will be spawned.
            direction: The direction in which the particles will move.
            num_particles: The number of particles to spawn.
        """
        for _ in range(num_particles):
            Particle(self.particle_group, position, direction, radius=1, fade=0.7)
