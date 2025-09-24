"""Scraper module."""

from __future__ import annotations

import logging

import ujson

from modules.github import GitHub, Repo
from modules.settings import Settings


class Scraper(GitHub):
    """Scraper class."""

    _repos: list[Repo]
    _settings: Settings
    _settings_path: str

    def __init__(self, settings_path: str = "settings.toml") -> Scraper:
        """Create a new Scraper instance."""
        logging.info("Initializing %s...", self.__class__.__name__)
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)
        super().__init__(self._settings.username, self._settings.token)

    def scrapeRepos(self, skip_private: bool = True) -> int | None:
        """Scrape the repos.

        Args:
            skip_private (bool, optional): if true, private repos are skipped. \
                Defaults to True.

        Returns:
            int: _description_
        """
        logging.info("Loading repos...")
        repos = []
        repo_names = self.getReposNames(skip_private=skip_private)

        try:
            for repo_name in repo_names:
                repos.append(self.getRepoByName(repo_name))
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt, exiting...")
            return None

        self._repos = sorted(repos, key=lambda x: x.created_at)

        logging.info("Loaded %s repos", len(self._repos))
        return len(self._repos)

    def saveStats(self, path: str | None = None) -> None:
        """Save stats to file.

        Args:
            path (str, optional): file path. Defaults to value from settings.
        """
        if path is None:
            path = self._settings.out_path + "stats.json"

        logging.info("Saving stats to %s", path)
        with open(path, "w") as f:
            ujson.dump(self.stats, f, sort_keys=True, indent=4)
        logging.info("Saved stats")

    def saveRepos(self, path: str | None = None) -> None:
        """Save repos list to file.

        Args:
            path (str, optional): file path. Defaults to value from settings.
        """
        if path is None:
            path = self._settings.out_path + "repos.json"

        logging.info("Saving repos to %s", path)
        with open(path, "w") as f:
            ujson.dump([r.as_dict for r in self._repos], f, sort_keys=True, indent=4)
        logging.info("Saved %s repos", len(self._repos))

    def loadRepos(self, path: str | None = None) -> None:
        """Load repos list from file.

        Args:
            path (str, optional): file path. Defaults to value from settings.
        """
        if path is None:
            path = self._settings.out_path + "repos.json"

        logging.info("Loading repos from %s", path)
        with open(path, "r") as f:
            self._repos = sorted(
                [Repo(**repo) for repo in ujson.load(f)], key=lambda x: x.created_at
            )
        logging.info("Loaded %s repos", len(self._repos))

    def reposByLanguage(self, language: str) -> set[Repo]:
        """Get a set of interesting repos written in a set language.

        Args:
            language (str): language name

        Returns:
            set[Repo]: set of repos
        """
        return set(
            filter(
                lambda x: x.language == language,
                self.interesting_repos,
            )
        )

    def _getLanguagesStat(self) -> dict[str, dict]:
        languages = dict()

        for repo in self._repos:
            for language in repo.languages:
                name = language["language"]
                if name not in languages:
                    languages[name] = {"size": 0, "repos": 0}

                languages[name]["size"] += language["size"]
                languages[name]["repos"] += 1

        total_size = sum(lang["size"] for lang in languages.values())

        for language in languages.values():
            relative_size = language["size"] / total_size
            language["relative_size"] = relative_size
            language["relative_size_formatted"] = f"{relative_size:.2%}"

        return languages

    @property
    def repos(self) -> list[Repo]:
        """Get the list of repos."""
        return self._repos

    @property
    def interesting_repos(self) -> list[Repo]:
        """Get the list of interesting repos."""
        return sorted(
            [
                r
                for r in self._repos
                if any(t in r.topics for t in self._settings.relevant_topics)
            ],
            key=lambda x: x.created_at,
        )

    @property
    def languages(self) -> list[str]:
        """Get the list of languages used in all the repositories."""
        languages = set(repo.language for repo in self._repos if repo.language)
        return sorted(languages)

    @property
    def interactive_repos(self) -> list[Repo]:
        """Get the list of interactive repos."""
        repos = [
            r
            for r in self.interesting_repos
            if r.is_interactive
            and all(t not in r.topics for t in self._settings.skip_interactive_topics)
            and r.name not in self._settings.skip_interactive_names
        ]
        return sorted(repos, key=lambda x: x.created_at, reverse=True)

    @property
    def repos_list(self) -> list[dict[str, list[Repo]]]:
        """Get the list of repos grouped by language."""
        repos = {}

        for lang in self.languages:
            lang_repos = sorted(
                self.reposByLanguage(lang),
                key=lambda x: x.created_at,
                reverse=True,
            )
            if lang_repos:
                repos[lang] = lang_repos

        return repos

    @property
    def stats(self) -> list[str]:
        """Get the stats."""
        stats = {}
        stats["total_repos"] = len(self._repos)
        stats["interesting_repos"] = len(self.interesting_repos)
        stats["interactive_repos"] = len(self.interactive_repos)
        stats["languages"] = self._getLanguagesStat()
        stats["stargazers_count"] = sum(r.stargazers_count for r in self._repos)
        stats["forks_count"] = sum(r.forks_count for r in self._repos)
        stats["watchers_count"] = sum(r.watchers_count for r in self._repos)
        stats["open_issues_count"] = sum(r.open_issues_count for r in self._repos)
        stats["commits_count"] = sum(r.commits_count for r in self._repos)

        return stats
