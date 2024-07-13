"""Module for the gameplay state in the game's state machine."""

import os
import random

import pygame
from loguru import logger
from pygame import Surface, Vector2
from pygame.event import Event
from pygame.locals import KEYDOWN, KEYUP, USEREVENT

from spycewar.constants import SCREEN_WIDTH_ENV_VAR
from spycewar.entities.explosion import Explosion
from spycewar.entities.players.enums import PlayerId
from spycewar.entities.players.health_bar import HealthBar
from spycewar.entities.players.player import Player
from spycewar.entities.projectiles.factory import ProjectileFactory
from spycewar.entities.projectiles.projectile import Projectile
from spycewar.entities.render_group import RenderGroup
from spycewar.entities.ships.thruster import Thrust
from spycewar.enums.states import GameState
from spycewar.events import Events
from spycewar.states.state import State


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
        self.__explosions = RenderGroup()
        self.__thrusts = RenderGroup()
        self.__heath_bars = RenderGroup()

    def enter(self) -> None:
        """Resets the state to indicate the game is not done when entering the gameplay state."""

        logger.info("Entering gameplay state...")
        self.done = False
        self.__players.add(Player(PlayerId.PLAYER1))
        self.__players.add(Player(PlayerId.PLAYER2))
        self.__heath_bars.add(HealthBar(PlayerId.PLAYER1, 10, 10))
        self.__heath_bars.add(HealthBar(PlayerId.PLAYER2, int(os.environ[SCREEN_WIDTH_ENV_VAR]) - 160, 10))

    def exit(self) -> None:
        """Placeholder for cleanup actions when exiting the gameplay state.

        Currently does nothing.
        """
        self.__players.empty()
        self.__projectiles.empty()
        self.__explosions.empty()
        self.__thrusts.empty()
        self.__heath_bars.empty()

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
        self.__explosions.process_events(event)
        self.__thrusts.process_events(event)
        self.__heath_bars.process_events(event)

    def update(self, delta_time: float) -> None:
        """Updates the game logic for the gameplay state.

        Args:
            delta_time: The time elapsed since the last frame.
        """

        self.__players.update(delta_time)
        self.__projectiles.update(delta_time)
        self.__explosions.update(delta_time)
        self.__thrusts.update(delta_time)
        self.__heath_bars.update(delta_time)
        self.__detect_collisions()

    def render(self, surface_dst: Surface) -> None:
        """Renders the game entities to the given surface.

        Args:
            surface_dst: The surface to render the game entities to.
        """

        self.__players.render(surface_dst)
        self.__projectiles.render(surface_dst)
        self.__explosions.render(surface_dst)
        self.__thrusts.render(surface_dst)
        self.__heath_bars.render(surface_dst)

    def release(self) -> None:
        """Releases resources associated with the gameplay state.

        Args:
            surface_dst: The surface to release resources from.
        """
        self.__players.release()
        self.__projectiles.release()
        self.__explosions.release()
        self.__thrusts.release()
        self.__heath_bars.release()

    def __handle_events(self, event: Event) -> None:
        """Handles game events for the gameplay state.

        Args:
            event: The game event to handle.
        """

        if event.event == Events.PLAYER1_FIRES:
            self.__spawn_projectile(PlayerId.PLAYER1, event.pos, event.vel)
        if event.event == Events.PLAYER2_FIRES:
            self.__spawn_projectile(PlayerId.PLAYER2, event.pos, event.vel)
        if event.event == Events.THRUST:
            self.__spawn_thrust(event.pos, event.dir_)
        if event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__kill_projectile(event.projectile)
        if event.event == Events.THRUST_EXHAUSTED:
            self.__kill_thrust(event.thrust)
        if event.event == Events.EXPLOSION_OVER:
            self.__kill_explosion(event.explosion)
        if event.event == Events.PLAYER_DIED:
            self.__kill_player(event.player)
            self.__game_over()

        if event.event == Events.GAMEOVER:
            self.done = True
            logger.info("Game over!")

    def __spawn_projectile(self, player: PlayerId, position: Vector2, velocity: Vector2) -> None:
        """Spawns a projectile of the given type at the specified position.

        Args:
            projectile_type: The type of projectile to spawn.
            position: The position to spawn the projectile at.
            velocity: The velocity of the projectile.
        """

        projectile = ProjectileFactory.create_projectile(player, position, velocity)
        self.__projectiles.add(projectile)

    def __spawn_thrust(self, position: Vector2, direction: Vector2) -> None:
        """Spawns a thrust at the given position.

        Args:
            position: The position to spawn the thrust at.
            direction: The direction of the thrust.
        """
        self.__thrusts.add(Thrust(position, direction))

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

    def __kill_thrust(self, thrust: Thrust) -> None:
        """Removes the given thrust from the game.

        Args:
            thrust: The thrust to remove.
        """

        if thrust in self.__thrusts:
            self.__thrusts.remove(thrust)
            del thrust
        else:
            logger.error("Trying to remove a thrust that is not in the game.")

    def __kill_explosion(self, explosion: Explosion) -> None:
        """Removes the given explosion from the game.

        Args:
            explosion: The explosion to remove.
        """

        if explosion in self.__explosions:
            self.__explosions.remove(explosion)
            del explosion
        else:
            logger.error("Trying to remove an explosion that is not in the game.")

    def __kill_player(self, player: Player) -> None:
        """Removes the given player from the game.

        Args:
            player: The player to remove.
        """

        if player in self.__players:
            logger.info(f"Player {player} died.")
            self.__players.remove(player)
            del player
        else:
            logger.error(f"Trying to remove a player {player} that is not in the game.")

    def __detect_collisions(self) -> None:
        """Detects collisions between the players and the projectiles.

        For efficiency reasons, we only check for mask collisions if the collision is first
        detected by the rectangle.
        """
        for player in pygame.sprite.groupcollide(self.__players, self.__projectiles, False, False).keys():

            if pygame.sprite.groupcollide(self.__players, self.__projectiles, False, True, pygame.sprite.collide_mask):
                logger.info("Player hit by projectile (mask)!")
                self.__spawn_explosion(player.pos)
                hit_event = Event(USEREVENT, event=Events.PLAYER_HIT, player=player, damage=random.randint(10, 20))
                pygame.event.post(hit_event)

        for i, player1 in enumerate(self.__players):
            for player2 in self.__players.sprites()[i + 1 :]:
                if player1.pos != player2.pos and pygame.sprite.collide_mask(player1, player2):
                    logger.info("Player hit by player (mask)!")
                    self.__spawn_explosion(player1.pos)
                    self.__spawn_explosion(player2.pos)
                    self.__kill_player(player1)
                    self.__kill_player(player2)

    def __spawn_explosion(self, position: Vector2) -> None:
        """Spawns an explosion at the given position.

        Args:
            position: The position to spawn the explosion at.
        """
        logger.info(f"Explosion at {position}")
        self.__explosions.add(Explosion(position))

    def __game_over(self, trigger_delay: int = 3000) -> None:
        """Post gameover event with some delay after the kill."""
        logger.info("Game over event triggered.")
        gameover_event = Event(USEREVENT, event=Events.GAMEOVER, color=(0, 0, 0))
        pygame.time.set_timer(gameover_event, trigger_delay, 1)
