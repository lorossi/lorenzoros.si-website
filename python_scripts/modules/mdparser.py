"""Markdown to HTML parser module."""
from __future__ import annotations

import re
from typing import Any
from .article import Article

import toml


class ParserError(Exception):
    """Parser error class."""

    def __init__(self, *args: object) -> None:
        """Create a new ParserError instance."""
        super().__init__(*args)


class MarkdownParser:
    """Markdown parser class."""

    _title_rules = {
        "h1": r"^#\s*([^#]*)$",
        "h2": r"^##\s*([^#]*)$",
        "h3": r"^###\s*([^#]*)$",
        "h4": r"^####\s*([^#]*)$",
        "h5": r"^#####\s*([^#]*)$",
        "h6": r"^######\s*([^#]*)$",
    }

    _span_rules = {
        "bold": r"\*\*([^*]+)\*\*",
        "italic": r"\*([^*]+)\*",
        "underline": r"__([^_]+)__",
        "strikethrough": r"~~([^~]+)~~",
        "code": r"`([^`]+)`",
    }

    _list_rules = {
        "ul": r"^\s*-\s*([^-]*)$",
        "ol": r"^\s*\d+\.\s*(.*)$",
    }

    _link_rule = r"\[([^\]]*)\]\(([^\)]*)\)"
    _blockquote_rule = r"^>\s*(.*)$"
    _codeblock_rule = r"```([^\n]*)\n((.*\n)+)```"
    _image_rule = r"!\[([^\]]*)\]\(([^\)]*)\)"
    _options_rule = r"---\n((.*\n)+)---"

    def _parseOptions(self, content: str) -> dict[str, Any]:
        """Parse options in the markdown file.

        Args:
            content (str): The markdown content. Options are passed as {key = value} \
                pairs in the first section of the file, between `---` characters, \
                in TOML format.

        Returns:
            dict[str, Any]: The options as a dictionary.
        """
        options_section = re.search(self._options_rule, content)
        if options_section:
            return toml.loads(options_section.group(1))
        return {}

    def _removeOptions(self, content: str) -> str:
        """Remove the options section from the markdown content."""
        return re.sub(self._options_rule, "", content)

    def _groupParagraphs(self, content: str) -> list[str]:
        """Group lines into paragraphs.

        Args:
            content (str): The markdown content.

        Returns:
            list[str]: The paragraphs.
        """
        paragraphs = []
        code_block_started = False
        current = ""
        for line in content.splitlines():
            if line or code_block_started:
                if line.startswith("```"):
                    code_block_started = not code_block_started
                current += f"{line}\n"
            else:
                paragraphs.append(current.rstrip())
                current = ""

        if current:
            paragraphs.append(current)

        return paragraphs

    def _createElement(self, tag: str, content: str, strip_newlines=False) -> str:
        if strip_newlines:
            content = content.replace("\n", " ")

        return f"<{tag}>{content.rstrip()}</{tag}>"

    def _createImage(self, url: str, alt: str) -> str:
        return f'<img src="{url}" alt="{alt}">'

    def _createLink(self, text: str, url: str) -> str:
        return f'<a href="{url}">{text}</a>'

    def _matchTitle(self, title: str) -> str:
        for tag, rule in self._title_rules.items():
            if match := re.search(rule, title):
                return self._createElement(tag, match.group(1))

        return None

    def _matchCodeBlock(self, paragraph: str) -> str:
        expression = self._codeblock_rule
        if match := re.search(expression, paragraph, re.MULTILINE):
            language = match.group(1)
            content = match.group(2)

            if language:
                return self._createElement(
                    "code", f'<pre language="{language}">\n{content}</pre>'
                )
            else:
                return self._createElement("code", content=content, strip_newlines=True)

        return None

    def _matchBlockquote(self, paragraph: str) -> str:
        if match := re.search(self._blockquote_rule, paragraph):
            return self._createElement("code", match.group(1))

        return None

    def _matchImage(self, paragraph: str) -> str:
        if match := re.search(self._image_rule, paragraph):
            alt = match.group(1)
            url = match.group(2)
            return self._createImage(url, alt)

        return None

    def _matchLink(self, paragraph: str) -> str:
        if match := re.search(self._link_rule, paragraph):
            paragraph = match.group(1)
            url = match.group(2)
            return self._createLink(paragraph, url)

        return None

    def _matchList(self, paragraph: str) -> str:
        for tag, rule in self._list_rules.items():
            if matches := re.findall(rule, paragraph, re.MULTILINE):
                items = [self._createElement("li", match) for match in matches]
                return self._createElement(tag, "\n".join(items))

        return None

    def _formatParagraph(self, paragraph: str) -> str:
        # match spans in paragraph
        for tag, rule in self._span_rules.items():
            paragraph = re.sub(rule, "<" + tag + r">\g<1></" + tag + ">", paragraph)

        # match links in paragraph
        for match in re.finditer(self._link_rule, paragraph):
            text = match.group(1)
            url = match.group(2)
            paragraph = paragraph.replace(match.group(0), self._createLink(text, url))

        return paragraph.replace("\n", " ")

    def _parseParagraph(self, paragraph: str) -> str:
        for function in [
            self._matchTitle,
            self._matchCodeBlock,
            self._matchImage,
            self._matchList,
            self._matchBlockquote,
        ]:
            if result := function(paragraph):
                return result

        content = self._formatParagraph(paragraph)
        return self._createElement("p", content)

    def parseFile(self, file_path: str) -> Article:
        """Parse a markdown file. Return the HTML content and the options.

        Args:
            file_path (str): The path to the markdown file.

        Returns:
            Article: The HTML content and the options.
        """
        with open(file_path, "r") as f:
            content = f.read()

        return self.parseString(content)

    def parseString(self, content: str) -> Article:
        """Parse a markdown string. Return the HTML content and the options.

        Args:
            content (str): content of the markdown file.

        Returns:
            Article: The HTML content and the options.
        """
        options = self._parseOptions(content)
        content = self._removeOptions(content)

        paragraphs = self._groupParagraphs(content)
        ...
        content = "\n".join(
            [self._parseParagraph(paragraph) for paragraph in paragraphs if paragraph]
        )

        return Article(content=content, **options)
