"""Tests for the settings loading."""

from pathlib import Path

import pytest

from modules.settings import BuilderSettings, DeployerSettings, ScraperSettings

TOML = """
[Scraper]
username = "someone"
relevant_topic = "released"

[Builder]
templates_path = "templates"
static_path = "../public"
data_path = "data"
blog_path = "../blog"
output_path = "../dist"
cache_path = ".cache"

[Deployer]
hostname = "example.com"
private_key_path = ""
"""


@pytest.fixture
def toml(tmp_path: Path) -> Path:
    path = tmp_path / "sub" / "settings.toml"
    path.parent.mkdir()
    path.write_text(TOML, encoding="utf-8")
    return path


def test_loads_with_defaults(toml: Path) -> None:
    settings = ScraperSettings.from_toml(toml)
    assert settings.username == "someone"
    assert settings.token == ""
    assert settings.interactive_topic == "interactive"
    assert settings.relevant_topic == "released"


def test_paths_are_relative_to_the_file(toml: Path) -> None:
    settings = BuilderSettings.from_toml(toml)
    base = toml.parent.resolve()
    assert settings.templates_path == base / "templates"
    assert settings.output_path == (base / "../dist").resolve()


def test_empty_path_is_unset(toml: Path) -> None:
    assert DeployerSettings.from_toml(toml).private_key_path is None


def test_env_overrides_strings(toml: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCRAPER_TOKEN", "secret")
    monkeypatch.setenv("SCRAPER_USERNAME", "other")
    settings = ScraperSettings.from_toml(toml)
    assert settings.token == "secret"
    assert settings.username == "other"


def test_missing_section(tmp_path: Path) -> None:
    path = tmp_path / "s.toml"
    path.write_text("[Scraper]\nusername = 'x'\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Section Builder not found"):
        BuilderSettings.from_toml(path)


def test_unknown_key(tmp_path: Path) -> None:
    path = tmp_path / "s.toml"
    path.write_text("[Scraper]\nusername = 'x'\nbogus = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="bogus"):
        ScraperSettings.from_toml(path)
