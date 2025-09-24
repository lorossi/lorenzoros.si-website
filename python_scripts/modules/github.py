"""GitHub API wrapper and parsed Repo class."""

from __future__ import annotations

import logging
from datetime import datetime

import requests
import ujson
from typing_extensions import Any, Callable


def testCredentialsDecorator(method: Callable):
    """Credentials decorator for GitHub class methods.

    When this method is called, it will check if the credentials are still.
    If not, it will raise an exception.

    Args:
        method (callable): method of the GitHub class.
    """

    def inner(*args):
        if not args[0].testCredentials():
            raise Exception("Invalid credentials")
        return method(*args)

    return inner


class GitHub:
    """GitHub API wrapper class."""

    def __init__(self, username: str, token: str):
        """Initialize the GitHub class.

        Args:
            username (str): GitHub username.
            token (str): GitHub token.
        """
        logging.info("Initializing %s...", self.__class__.__name__)
        self._username = username
        self._token = token
        self._credentials_tested = False

    def testCredentials(self) -> bool:
        """Test the credentials.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        if self._credentials_tested:
            return True

        url = "https://api.github.com"
        r = requests.get(url, auth=(self._username, self._token))
        self._credentials_tested = r.status_code == 200
        return r.status_code == 200

    @testCredentialsDecorator
    def _getAllRepos(self, skip_private: bool) -> list[str]:
        url = f"https://api.github.com/users/{self._username}/repos"

        if skip_private:
            repos_type = "public"
        else:
            repos_type = "all"

        repos_json = []
        params = {
            "type": repos_type,
            "sort": "full_name",
            "direction": "asc",
            "per_page": 100,
            "page": 1,
        }

        while True:
            r = requests.get(url, auth=(self._username, self._token), params=params)
            if not r.json():
                return repos_json

            repos_json += r.json()
            params["page"] += 1

    @testCredentialsDecorator
    def _getRepo(
        self,
        user: str,
        name: str,
    ) -> Repo:
        url = f"https://api.github.com/repos/{user}/{name}"
        r = requests.get(url, auth=(self._username, self._token))
        json_data = r.json()

        languages = self._getRepoLanguages(json_data["languages_url"])
        commits_count = self._getRepoCommitsCount(json_data["contributors_url"])

        return Repo.from_json(
            r.json(), languages=languages, commits_count=commits_count
        )

    @testCredentialsDecorator
    def _getRepoLanguages(self, url: str) -> dict:
        r = requests.get(url, auth=(self._username, self._token))
        languages = [
            {"language": lang, "size": size} for lang, size in r.json().items()
        ]
        return sorted(languages, key=lambda x: x["size"], reverse=True)

    @testCredentialsDecorator
    def _getRepoCommitsCount(self, url: str) -> int:
        r = requests.get(url, auth=(self._username, self._token))
        user_data = list(filter(lambda x: x["login"] == self._username, r.json()))

        if not user_data:
            return 0

        return user_data[0]["contributions"]

    def getReposUrls(self, skip_private: bool = False) -> list[str]:
        """Load a list of all the repos urls.

        Args:
            skip_private (bool, optional): Skip the private repos.
                Defaults to False.

        Returns:
            list[str]
        """
        logging.info("Getting repos urls")
        urls = [repo["html_url"] for repo in self._getAllRepos(skip_private)]
        logging.info("Loaded %s repos urls", len(urls))
        return urls

    def getReposNames(self, skip_private: bool = False) -> list[str]:
        """Load a list of all the repos names.

        Args:
            skip_private (bool, optional): Skip the private repos. \
                Defaults to False.

        Returns:
            list[str]
        """
        logging.info("Getting repos names")
        names = [repo["name"] for repo in self._getAllRepos(skip_private)]
        logging.info("Loaded %s repos names", len(names))
        return names

    def getRepoByName(self, name: str) -> Repo:
        """Get a repo by its name.

        Args:
            name (str): Repo name.

        Returns:
            Repo
        """
        logging.info("Getting repo named %s", name)
        repo = self._getRepo(self._username, name)
        logging.info("Loaded repo named %s", name)
        return repo


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
    def json(self) -> dict:
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
