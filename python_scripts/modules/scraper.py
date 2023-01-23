from __future__ import annotations

import logging

import ujson

from .github import GitHub, Repo
from .settings import Settings


class Scraper(GitHub):
    _repos: list[Repo]
    _settings: Settings
    _settings_path: str

    def __init__(self, settings_path: str = "settings.toml"):
        logging.info(f"Initializing {self.__class__.__name__}...")
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)
        super().__init__(self._settings.username, self._settings.token)

    def scrapeRepos(self, skip_private: bool = True) -> int:
        logging.info("Loading repos...")
        repos = []
        repo_names = self.getReposNames(skip_private=skip_private)

        for repo_name in repo_names:
            repos.append(self.getRepoByName(repo_name))

        self._repos = sorted(
            repos,
            key=lambda x: x.created_at,
        )

        logging.info(f"Loaded {len(self._repos)} repos")
        return len(self._repos)

    def saveRepos(self, path: str = None) -> None:
        if path is None:
            path = self._settings.out_path + "repos.json"

        logging.info(f"Saving repos to {path}")
        with open(path, "w") as f:
            ujson.dump([r.as_dict for r in self._repos], f, indent=4)
        logging.info(f"Saved {len(self._repos)} repos")

    def loadRepos(self, path: str = None) -> None:
        if path is None:
            path = self._settings.out_path + "repos.json"

        logging.info(f"Loading repos from {path}")
        with open(path, "r") as f:
            self._repos = [Repo(**repo) for repo in ujson.load(f)]
        logging.info(f"Loaded {len(self._repos)} repos")

    def reposByLanguage(self, language: str) -> set[Repo]:
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
        return self._repos

    @property
    def interesting_repos(self) -> list[Repo]:
        return sorted(
            [
                r
                for r in self._repos
                if any(t in r.topics for t in self._settings.relevant_topics)
            ],
            key=lambda x: x.created_at,
            reverse=True,
        )

    @property
    def interactive_repos(self) -> list[Repo]:
        return [r for r in self.interesting_repos if r.is_interactive]

    @property
    def repos_list(self) -> list[dict[str, list[Repo]]]:
        languages = sorted(
            list(
                set([repo.language for repo in self.interesting_repos if repo.language])
            )
        )
        repos = {lang: [] for lang in languages}

        for lang in repos.keys():
            lang_repos = sorted(
                self.reposByLanguage(lang),
                key=lambda x: x.created_at,
            )
            repos[lang] = lang_repos

        return repos

    @property
    def stats(self) -> list[str]:
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
