"""This module contains the Repository class."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from datetime import datetime
from typing import Any


@dataclass(frozen=True, eq=False)
class Repository:
    """Parsed GitHub repository."""

    name: str
    html_url: str
    created_at: str
    description: str | None = None
    topics: list[str] = field(default_factory=list)
    homepage: str | None = None
    default_branch: str = "main"
    id: int | None = None
    private: bool = False
    stargazers_count: int = 0
    watchers_count: int = 0
    updated_at: str | None = None
    pushed_at: str | None = None
    size: int = 0
    languages: list[dict[str, Any]] = field(default_factory=list)
    commits_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0
    watchers: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any], **extra: Any) -> Repository:
        """Create a Repository from a dict, ignoring unknown keys.

        Args:
            data (dict[str, Any]): repository data, e.g. from the GitHub API.
            **extra: additional values, overriding the ones in `data`.

        Returns:
            Repository
        """
        known = {f.name for f in fields(cls)}
        values = {k: v for k, v in (data | extra).items() if k in known}
        return cls(**values)

    def as_dict(self) -> dict[str, Any]:
        """Return the dict representation of the repository."""
        return asdict(self)

    @property
    def created_at_obj(self) -> datetime:
        """Creation date, as a datetime."""
        return datetime.fromisoformat(self.created_at)

    @property
    def created_at_formatted(self) -> str:
        """Creation date, formatted as YYYY-MM-DD."""
        return self.created_at_obj.strftime("%Y-%m-%d")

    @property
    def last_push(self) -> str:
        """Date of the last push, or the creation date if never pushed."""
        return self.pushed_at or self.created_at

    @property
    def last_push_formatted(self) -> str:
        """Date of the last push, formatted as YYYY-MM-DD."""
        return datetime.fromisoformat(self.last_push).strftime("%Y-%m-%d")

    @property
    def language(self) -> str | None:
        """Main language of the repository, if any."""
        if not self.languages:
            return None
        return self.languages[0]["language"]

    @property
    def name_formatted(self) -> str:
        """Name of the repository, in a human-readable form."""
        return self.name.replace("-", " ").lower()

    @property
    def description_formatted(self) -> str:
        """Description, capitalised and without the final period."""
        if not self.description:
            return ""
        description = self.description[0].upper() + self.description[1:]
        return description.removesuffix(".")

    @property
    def interactive_url(self) -> str:
        """Where to send the visitors of an interactive repo.

        This is the homepage, or the repository itself if it has none.
        """
        return self.homepage or self.html_url
