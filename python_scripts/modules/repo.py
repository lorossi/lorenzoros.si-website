"""This module contains the Repo class."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import ujson


class Repo:
    """Parsed GitHub repo class."""

    _frozen: bool = False
    _attributes = [
        "name",
        "description",
        "html_url",
        "topics",
        "homepage",
        "id",
        "private",
        "stargazers_count",
        "watchers_count",
        "created_at",
        "updated_at",
        "pushed_at",
        "size",
        "languages",
        "commits_count",
        "forks_count",
        "open_issues_count",
        "watchers",
    ]

    _time_attributes = list(filter(lambda x: x.endswith("_at"), _attributes))

    def __init__(self, **kwargs):
        """Initialize the object."""
        for a in self._attributes:
            self.__setattr__(a, kwargs.get(a))
        self._frozen = True

    @classmethod
    def from_json(
        cls, json_data: dict, languages: list[dict], commits_count: int
    ) -> Repo:
        """Create a Repo object from a json.

        Args:
            json_data (dict)
            languages (list[dict])
            commits_count (int)

        Returns:
            Repo: _description_
        """
        return cls(**json_data, languages=languages, commits_count=commits_count)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set the attribute of the object.

        Args:
            name (str)
            value (_type_)

        Raises:
            AttributeError: If the attribute cannot be modified.
        """
        if name not in self._attributes:
            return

        if self._frozen:
            raise AttributeError(
                f"Attribute {name} cannot be modified in {self.__class__.__name__}"
            )

        super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Any:
        """Get the attribute of the object.

        Args:
            name (str)

        Raises:
            AttributeError: If the attribute does not exist.

        Returns:
            Any
        """
        if name in self._attributes:
            return self.__getattribute__(name)

        if (n := name.replace("_obj", "")) in self._time_attributes:
            a = self.__getattribute__(n).replace("Z", "+00:00")
            return datetime.fromisoformat(a)

        if (n := name.replace("_formatted", "")) in self._time_attributes:
            a = self.__getattribute__(n).replace("Z", "+00:00")
            return datetime.fromisoformat(a).strftime("%Y-%m-%d")

        if name == "language":
            if len(self.languages) == 0:
                return None
            return self.languages[0]["language"]

        if name == "name_formatted":
            return self.name.replace("-", " ").lower()

        if name == "description_formatted":
            description = self.description[0].upper() + self.description[1:]
            if description.endswith("."):
                return description[:-1]
            return description

        if name == "languages_set":
            return set([lang["language"] for lang in self.languages])

        raise AttributeError(
            f"Attribute {name} does not exist in {self.__class__.__name__}"
        )

    def __repr__(self) -> str:
        """Return the representation of the object."""
        attributes = ", ".join(
            [f"{a}={self.__getattribute__(a)!r}" for a in self._attributes]
        )
        return f"{self.__class__.__name__}({attributes})"

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return self.__repr__()

    @property
    def json(self) -> str:
        """Return the json representation of the object."""
        return ujson.dumps(self.as_dict, sort_keys=True, indent=4)

    @property
    def as_dict(self) -> dict:
        """Return the dict representation of the object."""
        return {k: self.__getattribute__(k) for k in self._attributes}

    @property
    def is_interactive(self) -> bool:
        """Return True if the repo is interactive."""
        return self.homepage != "" and self.homepage is not None
