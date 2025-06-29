"""Module for the health bar of the players."""

from pygame import Surface
from pygame.event import Event

from spycewar.assets.fonts.utils import initialise_font
from spycewar.config import get_cfg
from spycewar.entities.bars import BarBase
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


class HealthBar(GameObject, BarBase):
    """Represents the health bar of a player."""

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        """Initialise the health bar."""
        GameObject.__init__(self)
        BarBase.__init__(self, x, y, 150, 15, (120, 120, 120))
        self.player_id = player_id
        self.__max_hp = get_cfg("entities", "players", player_id.value, "max_health")
        self.__hp = self.__max_hp
        self.__font = initialise_font("eurostile.ttf", 12)

    @property
    def ratio(self) -> float:
        """The ratio of the current health to the maximum health."""
        return self.__hp / self.__max_hp

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for the health bar.

        Args:
            event: the event to process.
        """
        if event.event == Events.PLAYER_HIT and event.player.state.player_id == self.player_id:
            self.__hp = event.player.state.health
        if event.event == Events.HEALTH_POWERUP_PICKUP and event.player.state.player_id == self.player_id:
            self.__hp = event.player.state.health

    def update(self, delta_time: float) -> None:
        """Update the health bar."""

    def render(self, surface_dst: Surface) -> None:
        """Render the health bar on the screen.

        Args:
            surface_dst: the surface to render the health bar on.
        """
        color = (220, 220, 220) if self.ratio > 0.2 else "red"
        self.render_bar(surface_dst, self.ratio, color)
        surface_dst.blit(
            self.__font.render(f"{self.player_id.name}", True, (0, 0, 0)),
            (self._x + 5, self._y + 2),
        )

    def release(self) -> None:
        """Release the health bar."""
