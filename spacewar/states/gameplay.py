"""Module for the gameplay state in the game's state machine."""

import pygame
from loguru import logger
from pygame import Surface, Vector2
from pygame.event import Event

from spacewar.entities.players.player import Player1
from spacewar.entities.projectiles.factory import ProjectileFactory
from spacewar.entities.projectiles.types import ProjectileType
from spacewar.entities.render_group import RenderGroup
from spacewar.enums.states import GameState
from spacewar.events import Events
from spacewar.states.state import State


class Gameplay(State):
    """Represents the gameplay state in the game's state machine.

    This state handles the main gameplay logic, including player actions, game updates, and
    transitions to other states.
    """

    def __init__(self) -> None:
        """Initializes the gameplay state, setting up the initial state flags and game entities."""

        super().__init__()

        self.done = False
        self.next_state = GameState.GAME_OVER
        self.__players = RenderGroup()
        self.__player1_projectiles = RenderGroup()

    def enter(self) -> None:
        """Resets the state to indicate the game is not done when entering the gameplay state."""

        logger.info("Entering gameplay state...")
        self.done = False
        self.__players.add(Player1())

    def exit(self) -> None:
        """Placeholder for cleanup actions when exiting the gameplay state.

        Currently does nothing.
        """
        self.__players.empty()

    def handle_input(self, event: Event) -> None:
        """Handles player input events, delegating to the player's render group for processing.

        Args:
            event: The input event to handle.
        """
        if event.type == pygame.KEYDOWN:
            self.__players.handle_input(event.key, True)
        elif event.type == pygame.KEYUP:
            self.__players.handle_input(event.key, False)

    def process_events(self, event: Event) -> None:
        """Placeholder for processing other game events.

        Args:
            event: The game event to process.
        """
        self.__handle_events(event)
        self.__players.process_events(event)
        self.__player1_projectiles.process_events(event)

    def update(self, delta_time: float) -> None:
        """Updates the game logic for the gameplay state.

        Args:
            delta_time: The time elapsed since the last frame.
        """

        self.__players.update(delta_time)
        self.__player1_projectiles.update(delta_time)

    def render(self, surface_dst: Surface) -> None:
        """Renders the game entities to the given surface.

        Args:
            surface_dst: The surface to render the game entities to.
        """
        self.__players.render(surface_dst)
        self.__player1_projectiles.render(surface_dst)

    def release(self) -> None:
        """Releases resources associated with the gameplay state.

        Args:
            surface_dst: The surface to release resources from.
        """
        self.__players.release()
        self.__player1_projectiles.release()

    def __handle_events(self, event: Event) -> None:
        """Handles game events for the gameplay state.

        Args:
            event: The game event to handle.
        """

        if event.event == Events.PLAYER1_FIRES:
            self.__spawn_projectile(ProjectileType.PLAYER1, event.pos, event.vel)

    def __spawn_projectile(self, projectile_type: ProjectileType, position: Vector2, velocity: Vector2) -> None:
        """Spawns a projectile of the given type at the specified position.

        Args:
            projectile_type: The type of projectile to spawn.
            position: The position to spawn the projectile at.
            velocity: The velocity of the projectile.
        """

        logger.info("Spawning projectile...")

        projectile = ProjectileFactory.create_projectile(projectile_type, position, velocity)

        if projectile_type == ProjectileType.PLAYER1:
            self.__player1_projectiles.add(projectile)
