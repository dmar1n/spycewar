"""Module for configuration management following the singleton pattern."""

from __future__ import annotations

import json
import sys
from importlib import resources
from pathlib import Path

from loguru import logger


def cfg(*args: str) -> dict:
    """Helper method to get a configuration value using a path of keys.

    Example:
        cfg("fps") -> 60
        cfg("window", "width") -> 800

    Args:
        *args: The keys of the configuration path.
    """
    data = Config.get_instance().data
    for arg in args:
        data = data[arg]
    return data


class Config:
    """Singleton class for configuration management."""

    __instance = None  # private class variable (not instance variable)
    __internal_path = "config"
    __filename = "config.json"
    __settings: dict = {}

    @classmethod
    def get_instance(cls) -> Config:
        """Get the singleton instance."""

        return cls.__instance if cls.__instance is not None else cls()

    def __init__(self) -> None:
        """Create the singleton instance."""

        if Config.__instance is not None:
            raise RuntimeError("A singleton does not allow multiple instances. Use get_instance() instead.")

        Config.__instance = self
        self.__load_config()

    @property
    def data(self) -> dict:
        """Get the configuration settings."""

        return self.__settings

    @data.setter
    def data(self, values: dict) -> None:
        """Set the configuration settings."""

        self.__settings = values

    def reload(self) -> None:
        """Reload the configuration from the file."""

        self.__load_config()

    def __get_internal_path(self) -> Path:
        """Get the internal path of the configuration file."""

        return Path(str(resources.files(Config.__internal_path).joinpath(Config.__filename)))

    def __load_config(self) -> None:
        """Reload the configuration from the file."""

        file_path = self.__get_internal_path()
        self.__load_config_from_json(file_path)

    def __load_config_from_json(self, file_path: Path) -> None:
        """Load the configuration from a file."""

        logger.info(f"Loading configuration from: {file_path}")

        with open(Path(file_path), encoding="utf_8") as file:
            self.__settings = json.load(file)


def main() -> int:
    """Main entry point for the script."""

    config = Config.get_instance()
    print(config.data)
    config.data = {"key": "value"}  # overwrite the configuration
    print(config.data)
    config.reload()
    print(config.data)
    print(cfg("fps"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
