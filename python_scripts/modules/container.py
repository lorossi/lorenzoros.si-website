"""Container class for storing data in a dictionary-like object. Supports access to the data as attributes and as dictionary keys."""
from __future__ import annotations

from typing_extensions import Any
import toml


class Container:
    """Container class."""

    def __init__(self, **kwargs: Any) -> None:
        """Create a new Container instance.

        Args:
            **kwargs: Key-value pairs to store in the container.
        """
        self._container = {}
        for key, value in kwargs.items():
            self._container[key] = value

    def __getattr__(self, key: str) -> Any:
        """Get an item from the container."""
        return self._container[key]

    def __setattr__(self, key: str, value: Any) -> None:
        """Set an item in the container."""
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._container[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if the container contains a key."""
        return key in self._container

    def __repr__(self) -> str:
        """Return a string representation of the container."""
        sorted_items = sorted(self._container.items(), key=lambda x: x[0])
        container_repr = ", ".join(f"{str(k)}={str(v)}" for k, v in sorted_items)
        return f"{self.__class__.__name__}({container_repr})"

    def __str__(self) -> str:
        """Return a string representation of the container."""
        return repr(self)

    def __len__(self) -> int:
        """Return the number of items in the container."""
        return len(self._container)

    def __iter__(self):
        """Return an iterator over the container."""
        return iter(self._container)

    def __getitem__(self, key: str) -> Any:
        """Get an item from the container."""
        return self.__getattr__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item in the container."""
        self.__setattr__(key, value)

    def items(self):
        """Return items in the container."""
        return self._container.items()

    def keys(self):
        """Return keys in the container."""
        return self._container.keys()

    def values(self):
        """Return values in the container."""
        return self._container.values()

    def copy(self) -> Container:
        """Return a copy of the container."""
        return self.__class__(**self._container)

    def update(self, other: Container) -> None:
        """Update the container with the items from another container."""
        for key, value in other.items():
            self._container[key] = value

    def get(self, key: str, default: Any = "") -> Any:
        """Get an item from the container."""
        return self._container.get(key, default)

    @classmethod
    def from_toml(cls, toml_file: str) -> Container:
        """Create a new Container instance from a TOML file.

        Args:
            toml_file (str): Path to the TOML file.
        """
        return cls(**toml.load(toml_file))

    def to_toml(self, toml_file: str) -> None:
        """Write the container to a TOML file.

        Args:
            toml_file (str): Path to the TOML file.
        """
        with open(toml_file, "w") as f:
            toml.dump(self._container, f)
