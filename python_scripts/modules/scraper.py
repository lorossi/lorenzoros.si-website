from __future__ import annotations

import logging
from datetime import datetime

import toml
import ujson

from .embedder import Embedder
from .github import GitHub, Repo
from .htmlelements import InteractiveList, StaticList


class Scraper(GitHub):
    _repos: list[Repo]
    _interactive_list: InteractiveList
    _static_list: StaticList
    _settings: dict
    _settings_path: str

    def __init__(self, settings_path: str = "settings.toml"):
        logging.info(f"Initializing {self.__class__.__name__}...")
        self._settings_path = settings_path
        self._loadSettings(settings_path)
        super().__init__(self._settings["username"], self._settings["token"])

    def _loadSettings(self, path: str) -> None:
        logging.info(f"Loading settings from {path}")
        with open(path, "r") as f:
            self._settings = toml.load(f)[self.__class__.__name__]
        logging.info("Loaded settings")

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

    def _createInteractiveList(self) -> None:
        logging.info("Creating interactive list")

        relevant_repos = sorted(
            (
                repo
                for repo in self._repos
                if repo.homepage  # the repo has a homepage
                and repo.name not in self._settings["skip_websites_names"]
                and set(repo.topics) & set(self._settings["relevant_topics"])
                and all(
                    r not in self._settings["skip_websites_topics"] for r in repo.topics
                )
            ),
            key=lambda x: x.created_at_obj,
            reverse=True,
        )

        self._interactive_list = InteractiveList(relevant_repos, self._settings_path)
        logging.info("Created interactive list")

    def _createStaticList(self) -> None:
        logging.info("Creating static list")

        relevant_repos = [
            repo
            for repo in self._repos
            if set(repo.topics) & set(self._settings["relevant_topics"])
        ]
        relevant_repos.sort(key=lambda x: x.created_at_obj, reverse=True)
        relevant_repos.sort(key=lambda x: x.language)

        self._static_list = StaticList(relevant_repos, self._settings_path)

    def createHTMLLists(self) -> None:
        self._createInteractiveList()
        self._createStaticList()

    def saveHTMLLists(self) -> None:
        out_path = self._settings["out_path"]
        self._interactive_list.saveHTML(out_path)
        self._static_list.saveHTML(out_path)

    def embedHTMLLists(self) -> None:
        self._embedder = Embedder(settings_path=self._settings_path)

        self._embedder.embedContent(
            self._interactive_list.html,
            self._settings["interactive_token"],
        )
        self._embedder.embedContent(
            self._static_list.html, self._settings["static_token"]
        )
        current_date = datetime.now().strftime("%Y%m%d")
        self._embedder.embedContent(current_date, self._settings["date_token"])

        self._embedder.saveHTML(self._settings["out_path"])

    @property
    def interactive_list(self) -> InteractiveList:
        return self._interactive_list

    @property
    def static_list(self) -> StaticList:
        return self._static_list
