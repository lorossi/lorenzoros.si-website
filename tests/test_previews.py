"""Tests for the download of the repo previews."""

from pathlib import Path
from typing import Any, Self

import pytest
import requests

from modules.previews import MAX_SIZE, PreviewFetcher
from modules.repository import Repository
from modules.settings import ScraperSettings


class FakeResponse:
    def __init__(
        self, status: int = 200, content_type: str = "image/png", body: bytes = b"png"
    ) -> None:
        self.status_code = status
        self.headers = {"Content-Type": content_type}
        self._body = body

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))

    def iter_content(self, size: int) -> Any:
        for i in range(0, len(self._body), size):
            yield self._body[i : i + size]


class FakeSession:
    def __init__(self, response: FakeResponse | Exception) -> None:
        self.response = response
        self.urls: list[str] = []

    def get(self, url: str, **_: Any) -> FakeResponse:
        self.urls.append(url)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


REPO = Repository(
    name="demo", html_url="u", created_at="2026-01-01T00:00:00Z", default_branch="dev"
)


def fetcher(tmp_path: Path, response: FakeResponse | Exception, **kw: Any) -> tuple:
    session = FakeSession(response)
    settings = ScraperSettings(username="me")
    return PreviewFetcher(settings, tmp_path, session=session, **kw), session  # ty: ignore[invalid-argument-type]


def test_downloads_into_the_cache(tmp_path: Path) -> None:
    f, session = fetcher(tmp_path, FakeResponse())
    f.fetch([REPO])
    assert (tmp_path / "demo.png").read_bytes() == b"png"
    assert session.urls == [
        "https://raw.githubusercontent.com/me/demo/dev/.github/preview.png"
    ]


def test_missing_preview_clears_the_cache(tmp_path: Path) -> None:
    (tmp_path / "demo.png").write_bytes(b"old")
    f, _ = fetcher(tmp_path, FakeResponse(status=404))
    f.fetch([REPO])
    assert not (tmp_path / "demo.png").exists()


@pytest.mark.parametrize(
    "response",
    [
        requests.ConnectionError("down"),
        FakeResponse(status=500),
        FakeResponse(content_type="text/html"),
        FakeResponse(body=b"x" * (MAX_SIZE + 1)),
    ],
)
def test_failures_keep_the_cache(
    tmp_path: Path, response: FakeResponse | Exception
) -> None:
    (tmp_path / "demo.png").write_bytes(b"old")
    f, _ = fetcher(tmp_path, response)
    f.fetch([REPO])
    assert (tmp_path / "demo.png").read_bytes() == b"old"


def test_offline_touches_nothing(tmp_path: Path) -> None:
    f, session = fetcher(tmp_path, FakeResponse(), offline=True)
    f.fetch([REPO])
    assert session.urls == []


def test_copy_to_returns_only_cached(tmp_path: Path) -> None:
    (tmp_path / "cache").mkdir()
    (tmp_path / "cache" / "demo.png").write_bytes(b"png")
    f, _ = fetcher(tmp_path / "cache", FakeResponse())
    other = Repository(name="other", html_url="u", created_at="2026-01-01T00:00:00Z")
    out = tmp_path / "out"
    assert f.copy_to([REPO, other], out) == {"demo": "demo.png"}
    assert (out / "demo.png").read_bytes() == b"png"


def test_preview_path_must_be_an_image(tmp_path: Path) -> None:
    settings = ScraperSettings(username="me", preview_path="preview.svg")
    with pytest.raises(ValueError, match="preview_path"):
        PreviewFetcher(settings, tmp_path)
