"""Typed settings, loaded from a TOML file and overridable via environment."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class _Section:
    """Base class for a settings section.

    The section name in the TOML file is the class name without the "Settings"
    suffix. Fields typed as `str` can be overridden by an environment variable
    named `<SECTION>_<FIELD>` (e.g. `DEPLOYER_PRIVATE_KEY`). Fields typed as
    `Path` are resolved relative to the folder containing the TOML file; an
    empty path is treated as unset.
    """

    @classmethod
    def section_name(cls) -> str:
        """Return the name of the section in the TOML file.

        Returns:
            str: the section name.
        """
        return cls.__name__.removesuffix("Settings")

    @classmethod
    def from_toml(cls, path: Path) -> Self:
        """Load the section from a TOML file, applying environment overrides.

        Args:
            path (Path): path to the TOML file.

        Returns:
            Self: the loaded settings.

        Raises:
            ValueError: if the section is missing or contains unknown keys.
        """
        with path.open("rb") as f:
            data = tomllib.load(f)

        name = cls.section_name()
        if name not in data:
            raise ValueError(f"Section {name} not found in {path}")

        values = dict(data[name])
        unknown = set(values) - {f.name for f in fields(cls)}
        if unknown:
            raise ValueError(f"Unknown keys in section {name}: {sorted(unknown)}")

        base_dir = path.resolve().parent
        for f in fields(cls):
            env_value = os.environ.get(f"{name.upper()}_{f.name.upper()}")
            if env_value is not None and f.type == "str":
                values[f.name] = env_value
            elif f.name in values and f.type.startswith("Path"):
                raw = values[f.name]
                values[f.name] = (base_dir / raw).resolve() if raw else None

        return cls(**values)


@dataclass(frozen=True)
class ScraperSettings(_Section):
    """GitHub scraper settings."""

    username: str
    token: str = ""
    relevant_topics: list[str] = field(default_factory=list)
    skip_interactive_names: list[str] = field(default_factory=list)
    skip_interactive_topics: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuilderSettings(_Section):
    """Site builder settings."""

    templates_path: Path
    static_path: Path
    data_path: Path
    output_path: Path


@dataclass(frozen=True)
class DeployerSettings(_Section):
    """SFTP deployer settings."""

    hostname: str
    username: str = ""
    private_key: str = ""
    private_key_path: Path | None = None
    private_key_passphrase: str = ""
    server_public_key: str = ""
    remote_path: str = ""
