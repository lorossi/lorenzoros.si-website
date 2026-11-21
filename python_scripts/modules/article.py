"""This module contains the Article class, a blog post written in Markdown."""

from __future__ import annotations

import datetime
import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from latex2mathml.converter import convert as latex_to_mathml
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block import StateBlock
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict
from mdit_py_plugins.dollarmath import dollarmath_plugin

logger = logging.getLogger(__name__)

FRONT_MATTER_DELIMITER = "+++"
FRONT_MATTER_TYPES = {
    "title": str,
    "date": datetime.date,
    "description": str,
    "draft": bool,
    "tags": list,
}


def _is_figure(tokens: list[Token], idx: int) -> bool:
    """Check if a paragraph_open/paragraph_close token wraps a lone image.

    Args:
        tokens (list[Token]): the block tokens.
        idx (int): index of the paragraph token.

    Returns:
        bool: True if the paragraph contains nothing but an image.
    """
    inline = tokens[idx + 1] if tokens[idx].nesting == 1 else tokens[idx - 1]
    return (
        inline.type == "inline"
        and len(inline.children or []) == 1
        and (inline.children or [])[0].type == "image"
    )


def _render_paragraph(
    self: RendererHTML,
    tokens: list[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render a paragraph, without the <p> if it only contains an image.

    Args:
        self (RendererHTML): the renderer.
        tokens (list[Token]): the block tokens.
        idx (int): index of the paragraph token.
        options (OptionsDict): the markdown-it options.
        env (EnvType): the markdown-it environment.

    Returns:
        str: the HTML.
    """
    if _is_figure(tokens, idx):
        return ""
    return self.renderToken(tokens, idx, options, env)


def _render_image(
    self: RendererHTML,
    tokens: list[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Render an image; if alone in its paragraph, the alt text is its caption.

    Args:
        self (RendererHTML): the renderer.
        tokens (list[Token]): the inline tokens of the paragraph.
        idx (int): index of the image token.
        options (OptionsDict): the markdown-it options.
        env (EnvType): the markdown-it environment.

    Returns:
        str: the HTML.
    """
    token = tokens[idx]
    token.attrSet("alt", self.renderInlineAsText(token.children, options, env))
    img = self.renderToken(tokens, idx, options, env)
    if len(tokens) != 1:  # inline image in a sentence: leave it as is
        return img
    caption = self.renderInline(token.children or [], options, env)
    return f"<figure>{img}<figcaption>{caption}</figcaption></figure>\n"


def _math(latex: str, *, display: bool) -> str:
    """Render LaTeX to MathML (browsers draw it natively, no JavaScript needed).

    Args:
        latex (str): the formula.
        display (bool): True for a block formula, False for an inline one.

    Returns:
        str: the MathML.
    """
    return latex_to_mathml(latex, display="block" if display else "inline")


def _bracket_math_inline(state: StateInline, silent: bool) -> bool:  # ruff: ignore[boolean-type-hint-positional-argument]
    r"""Parse \(inline\) and \[display\] math inside a paragraph.

    It runs before the escape rule, that would otherwise turn \( into (. The
    tokens are the ones of dollarmath, so they are rendered by the same rules.

    Args:
        state (StateInline): the inline parser state.
        silent (bool): if True, only check for a match without adding tokens.

    Returns:
        bool: True if math was found.
    """
    opener = state.src[state.pos : state.pos + 2]
    if opener not in {"\\(", "\\["}:
        return False
    closer = "\\)" if opener == "\\(" else "\\]"
    end = state.src.find(closer, state.pos + 2)
    if end == -1:
        return False
    if not silent:
        kind = "math_inline" if opener == "\\(" else "math_inline_double"
        token = state.push(kind, "math", 0)
        token.content = state.src[state.pos + 2 : end]
        token.markup = opener
    state.pos = end + 2
    return True


def _bracket_math_block(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,  # ruff: ignore[boolean-type-hint-positional-argument]
) -> bool:
    r"""Parse a \[display\] math block, starting at the beginning of a line.

    The block ends on the first line ending with \]; it cannot contain blank
    lines, like a paragraph.

    Args:
        state (StateBlock): the block parser state.
        start_line (int): the first line of the block.
        end_line (int): the last line of the document.
        silent (bool): if True, only check for a match without adding tokens.

    Returns:
        bool: True if a math block was found.
    """
    if state.is_code_block(start_line):
        return False
    start = state.bMarks[start_line] + state.tShift[start_line]
    if not state.src.startswith("\\[", start):
        return False

    line, content = start_line, ""
    begin = start + 2
    while line < end_line:
        text = state.src[begin : state.eMarks[line]].rstrip()
        if line > start_line and not text.strip():  # blank line: not math
            return False
        if text.endswith("\\]"):
            content += text[:-2]
            break
        content += text + "\n"
        line += 1
        begin = state.bMarks[line] + state.tShift[line] if line < end_line else 0
    else:
        return False

    if not silent:
        token = state.push("math_block", "math", 0)
        token.block = True
        token.content = content
        token.markup = "\\["
        token.map = [start_line, line + 1]
    state.line = line + 1
    return True


# CommonMark, plus tables, strikethrough and $math$ or \(math\) (pre-rendered to
# MathML); raw HTML is allowed since the articles are written by me
MARKDOWN = (
    MarkdownIt("commonmark", {"typographer": True})
    .enable(["table", "strikethrough", "replacements", "smartquotes"])
    .use(
        dollarmath_plugin,
        double_inline=True,
        renderer=lambda content, opts: _math(
            content, display=bool(opts.get("display_mode"))
        ),
    )
)
MARKDOWN.inline.ruler.before("escape", "math_brackets", _bracket_math_inline)
MARKDOWN.block.ruler.before(
    "fence",
    "math_block_brackets",
    _bracket_math_block,
    {"alt": ["paragraph", "reference", "blockquote", "list"]},
)
MARKDOWN.add_render_rule("paragraph_open", _render_paragraph)
MARKDOWN.add_render_rule("paragraph_close", _render_paragraph)
MARKDOWN.add_render_rule("image", _render_image)


@dataclass(frozen=True)
class Article:
    """A blog article, parsed from a Markdown file with TOML front matter.

    The file looks like:

        +++
        title = "My article"
        date = 2026-10-26
        description = "Optional, shown in the list and in the meta tags"
        tags = ["physics", "c"]  # optional, the topics the article is about
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
    tags: tuple[str, ...] = ()

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
                "draft is true or false, tags is a list of strings)"
            )
        tags = meta.pop("tags", [])
        if not all(isinstance(t, str) and t.strip() for t in tags):
            raise ValueError(f"{path}: tags must be a list of non-empty strings")
        # each tag gets its own folder, /blog/tag/<tag>/
        if any("/" in t or t.strip() in {".", ".."} for t in tags):
            raise ValueError(f'{path}: tags cannot contain "/" or be "." or ".."')
        meta["tags"] = tuple(dict.fromkeys(t.strip().lower() for t in tags))

        return cls(slug=path.stem, content=MARKDOWN.render(body), **meta)

    @property
    def url(self) -> str:
        """Absolute path of the article on the website."""
        return f"/blog/{self.slug}/"

    @property
    def date_formatted(self) -> str:
        """Publication date, formatted as YYYY-MM-DD."""
        return self.date.isoformat()

    @property
    def date_short(self) -> str:
        """Publication day, formatted as MM-DD (the year is shown elsewhere)."""
        return self.date.strftime("%m-%d")

    @property
    def date_long(self) -> str:
        """Publication date, formatted as e.g. "October 26, 2026"."""
        return f"{self.date:%B} {self.date.day}, {self.date.year}"


def tag_url(tag: str) -> str:
    """Absolute path of the blog index filtered by a tag.

    Args:
        tag (str): the tag.

    Returns:
        str: the url, with the tag percent-encoded.
    """
    return f"/blog/tag/{quote(tag, safe='')}/"


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


def group_by_tag(articles: list[Article]) -> dict[str, list[Article]]:
    """Group articles by tag, for the tag filter of the blog index.

    An article with several tags appears in each of them; untagged articles
    appear in none.

    Args:
        articles (list[Article]): the articles, newest first.

    Returns:
        dict[str, list[Article]]: the articles of each tag (newest first),
            most used tags first, then in alphabetical order.
    """
    groups: dict[str, list[Article]] = {}
    for article in articles:
        for tag in article.tags:
            groups.setdefault(tag, []).append(article)
    return dict(sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])))


def group_by_year(articles: list[Article]) -> dict[int, list[Article]]:
    """Group articles by publication year, for the blog index.

    Args:
        articles (list[Article]): the articles, newest first.

    Returns:
        dict[int, list[Article]]: the articles of each year, newest first.
    """
    groups: dict[int, list[Article]] = {}
    for article in articles:
        groups.setdefault(article.date.year, []).append(article)
    return dict(sorted(groups.items(), reverse=True))
