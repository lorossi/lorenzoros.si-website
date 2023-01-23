"""Settings class for the project."""

from __future__ import annotations

import toml

from .container import Container


class Settings(Container):
    """Settings class.

    Supports access to the settings as attributes and as dictionary keys.
    Can be instantiated from a TOML file.
    """

    def __init__(self, **kwargs) -> Settings:
        """Create a new Settings instance."""
        super().__init__(**kwargs)

    @classmethod
    def from_toml(cls, path: str, section: str = None):
        """Create a new Settings instance from a TOML file.

        Args:
            path (str): Path to the TOML file.
            section (str, optional): Section to load. Defaults to None.

        Returns:
            Settings: Settings instance.
        """
        with open(path, "r") as f:
            settings = toml.load(f)

        if section:
            return cls(**settings[section])
        return cls(**settings)
