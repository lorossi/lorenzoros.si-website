"""GitHub API wrapper."""

from __future__ import annotations

import logging
from http import HTTPStatus
from operator import itemgetter
from typing import Any

import requests

from modules.repository import Repository

logger = logging.getLogger(__name__)

API_URL = "https://api.github.com"


class GitHub:
    """GitHub API wrapper class."""

    def __init__(self, username: str, token: str) -> None:
        """Initialize the GitHub class.

        Args:
            username (str): GitHub username.
            token (str): GitHub token.
        """
        self._username = username
        self._session = requests.Session()
        self._session.headers["Accept"] = "application/vnd.github+json"
        if token:
            self._session.headers["Authorization"] = f"Bearer {token}"
        self._requests_count = 0

    def _get(self, url: str, params: dict | None = None) -> Any:
        """Make a GET request to the GitHub API and return the decoded JSON.

        Args:
            url (str): URL to make the request to.
            params (dict | None, optional): Query parameters. Defaults to None.

        Returns:
            Any: decoded JSON response.

        Raises:
            requests.HTTPError: if the request fails.
        """
        response = self._session.get(url, params=params, timeout=30)
        self._requests_count += 1
        if not response.ok:
            raise requests.HTTPError(
                f"GitHub API request to {url} failed: "
                f"HTTP {response.status_code} - {response.text}",
                response=response,
            )
        return response.json()

    def _get_all_repos(self, *, skip_private: bool) -> list[dict]:
        url = f"{API_URL}/users/{self._username}/repos"
        params = {
            "type": "public" if skip_private else "all",
            "sort": "full_name",
            "direction": "asc",
            "per_page": 100,
            "page": 1,
        }

        repos_json = []
        while page := self._get(url, params=params):
            repos_json += page
            params["page"] += 1
        return repos_json

    def _get_repo_languages(self, url: str) -> list[dict[str, Any]]:
        languages = [
            {"language": lang, "size": size} for lang, size in self._get(url).items()
        ]
        return sorted(languages, key=itemgetter("size"), reverse=True)

    def _get_repo_commits_count(self, url: str) -> int:
        # an empty repository returns 204 No Content
        response = self._session.get(url, timeout=30)
        self._requests_count += 1
        if response.status_code == HTTPStatus.NO_CONTENT:
            return 0
        response.raise_for_status()

        for contributor in response.json():
            if contributor["login"] == self._username:
                return contributor["contributions"]
        return 0

    def get_repos(self, *, skip_private: bool = True) -> list[Repository]:
        """Load all the repositories of the user, with languages and commits.

        Args:
            skip_private (bool, optional): Skip the private repos.
                Defaults to True.

        Returns:
            list[Repository]
        """
        logger.info("Getting repos of %s", self._username)
        repos = []
        for repo_json in self._get_all_repos(skip_private=skip_private):
            logger.info("Loading repo %s", repo_json["name"])
            r = Repository.from_dict(
                repo_json,
                languages=self._get_repo_languages(repo_json["languages_url"]),
                commits_count=self._get_repo_commits_count(
                    repo_json["contributors_url"]
                ),
            )
            repos.append(r)

        logger.info("Loaded %d repos", len(repos))
        return repos

    @property
    def requests_count(self) -> int:
        """Number of requests made to the GitHub API."""
        return self._requests_count
