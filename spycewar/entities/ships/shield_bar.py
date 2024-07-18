"""Module for the shield bar of the players."""

from pygame import Surface
from pygame.draw import rect
from pygame.event import Event

from spycewar.config import get_cfg
from spycewar.entities.game_object import GameObject
from spycewar.entities.players.enums import PlayerId
from spycewar.events import Events


class ShieldBar(GameObject):
    """Represents the shield bar of a player."""

    __empty_color = (99, 99, 99)

    def __init__(self, player_id: PlayerId, x: int, y: int) -> None:
        super().__init__()
        self.player_id = player_id
        self.__x = x
        self.__y = y
        self.__width = 150
        self.__height = 7
        self.__max_shield = get_cfg("entities", "ships", player_id.value, "max_shield")
        self.__shield = self.__max_shield

    @property
    def ratio(self) -> float:
        """The ratio of the current shield to the maximum shield."""

        return self.__shield / self.__max_shield

    def handle_input(self, key: int, is_pressed: bool) -> None:
        pass

    def process_events(self, event: Event) -> None:
        if event.event == Events.SHIELD_ACTIVATED and event.player.state.player_id == self.player_id:
            self.__shield = event.player.state.shield

    def update(self, delta_time: float) -> None:
        """Update the shield bar."""

    def render(self, surface_dst: Surface) -> None:
        """Render the shield bar on the screen.

        Args:
            surface_dst: the surface to render the shield bar on.
        """
        color = (90, 144, 178) if self.ratio > 0.2 else ("orange")
        rect(surface_dst, self.__empty_color, (self.__x, self.__y, self.__width, self.__height))
        rect(surface_dst, color, (self.__x + 1, self.__y + 1, self.__width * self.ratio - 2, self.__height - 2))

    def release(self) -> None:
        """Release the shield bar."""
