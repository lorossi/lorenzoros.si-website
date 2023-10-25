"""This module contains the Article class."""
from __future__ import annotations

import re
from datetime import datetime

from modules.container import Container


class Article(Container):
    """This class represents an article."""

    content: str

    def __init__(self, content: str, **kwargs) -> Article:
        """Create a new Article instance."""
        super().__init__(**kwargs)
        self.content = content

    @property
    def title(self) -> str:
        """Return the title of the article.

        Returns:
            str
        """
        if title := self.get("title"):
            return title

        html_title = re.search(r"<h1>([^<]+)</h1>", self.content)
        if html_title:
            return html_title.group(1)

        return ""

    @property
    def link(self) -> str:
        """Return the link of the article.

        Returns:
            str
        """
        if link := self.get("link"):
            return link

        return self.title.lower().replace(" ", "-") + ".html"

    @property
    def category(self) -> str:
        """Return the category of the article.

        Returns:
            str
        """
        return self.get("category", "")

    @property
    def date(self) -> str:
        """Return the date of the article.

        Returns:
            str
        """
        return self.get("date", "")

    @property
    def language(self) -> str:
        """Return the language of the article.

        Returns:
            str
        """
        return self.get("language", "english")

    @property
    def overwrite(self) -> bool:
        """Return the overwrite flag of the article.

        Returns:
            bool
        """
        return self.get("overwrite", False)

    @property
    def date_obj(self) -> datetime:
        """Return the date of the article as a datetime object.

        Returns:
            datetime
        """
        if date := self.get("date"):
            return datetime.strptime(date, "%Y-%m-%d")

        return datetime.now()
