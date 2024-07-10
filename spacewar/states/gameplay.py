"""Module for the gameplay state in the game's state machine."""

import pygame
from loguru import logger
from pygame import Surface, Vector2
from pygame.event import Event
from pygame.locals import KEYDOWN, KEYUP

from spacewar.entities.players.enums import PlayerId
from spacewar.entities.players.player import Player
from spacewar.entities.projectiles.factory import ProjectileFactory
from spacewar.entities.projectiles.projectile import Projectile
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
        self.__projectiles = RenderGroup()

    def enter(self) -> None:
        """Resets the state to indicate the game is not done when entering the gameplay state."""

        logger.info("Entering gameplay state...")
        self.done = False
        self.__players.add(Player(PlayerId.PLAYER1))
        self.__players.add(Player(PlayerId.PLAYER2))

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
        if event.type == KEYDOWN:
            self.__players.handle_input(event.key, True)
        elif event.type == KEYUP:
            self.__players.handle_input(event.key, False)

    def process_events(self, event: Event) -> None:
        """Placeholder for processing other game events.

        Args:
            event: The game event to process.
        """
        self.__handle_events(event)
        self.__players.process_events(event)
        self.__projectiles.process_events(event)

    def update(self, delta_time: float) -> None:
        """Updates the game logic for the gameplay state.

        Args:
            delta_time: The time elapsed since the last frame.
        """

        self.__players.update(delta_time)
        self.__projectiles.update(delta_time)

        self.__detect_collisions()

    def render(self, surface_dst: Surface) -> None:
        """Renders the game entities to the given surface.

        Args:
            surface_dst: The surface to render the game entities to.
        """

        self.__players.render(surface_dst)
        self.__projectiles.render(surface_dst)

    def release(self) -> None:
        """Releases resources associated with the gameplay state.

        Args:
            surface_dst: The surface to release resources from.
        """
        self.__players.release()
        self.__projectiles.release()

    def __handle_events(self, event: Event) -> None:
        """Handles game events for the gameplay state.

        Args:
            event: The game event to handle.
        """

        if event.event == Events.PLAYER1_FIRES:
            self.__spawn_projectile(PlayerId.PLAYER1, event.pos, event.vel)
        if event.event == Events.PLAYER2_FIRES:
            self.__spawn_projectile(PlayerId.PLAYER2, event.pos, event.vel)

        elif event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__kill_projectile(event.projectile)

    def __spawn_projectile(self, player: PlayerId, position: Vector2, velocity: Vector2) -> None:
        """Spawns a projectile of the given type at the specified position.

        Args:
            projectile_type: The type of projectile to spawn.
            position: The position to spawn the projectile at.
            velocity: The velocity of the projectile.
        """

        projectile = ProjectileFactory.create_projectile(player, position, velocity)
        self.__projectiles.add(projectile)

    def __kill_projectile(self, projectile: Projectile) -> None:
        """Removes the given projectile from the game.

        Args:
            projectile: The projectile to remove.
        """

        if projectile in self.__projectiles:
            self.__projectiles.remove(projectile)
            del projectile
        else:
            logger.error("Trying to remove a projectile that is not in the game.")

    def __detect_collisions(self) -> None:
        """Detects collisions between the players and the projectiles.

        For efficiency reasons, we only check for mask collisions if the collision is first
        detected by the rectangle.
        """
        for player in pygame.sprite.groupcollide(self.__players, self.__projectiles, False, False).keys():

            if pygame.sprite.groupcollide(self.__players, self.__projectiles, False, True, pygame.sprite.collide_mask):
                logger.info("Player hit by projectile (mask)!")
                self.__spawn_explosion(player.pos)

        for i, player1 in enumerate(self.__players):
            for player2 in self.__players.sprites()[i + 1 :]:
                if pygame.sprite.collide_mask(player1, player2):
                    logger.info("Player hit by player (mask)!")
                    self.__spawn_explosion(player1.pos)
                    self.__game_over()

    def __spawn_explosion(self, position: Vector2) -> None:
        """Spawns an explosion at the given position.

        Args:
            position: The position to spawn the explosion at.
        """
        logger.info(f"Explosion at {position}")

    def __game_over(self) -> None:
        """Transitions the game to the game over state."""

        # self.done = True
        # self.next_state = GameState.GAME_OVER
        logger.info("Game over!")
