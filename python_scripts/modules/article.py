from .container import Container
import re
from datetime import datetime


class Article(Container):
    content: str

    def __init__(self, content: str, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    @property
    def title(self):
        if title := self.get("title"):
            return title

        html_title = re.search(r"<h1>([^<]+)</h1>", self.content)
        if html_title:
            return html_title.group(1)

        return ""

    @property
    def link(self):
        if link := self.get("link"):
            return link

        return self.title.lower().replace(" ", "-") + ".html"

    @property
    def category(self):
        if category := self.get("category"):
            return category

        return ""

    @property
    def date(self):
        if date := self.get("date"):
            return date

        return ""

    @property
    def language(self):
        if language := self.get("language"):
            return language

        return "english"

    @property
    def overwrite(self):
        if overwrite := self.get("overwrite"):
            return overwrite

        return False

    @property
    def date_obj(self) -> datetime:
        if date := self.get("date"):
            return datetime.strptime(date, "%Y-%m-%d")

        return datetime.now()
