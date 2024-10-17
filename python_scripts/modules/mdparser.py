"""Markdown to HTML parser module."""

from __future__ import annotations

import hashlib
import os
import re
from datetime import datetime
from typing import Any

import toml

from modules.article import Article
from modules.latex_converter import LatexMathConverter


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

    _math_rule = r"\${1,2}([^\$]+)\${1,2}"

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

    def _createElement(
        self,
        tag: str,
        content: str,
        strip_newlines: bool = False,
    ) -> str:
        if strip_newlines:
            content = content.replace("\n", " ")

        return f"<{tag}>{content.rstrip()}</{tag}>"

    def _createImage(self, url: str, alt: str) -> str:
        return f'<img src="{url}" alt="{alt}">'

    def _createLink(self, text: str, url: str) -> str:
        return f'<a href="{url}">{text}</a>'

    def _matchTitle(self, paragraph: str) -> str | None:
        for tag, rule in self._title_rules.items():
            if match := re.search(rule, paragraph):
                return self._createElement(tag, match.group(1))

        return None

    def _matchCodeBlock(self, paragraph: str) -> str | None:
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

    def _matchBlockquote(self, paragraph: str) -> str | None:
        if match := re.search(self._blockquote_rule, paragraph):
            return self._createElement("code", match.group(1))

        return None

    def _matchLink(self, paragraph: str) -> str | None:
        if match := re.search(self._link_rule, paragraph):
            paragraph = match.group(1)
            url = match.group(2)
            return self._createLink(paragraph, url)

        return None

    def _matchList(self, paragraph: str) -> str | None:
        for tag, rule in self._list_rules.items():
            if matches := re.findall(rule, paragraph, re.MULTILINE):
                items = [self._createElement("li", match) for match in matches]
                return self._createElement(tag, "\n".join(items))

        return None

    def _matchImage(self, paragraph: str, out_folder: str) -> str | None:
        if match := re.search(self._image_rule, paragraph):
            alt = match.group(1)
            url = match.group(2)

            # the image is a remote file
            if url.startswith("http"):
                return self._createImage(url, alt)

            # the image is a local file
            # copy the image to the output directory
            in_image_path = os.path.basename(url)

            out_image_path = os.path.join(
                out_folder,
                in_image_path,
            )
            os.makedirs(out_image_path, exist_ok=True)
            os.system(f"cp {in_image_path} {out_image_path}")
            # return the image tag
            return self._createImage(out_image_path, alt)

        return None

    def _matchMath(self, paragraph: str, out_folder: str) -> str | None:
        if match := re.search(self._math_rule, paragraph):
            formula = match.group(1)
            converter = LatexMathConverter()
            image_name = hashlib.sha256(formula.encode()).hexdigest() + ".png"
            image_path = os.path.join(out_folder, image_name)

            if not os.path.exists(image_path):
                converter.convert(formula, image_path)

            return self._createImage(image_name, image_name)

        return None

    def _formatParagraph(self, paragraph: str) -> str | None:
        # match spans in paragraph
        for tag, rule in self._span_rules.items():
            paragraph = re.sub(rule, "<" + tag + r">\g<1></" + tag + ">", paragraph)

        # match links in paragraph
        for match in re.finditer(self._link_rule, paragraph):
            text = match.group(1)
            url = match.group(2)
            paragraph = paragraph.replace(match.group(0), self._createLink(text, url))

        return paragraph.replace("\n", " ")

    def _parseParagraph(self, paragraph: str, out_folder: str) -> str:
        for f in [
            self._matchTitle,
            self._matchCodeBlock,
            self._matchBlockquote,
            self._matchList,
            self._matchLink,
        ]:
            if result := f(paragraph):
                return result

        for f in [
            self._matchImage,
            self._matchMath,
        ]:
            if result := f(paragraph, out_folder):
                return result

        content = self._formatParagraph(paragraph)
        return self._createElement("p", content)

    def parseFile(self, file_path: str, out_folder: str) -> Article:
        """Parse a markdown file. Return the HTML content and the options.

        Args:
            file_path (str): The path to the markdown file.
            out_folder (str): The output folder for the attachments.

        Returns:
            Article: The HTML content and the options.
        """
        with open(file_path, "r") as f:
            content = f.read()

        article = self.parseString(content, out_folder)
        if not article.date:
            created_timestamp = os.path.getctime(file_path)
            time_obj = datetime.fromtimestamp(created_timestamp)
            article.date = time_obj.strftime("%Y-%m-%d")

        return article

    def parseString(self, content: str, out_folder: str) -> Article:
        """Parse a markdown string. Return the HTML content and the options.

        Args:
            content (str): content of the markdown file.
            out_folder (str): The output folder for the attachments.

        Returns:
            Article: The HTML content and the options.
        """
        options = self._parseOptions(content)
        content = self._removeOptions(content)

        paragraphs = self._groupParagraphs(content)
        parsed_paragraphs = []

        for p in paragraphs:
            parsed = self._parseParagraph(p, out_folder)
            parsed_paragraphs.append(parsed)

        return Article(
            content="\n".join(parsed_paragraphs),
            **options,
        )
