"""Module for storing game context data."""

from typing import Any


class GameContext:
    """Represents the game context data to be passed between states if necessary.

    The states are entered with a GameContext object. Each state can invoke the `set_data` method to
    store a key/value pair in the context data. This data can be accessed by other states in the same way,
    calling the property `data`.

    Attributes:
        __data: A dictionary to store the context data.

    Methods:
        set_data: Sets the context data as key/value pairs.
        data: Returns the context data as a dictionary.
    """

    def __init__(self) -> None:
        self.__data: dict = {}

    def set_data(self, **kwargs: Any) -> None:
        """Sets the context data."""
        self.__data.update(**kwargs)

    @property
    def data(self) -> dict:
        """Returns the context data."""
        return self.__data
