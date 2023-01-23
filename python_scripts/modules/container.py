from __future__ import annotations

from typing_extensions import Any
import toml


class Container:
    def __init__(self, **kwargs: Any) -> None:
        self._container = {}
        for key, value in kwargs.items():
            self._container[key] = value

    def __getattr__(self, key: str) -> Any:
        return self._container[key]

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._container[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._container

    def __repr__(self) -> str:
        sorted_items = sorted(self._container.items(), key=lambda x: x[0])
        container_repr = ", ".join(f"{str(k)}={str(v)}" for k, v in sorted_items)
        return f"{self.__class__.__name__}({container_repr})"

    def __len__(self) -> int:
        return len(self._container)

    def __iter__(self):
        return iter(self._container)

    def __getitem__(self, key: str) -> Any:
        return self.__getattr__(key)

    def items(self):
        return self._container.items()

    def keys(self):
        return self._container.keys()

    def values(self):
        return self._container.values()

    def copy(self) -> Container:
        return self.__class__(**self._container)

    def update(self, other: Container) -> None:
        for key, value in other.items():
            self._container[key] = value

    def get(self, key: str, default: Any = "") -> Any:
        return self._container.get(key, default)

    @classmethod
    def from_toml(cls, toml_file: str) -> Container:
        return cls(**toml.load(toml_file))

    def to_toml(self, toml_file: str) -> None:
        with open(toml_file, "w") as f:
            toml.dump(self._container, f)
