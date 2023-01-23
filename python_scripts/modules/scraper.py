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
        self._repos = []
        repo_names = self.getReposNames(skip_private=skip_private)

        for repo_name in repo_names:
            self._repos.append(self.getRepoByName(repo_name))

        logging.info(f"Loaded {len(self._repos)} repos")
        return len(self._repos)

    def saveRepos(self, path: str = "repos.json") -> None:
        logging.info(f"Saving repos to {path}")
        with open(path, "w") as f:
            ujson.dump([r.as_dict for r in self._repos], f, indent=4)
        logging.info(f"Saved {len(self._repos)} repos")

    def loadRepos(self, path: str = "repos.json") -> None:
        logging.info(f"Loading repos from {path}")
        with open(path, "r") as f:
            self._repos = [Repo(**repo) for repo in ujson.load(f)]
        logging.info(f"Loaded {len(self._repos)} repos")

    def reposByLanguage(self, language: str) -> list[Repo]:
        return set(
            filter(
                lambda x: x.language == language,
                self.interesting_repos,
            )
        )

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

        for lang in languages:
            lang_repos = sorted(
                self.reposByLanguage(lang),
                key=lambda x: x.created_at,
            )
            repos[lang] = lang_repos

        return repos
