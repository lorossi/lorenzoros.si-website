"""This module contains the Article class, a blog post written in Markdown."""

from __future__ import annotations

import datetime
import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt

logger = logging.getLogger(__name__)

FRONT_MATTER_DELIMITER = "+++"
FRONT_MATTER_TYPES = {
    "title": str,
    "date": datetime.date,
    "description": str,
    "draft": bool,
}

# CommonMark, plus tables and strikethrough; raw HTML is allowed since the
# articles are written by me
MARKDOWN = MarkdownIt("commonmark", {"typographer": True}).enable(
    ["table", "strikethrough", "replacements", "smartquotes"]
)


@dataclass(frozen=True)
class Article:
    """A blog article, parsed from a Markdown file with TOML front matter.

    The file looks like:

        +++
        title = "My article"
        date = 2026-10-26
        description = "Optional, shown in the list and in the meta tags"
        draft = false
        +++

        The content, in Markdown.
    """

    slug: str
    title: str
    date: datetime.date
    content: str
    description: str = ""
    draft: bool = False

    @classmethod
    def from_file(cls, path: Path) -> Article:
        """Parse an article from a Markdown file.

        The slug (used in the url) is the file name without extension.

        Args:
            path (Path): the Markdown file.

        Returns:
            Article: the parsed article, with the content rendered to HTML.

        Raises:
            ValueError: if the front matter is missing or invalid.
        """
        text = path.read_text(encoding="utf-8")
        opening, _, rest = text.partition("\n")
        front_matter, delimiter, body = rest.partition(f"\n{FRONT_MATTER_DELIMITER}\n")
        if opening.strip() != FRONT_MATTER_DELIMITER or not delimiter:
            raise ValueError(
                f"{path}: the article must start with a front matter "
                f"enclosed by {FRONT_MATTER_DELIMITER} lines"
            )

        try:
            meta = tomllib.loads(front_matter)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"{path}: invalid front matter: {e}") from e

        unknown = set(meta) - set(FRONT_MATTER_TYPES)
        if unknown:
            raise ValueError(f"{path}: unknown front matter keys {sorted(unknown)}")
        missing = {"title", "date"} - set(meta)
        if missing:
            raise ValueError(f"{path}: missing front matter keys {sorted(missing)}")
        # `type` instead of `isinstance`, since a datetime is also a date
        wrong = [k for k, v in meta.items() if type(v) is not FRONT_MATTER_TYPES[k]]
        if wrong:
            raise ValueError(
                f"{path}: wrong type for front matter keys {sorted(wrong)} "
                "(title and description are strings, date is YYYY-MM-DD, "
                "draft is true or false)"
            )

        return cls(slug=path.stem, content=MARKDOWN.render(body), **meta)

    @property
    def url(self) -> str:
        """Absolute path of the article on the website."""
        return f"/blog/{self.slug}/"

    @property
    def date_formatted(self) -> str:
        """Publication date, formatted as YYYY-MM-DD."""
        return self.date.isoformat()


def load_articles(path: Path, *, include_drafts: bool = False) -> list[Article]:
    """Load all the articles in a folder, newest first.

    Args:
        path (Path): folder containing the Markdown files.
        include_drafts (bool, optional): if True, drafts are loaded too.
            Defaults to False.

    Returns:
        list[Article]: the articles, newest first.
    """
    articles = []
    for file in sorted(path.glob("*.md")):
        article = Article.from_file(file)
        if article.draft and not include_drafts:
            logger.info("Skipping draft %s", file.name)
            continue
        articles.append(article)

    logger.info("Loaded %d articles", len(articles))
    return sorted(articles, key=lambda a: (a.date, a.slug), reverse=True)
