"""Download the preview images of the interactive repositories."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from urllib.parse import quote

import requests

from modules.repository import Repository
from modules.settings import ScraperSettings

logger = logging.getLogger(__name__)

RAW_URL = "https://raw.githubusercontent.com"
ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}
MAX_SIZE = 2 * 1024 * 1024  # bytes
CHUNK_SIZE = 64 * 1024  # bytes


class PreviewFetcher:
    """Downloads the preview of the repos into a cache folder.

    The preview is the file at a fixed path (`preview_path` setting) in the
    default branch of the repository. Repos without it simply have no preview.
    The cache lets offline builds keep the previews.
    """

    def __init__(
        self,
        settings: ScraperSettings,
        cache_path: Path,
        *,
        offline: bool = False,
        session: requests.Session | None = None,
    ) -> None:
        """Create a new PreviewFetcher instance.

        Args:
            settings (ScraperSettings): scraper settings.
            cache_path (Path): folder to download the previews to.
            offline (bool, optional): if True, nothing is downloaded and
                `fetch` does nothing. Defaults to False.
            session (requests.Session | None, optional): HTTP session. If None,
                a new one is created. Defaults to None.

        Raises:
            ValueError: if `preview_path` is not a raster image.
        """
        self._username = settings.username
        self._preview_path = settings.preview_path
        self._suffix = Path(self._preview_path).suffix.lower()
        if self._suffix not in ALLOWED_SUFFIXES:
            raise ValueError(
                f"preview_path must end with one of {sorted(ALLOWED_SUFFIXES)}, "
                f"got {self._preview_path!r}"
            )
        self._cache_path = cache_path
        self._offline = offline
        self._session = session or requests.Session()

    def filename(self, repo: Repository) -> str:
        """Return the name of the cached preview file of a repo.

        Args:
            repo (Repository): the repository.

        Returns:
            str: file name, e.g. `my-repo.png`.
        """
        return f"{repo.name}{self._suffix}"

    def cached(self, repos: list[Repository]) -> dict[str, Path]:
        """Find the previews that are in the cache.

        Args:
            repos (list[Repository]): repos to look for.

        Returns:
            dict[str, Path]: path of the preview, by repo name.
        """
        found = {}
        for repo in repos:
            path = self._cache_path / self.filename(repo)
            if path.is_file():
                found[repo.name] = path
        return found

    def fetch(self, repos: list[Repository]) -> None:
        """Update the cache with the current previews of the repos.

        A repo that no longer has a preview loses its cached one. A network
        failure keeps what is cached and does not stop the build. Offline,
        nothing is touched.

        Args:
            repos (list[Repository]): repos to download the previews of.
        """
        if self._offline:
            return

        self._cache_path.mkdir(parents=True, exist_ok=True)
        for repo in repos:
            path = self._cache_path / self.filename(repo)
            try:
                content = self._download(repo)
            except (requests.RequestException, ValueError) as e:
                logger.warning("Preview of %s not updated: %s", repo.name, e)
                continue

            if content is None:
                logger.info("%s has no preview (%s)", repo.name, self._preview_path)
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(content)
                logger.info("Downloaded the preview of %s", repo.name)

    def copy_to(self, repos: list[Repository], output: Path) -> dict[str, str]:
        """Copy the cached previews of the repos to the output folder.

        Args:
            repos (list[Repository]): repos to copy the previews of.
            output (Path): destination folder.

        Returns:
            dict[str, str]: file name in `output`, by repo name.
        """
        cached = self.cached(repos)
        if cached:
            output.mkdir(parents=True, exist_ok=True)
        for path in cached.values():
            shutil.copy2(path, output / path.name)
        return {name: path.name for name, path in cached.items()}

    def _download(self, repo: Repository) -> bytes | None:
        """Download the preview of a repo.

        Args:
            repo (Repository): the repository.

        Returns:
            bytes | None: the image, or None if the repo has no preview.

        Raises:
            ValueError: if the file is not an image or is too big.
        """
        url = (
            f"{RAW_URL}/{quote(self._username)}/{quote(repo.name)}/"
            f"{quote(repo.default_branch)}/{quote(self._preview_path)}"
        )
        with self._session.get(url, stream=True, timeout=30) as response:
            if response.status_code == requests.codes.not_found:
                return None
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                raise ValueError(f"{url} is not an image ({content_type!r})")

            content = bytearray()
            for chunk in response.iter_content(CHUNK_SIZE):
                content += chunk
                if len(content) > MAX_SIZE:
                    raise ValueError(f"{url} is bigger than {MAX_SIZE} bytes")
        return bytes(content)
