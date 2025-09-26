"""Settings class for the project."""

from __future__ import annotations

from typing import Any

import toml


class Settings:
    """Settings class.

    Supports access to the settings as attributes and as dictionary keys.
    Can be instantiated from a TOML file.
    """

    _settings: dict

    def __init__(self, **kwargs) -> None:
        """Create a new Settings instance."""
        self._settings = kwargs

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""
        if name in self._settings:
            return self._settings[name]

        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

    @staticmethod
    def from_toml(path: str, section: str | None = None) -> Settings:
        """Create a new Settings instance from a TOML file.

        Args:
            path (str): Path to the TOML file.
            section (str, optional): Section to load. If None, loads the whole file.
                Defaults to None.

        Returns:
            Settings: Settings instance.
        """
        with open(path, "r") as f:
            settings = toml.load(f)

        if section is not None:
            if section not in settings:
                raise ValueError(f"Section {section} not found in {path}")

            settings = settings[section]

        return Settings(**settings)
