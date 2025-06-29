"""Utility for loading projectile images for player projectiles."""

from importlib import resources
from typing import Any

from spycewar.assets.images.utils import load_image
from spycewar.config import get_cfg
from spycewar.entities.players.enums import PlayerId


def load_player_projectile_image(player_id: PlayerId) -> tuple[Any, int, int]:
    """Load the projectile image for the given player.

    Args:
        player_id: The ID of the player whose projectile image to load.

    Returns:
        A tuple containing the loaded image, its mid-width, and mid-height.
    """

    file_dir, filename = get_cfg(
        "entities",
        "projectiles",
        player_id.value,
        "file",
    )
    file_path = resources.files(file_dir).joinpath(filename)
    image = load_image(file_path)
    mid_width = image.get_width() / 2
    mid_height = image.get_height() / 2
    return image, mid_width, mid_height
