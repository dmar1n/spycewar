"""Module for the shield bar of the players."""

from pygame import Surface
from pygame.event import Event

from spycewar.config import get_cfg
from spycewar.entities.bars import BarBase
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


class ShieldBar(GameObject, BarBase):
    """Represents the shield bar of a player."""

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        """Initialise the shield bar."""
        GameObject.__init__(self)
        BarBase.__init__(self, x, y, 150, 7, (99, 99, 99))
        self.player_id = player_id
        self.__max_shield = get_cfg("entities", "ships", player_id.value, "max_shield")
        self.__shield = self.__max_shield

    @property
    def ratio(self) -> float:
        """The ratio of the current shield to the maximum shield."""
        return self.__shield / self.__max_shield

    def handle_input(self, key: int, is_pressed: bool) -> None:
        """Handle the input of the player.

        Args:
            key: the key pressed by the player.
            is_pressed: a boolean indicating whether the key is pressed or released.
        """

    def process_events(self, event: Event) -> None:
        """Process events for the shield bar."""
        if event.event == Events.SHIELD_ACTIVATED and event.player.state.player_id == self.player_id:
            self.__shield = event.player.state.shield

    def update(self, delta_time: float) -> None:
        """Update the shield bar."""

    def render(self, surface_dst: Surface) -> None:
        """Render the shield bar on the screen.

        Args:
            surface_dst: the surface to render the shield bar on.
        """
        color = (90, 144, 178) if self.ratio > 0.2 else "orange"
        self.render_bar(surface_dst, self.ratio, color)

    def release(self) -> None:
        """Release the shield bar."""
