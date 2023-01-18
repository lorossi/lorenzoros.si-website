from __future__ import annotations

import logging

import toml

from .github import Repo


class DOMelement:
    def __init__(self, **kwargs):
        self._element = kwargs["element"]
        self._content = kwargs.get("content", "")
        self._children = kwargs.get("children", [])
        self._attributes = kwargs.get("attributes", [])

    def _formatHTMLAttributes(self) -> str:
        attributes = ""
        for k, v in self._attributes.items():
            if isinstance(v, list):
                plain_values = " ".join(v)
            else:
                plain_values = v
            attributes += f'{k}="{plain_values}"'

        return attributes

    def __str__(self) -> str:
        return (
            f"<{self._element} {self._formatHTMLAttributes()}>"
            f"{self._content}"
            f"{''.join([str(child) for child in self._children])}"
            f"</{self._element}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class HTMLList:
    _settings: dict
    _list: list[DOMelement]

    def _loadSettings(self, path: str) -> None:
        logging.info(f"Loading settings from {path}")
        with open(path, "r") as f:
            self._settings = toml.load(f)[self.__class__.__name__]
        logging.info("Loaded settings")

    def __init__(self, repos: list[Repo], settings_path: str = "settings.toml"):
        logging.info(f"Initializing {self.__class__.__name__}...")
        self._repos = repos
        self._loadSettings(settings_path)

    def __repr__(self) -> str:
        return str(self._list)

    def __str__(self) -> str:
        return self.__repr__()

    def saveHTML(self, base_path: str = "") -> None:
        full_path = base_path + self.filename
        logging.info(f"Saving HTML to {full_path} for {self.__class__.__name__}")
        with open(full_path, "w") as f:
            f.write(self.html)
        logging.info("Saved HTML")

    @property
    def html(self) -> str:
        return str(self._list)

    @property
    def filename(self) -> str:
        return self._settings["filename"]


class DOMElementFactory:
    @staticmethod
    def createElement(element: str, **kwargs) -> DOMelement:
        match element:
            case "div":
                return DOMelement(
                    element="div",
                    content=kwargs.get("content"),
                    children=kwargs.get("children", []),
                    attributes={"class": kwargs["classlist"]},
                )
            case "a":
                return DOMelement(
                    element="a",
                    content=kwargs.get("content"),
                    attributes={"href": kwargs["href"], "class": kwargs["classlist"]},
                )
            case "span":
                return DOMelement(
                    element="span",
                    content=kwargs.get("content"),
                    attributes={"class": kwargs["classlist"]},
                )
            case "li":
                return DOMelement(
                    element="li",
                    content=kwargs.get("content"),
                    children=kwargs.get("children"),
                    attributes={"class": kwargs["classlist"]},
                )
            case "ul":
                return DOMelement(
                    element="ul",
                    content=kwargs.get("content"),
                    children=kwargs.get("children"),
                    attributes={"class": kwargs["classlist"]},
                )


class InteractiveList(HTMLList):
    def __init__(self, repos: list[Repo], settings_path: str = "settings.toml"):
        super().__init__(repos, settings_path)
        self._list = self._createUnorderedList()

    def _createLinks(self) -> list[DOMelement]:
        a_list = [
            DOMElementFactory.createElement(
                element="a",
                content=repo.name_formatted,
                href=repo.homepage,
                classlist=self._settings["a_classlist"],
            )
            for repo in self._repos
        ]
        span_list = [
            DOMElementFactory.createElement(
                element="span",
                content=f"created: {repo.created_at_formatted}",
                classlist=self._settings["span_classlist"],
            )
            for repo in self._repos
        ]

        return [(a, span) for a, span in zip(a_list, span_list)]

    def _createListItems(self) -> list[DOMelement]:
        return [
            DOMElementFactory.createElement(
                element="li",
                content="",
                children=link,
                classlist=self._settings["li_classlist"],
            )
            for link in self._createLinks()
        ]

    def _createUnorderedList(self) -> list[DOMelement]:
        return DOMElementFactory.createElement(
            element="ul",
            content="",
            children=self._createListItems(),
            classlist=self._settings["ul_classlist"],
        )


class StaticList(HTMLList):
    def __init__(self, repos: list[Repo], settings_path: str = "settings.toml"):
        super().__init__(repos, settings_path)
        self._list = self._createDivs()

    def _createLinks(self, repo: Repo) -> tuple[DOMelement]:
        a = DOMElementFactory.createElement(
            element="a",
            content=repo.name_formatted,
            href=repo.html_url,
            classlist=self._settings["a_classlist"],
        )

        span = DOMElementFactory.createElement(
            element="span",
            content=repo.description_formatted,
            classlist=self._settings["span_classlist"],
        )

        return (a, span)

    def _createListItems(self, language: str) -> list[DOMelement]:
        return [
            DOMElementFactory.createElement(
                element="li",
                content="",
                children=self._createLinks(repo),
                classlist=self._settings["li_classlist"],
            )
            for repo in [repo for repo in self._repos if repo.language == language]
        ]

    def _createUnorderedList(self, language) -> list[DOMelement]:
        return [
            DOMElementFactory.createElement(
                element="ul",
                content="",
                children=self._createListItems(language),
                classlist=self._settings["ul_classlist"],
            )
        ]

    def _createDivs(self) -> list[DOMelement]:
        return [
            DOMElementFactory.createElement(
                element="div",
                content=language,
                children=self._createUnorderedList(language),
                classlist=self._settings["div_classlist"],
            )
            for language in sorted(list(set([repo.language for repo in self._repos])))
        ]

    def __str__(self) -> str:
        return "\n".join([str(element) for element in self._list])
