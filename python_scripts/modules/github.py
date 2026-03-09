"""GitHub API wrapper and parsed Repo class."""

from __future__ import annotations

import logging
from typing import Any, Callable

import requests

from modules.repository import Repository


def check_credentials_decorator(method: Callable) -> Callable:
    """Credentials decorator for GitHub class methods.

    When this method is called, it will check if the credentials are still valid.
    If not, it will raise an exception.

    Args:
        method (callable): method of the GitHub class.
    """

    def inner(*args) -> Any:
        if not args[0].test_credentials():
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
        self._requests_count = 0

    def _make_authorized_request(
        self, url: str, params: dict | None = None
    ) -> requests.Response:
        """Make an authorized request to the GitHub API.

        Args:
            url (str): URL to make the request to.
            params (dict | None, optional): Query parameters. Defaults to None.

        Returns:
            requests.Response: Response object.
        """
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logging.warning(
                "GitHub API request failed: HTTP %d - %s",
                response.status_code,
                response.text,
            )
        self._requests_count += 1
        return response

    def test_credentials(self) -> bool:
        """Test the credentials.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        if self._credentials_tested:
            return True

        r = self._make_authorized_request("https://api.github.com")
        self._credentials_tested = r.status_code == 200
        return r.status_code == 200

    @check_credentials_decorator
    def _get_all_repos(self, skip_private: bool) -> list[dict]:
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
            r = self._make_authorized_request(url, params=params)
            if not r.json():
                return repos_json

            repos_json += r.json()
            params["page"] += 1

    @check_credentials_decorator
    def _get_repo(
        self,
        user: str,
        name: str,
    ) -> Repository:
        url = f"https://api.github.com/repos/{user}/{name}"
        r = self._make_authorized_request(url)
        json_data = r.json()

        languages = self._get_repo_languages(json_data["languages_url"])
        commits_count = self._get_repo_commits_count(json_data["contributors_url"])

        return Repository.from_json(
            r.json(), languages=languages, commits_count=commits_count
        )

    @check_credentials_decorator
    def _get_repo_languages(self, url: str) -> list[dict[str, float]]:
        r = self._make_authorized_request(url)
        languages = [
            {"language": lang, "size": size} for lang, size in r.json().items()
        ]
        return sorted(languages, key=lambda x: x["size"], reverse=True)

    @check_credentials_decorator
    def _get_repo_commits_count(self, url: str) -> int:
        r = self._make_authorized_request(url)
        json_data = r.json()

        user_data = list(filter(lambda x: x["login"] == self._username, json_data))

        if not user_data:
            return 0

        return user_data[0]["contributions"]

    def get_repos_urls(self, skip_private: bool = False) -> list[str]:
        """Load a list of all the repos urls.

        Args:
            skip_private (bool, optional): Skip the private repos.
                Defaults to False.

        Returns:
            list[str]
        """
        logging.info("Getting repos urls")
        urls = [repo["html_url"] for repo in self._get_all_repos(skip_private)]
        logging.info("Loaded %s repos urls", len(urls))
        return urls

    def get_repos_names(self, skip_private: bool = False) -> list[str]:
        """Load a list of all the repos names.

        Args:
            skip_private (bool, optional): Skip the private repos.
                Defaults to False.

        Returns:
            list[str]
        """
        logging.info("Getting repos names")
        names = [repo["name"] for repo in self._get_all_repos(skip_private)]
        logging.info("Loaded %s repos names", len(names))
        return names

    def get_repo_by_name(self, name: str) -> Repository:
        """Get a repo by its name.

        Args:
            name (str): Repo name.

        Returns:
            Repo
        """
        logging.info("Getting repo named %s", name)
        repo = self._get_repo(self._username, name)
        logging.info("Loaded repo named %s", name)
        return repo

    @property
    def requests_count(self) -> int:
        """Return the number of requests made to the GitHub API.

        Returns:
            int
        """
        return self._requests_count
