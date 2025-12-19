"""Module for the hyperspace cooldown bar of the players."""

from pygame import Surface
from pygame.event import Event

from spycewar.entities.bars import BarBase
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.player import Player


class HyperspaceBar(GameObject, BarBase):
    """Represents the hyperspace cooldown bar of a player."""

    def __init__(self, player: Player, x: int, y: int) -> None:
        """Initialise the hyperspace cooldown bar."""
        GameObject.__init__(self)
        BarBase.__init__(self, x, y, 150, 5, (80, 80, 80))
        self.__player = player
        self.__max_cooldown = max(player.specs.hyperspace_cooldown, 0.0)

    @property
    def ratio(self) -> float:
        """The ratio of the cooldown that has elapsed."""
        if self.__max_cooldown <= 0.0:
            return 1.0
        remaining = max(self.__player.hyperspace_cooldown, 0.0)
        return (self.__max_cooldown - remaining) / self.__max_cooldown

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for the hyperspace cooldown bar."""

    def update(self, delta_time: float) -> None:
        """Update the hyperspace cooldown bar."""

    def render(self, surface_dst: Surface) -> None:
        """Render the hyperspace cooldown bar on the screen.

        Args:
            surface_dst: the surface to render the hyperspace cooldown bar on.
        """
        color = (120, 200, 120) if self.ratio >= 1.0 else (200, 170, 90)
        self.render_bar(surface_dst, self.ratio, color)

    def release(self) -> None:
        """Release the hyperspace cooldown bar."""
