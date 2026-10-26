"""Scraper module."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from modules.github import GitHub
from modules.repository import Repository
from modules.settings import ScraperSettings

logger = logging.getLogger(__name__)


class Scraper:
    """Collects the repositories and groups them for the website."""

    def __init__(self, settings: ScraperSettings, github: GitHub | None = None) -> None:
        """Create a new Scraper instance.

        Args:
            settings (ScraperSettings): scraper settings.
            github (GitHub | None, optional): GitHub client. If None, one is
                created from the settings. Defaults to None.
        """
        self._settings = settings
        self._github = github or GitHub(settings.username, settings.token)
        self._repos: list[Repository] = []

    def scrape_repos(self, *, skip_private: bool = True) -> None:
        """Load the repos from GitHub.

        Args:
            skip_private (bool, optional): if true, private repos are skipped.
                Defaults to True.
        """
        repos = self._github.get_repos(skip_private=skip_private)
        self._repos = sorted(repos, key=lambda x: x.created_at)

    def save_repos(self, path: Path) -> None:
        """Save repos list to file.

        Args:
            path (Path): file path.
        """
        logger.info("Saving repos to %s", path)
        data = {"Repositories": [r.as_dict() for r in self._repos]}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_repos(self, path: Path) -> None:
        """Load repos list from file.

        Args:
            path (Path): file path.
        """
        logger.info("Loading repos from %s", path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self._repos = [Repository.from_dict(r) for r in data["Repositories"]]
        logger.info("Loaded %d repos", len(self._repos))

    def save_stats(self, path: Path) -> None:
        """Save stats to file.

        Args:
            path (Path): file path.
        """
        logger.info("Saving stats to %s", path)
        path.write_text(json.dumps(self.stats, indent=2), encoding="utf-8")

    def _get_languages_stat(self) -> dict[str, dict]:
        languages: dict[str, dict] = {}

        for repo in self._repos:
            for language in repo.languages:
                stat = languages.setdefault(
                    language["language"], {"size": 0, "repos": 0}
                )
                stat["size"] += language["size"]
                stat["repos"] += 1

        total_size = sum(lang["size"] for lang in languages.values()) or 1
        for stat in languages.values():
            stat["relative_size"] = stat["size"] / total_size
            stat["relative_size_formatted"] = f"{stat['relative_size']:.2%}"

        return languages

    @property
    def repos(self) -> list[Repository]:
        """All the loaded repos, oldest first."""
        return self._repos

    @property
    def interesting_repos(self) -> list[Repository]:
        """Repos with at least one of the relevant topics."""
        return [
            r
            for r in self._repos
            if any(t in r.topics for t in self._settings.relevant_topics)
        ]

    @property
    def interactive_repos(self) -> list[Repository]:
        """Interesting repos that have a homepage, newest first."""
        repos = [
            r
            for r in self.interesting_repos
            if r.is_interactive
            and all(t not in r.topics for t in self._settings.skip_interactive_topics)
            and r.name not in self._settings.skip_interactive_names
        ]
        return sorted(repos, key=lambda x: x.created_at, reverse=True)

    @property
    def repos_list(self) -> dict[str, list[Repository]]:
        """Interesting repos grouped by main language, newest first."""
        grouped: dict[str, list[Repository]] = {}
        for repo in self.interesting_repos:
            if repo.language:
                grouped.setdefault(repo.language, []).append(repo)

        return {
            lang: sorted(grouped[lang], key=lambda x: x.created_at, reverse=True)
            for lang in sorted(grouped)
        }

    @property
    def stats(self) -> dict[str, Any]:
        """Statistics about the loaded repos."""
        return {
            "total_repos": len(self._repos),
            "interesting_repos": len(self.interesting_repos),
            "interactive_repos": len(self.interactive_repos),
            "languages": self._get_languages_stat(),
            "stargazers_count": sum(r.stargazers_count for r in self._repos),
            "forks_count": sum(r.forks_count for r in self._repos),
            "watchers_count": sum(r.watchers_count for r in self._repos),
            "open_issues_count": sum(r.open_issues_count for r in self._repos),
            "commits_count": sum(r.commits_count for r in self._repos),
            "github_requests_count": self._github.requests_count,
        }
