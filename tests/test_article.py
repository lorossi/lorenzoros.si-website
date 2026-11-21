"""Tests for the Markdown articles."""

import datetime
from pathlib import Path

import pytest

from modules.article import (
    Article,
    group_by_tag,
    group_by_year,
    load_articles,
    tag_url,
)

VALID = """+++
title = "Hello"
date = 2026-10-26
description = "A description"
tags = ["Physics", "c", "physics"]
+++

Some *text*.
"""


def write(path: Path, name: str, text: str) -> Path:
    """Write an article and return its path."""
    file = path / name
    file.write_text(text, encoding="utf-8")
    return file


def make(path: Path, name: str = "a.md", **meta: str) -> Path:
    """Write an article with the given front matter lines."""
    lines = {"title": '"T"', "date": "2026-01-01", **meta}
    front = "\n".join(f"{k} = {v}" for k, v in lines.items())
    return write(path, name, f"+++\n{front}\n+++\nbody\n")


def render(tmp_path: Path, body: str) -> str:
    """Render a Markdown body through an article."""
    file = write(tmp_path, "x.md", f'+++\ntitle = "T"\ndate = 2026-01-01\n+++\n{body}')
    return Article.from_file(file).content


class TestFrontMatter:
    def test_valid(self, tmp_path: Path) -> None:
        article = Article.from_file(write(tmp_path, "hello-world.md", VALID))
        assert article.slug == "hello-world"
        assert article.title == "Hello"
        assert article.date == datetime.date(2026, 10, 26)
        assert article.description == "A description"
        assert not article.draft
        assert "<em>text</em>" in article.content

    def test_tags_are_normalised(self, tmp_path: Path) -> None:
        article = Article.from_file(write(tmp_path, "a.md", VALID))
        assert article.tags == ("physics", "c")

    def test_properties(self, tmp_path: Path) -> None:
        article = Article.from_file(write(tmp_path, "a.md", VALID))
        assert article.url == "/blog/a/"
        assert article.date_formatted == "2026-10-26"
        assert article.date_short == "10-26"
        assert article.date_long == "October 26, 2026"

    @pytest.mark.parametrize(
        "text",
        [
            "no front matter",
            '+++\ntitle = "T"\ndate = 2026-01-01\n',  # not closed
            '+++\ntitle = "T\n+++\nbody',  # invalid TOML
            '+++\ntitle = "T"\n+++\nbody',  # missing date
            "+++\ndate = 2026-01-01\n+++\nbody",  # missing title
            '+++\ntitle = "T"\ndate = 2026-01-01\nfoo = 1\n+++\nbody',  # unknown
            "+++\ntitle = 1\ndate = 2026-01-01\n+++\nbody",  # wrong type
            '+++\ntitle = "T"\ndate = "2026-01-01"\n+++\nbody',  # date as string
            '+++\ntitle = "T"\ndate = 2026-01-01T10:00:00\n+++\nbody',  # datetime
        ],
    )
    def test_invalid(self, tmp_path: Path, text: str) -> None:
        with pytest.raises(ValueError, match=r"a\.md"):
            Article.from_file(write(tmp_path, "a.md", text))

    @pytest.mark.parametrize("tags", ['[""]', '["  "]', "[1]", '["a/b"]', '[".."]'])
    def test_invalid_tags(self, tmp_path: Path, tags: str) -> None:
        with pytest.raises(ValueError, match="tags"):
            Article.from_file(make(tmp_path, tags=tags))


class TestRendering:
    def test_inline_math_dollars(self, tmp_path: Path) -> None:
        html = render(tmp_path, "Let $x^2$ be.\n")
        assert "<math" in html
        assert "$" not in html

    @pytest.mark.parametrize("body", ["Let \\(x^2\\) be.\n", "Let \\[x^2\\] be.\n"])
    def test_bracket_math_inline(self, tmp_path: Path, body: str) -> None:
        html = render(tmp_path, body)
        assert "<math" in html
        assert "\\" not in html

    def test_display_math_block(self, tmp_path: Path) -> None:
        html = render(tmp_path, "\\[\nx = 1\n\\]\n")
        assert 'display="block"' in html

    def test_display_math_with_blank_line_is_not_math(self, tmp_path: Path) -> None:
        assert "<math" not in render(tmp_path, "\\[\nx\n\ny\n\\]\n")

    def test_unclosed_bracket_math_is_text(self, tmp_path: Path) -> None:
        html = render(tmp_path, "an open \\( paren\n")
        assert "<math" not in html

    def test_lone_image_becomes_figure(self, tmp_path: Path) -> None:
        html = render(tmp_path, "![A *nice* cat](cat.png)\n")
        assert "<figure>" in html
        assert "<figcaption>A <em>nice</em> cat</figcaption>" in html
        assert "<p>" not in html
        assert 'alt="A nice cat"' in html

    def test_inline_image_stays_inline(self, tmp_path: Path) -> None:
        html = render(tmp_path, "See ![cat](cat.png) here.\n")
        assert "<figure>" not in html
        assert "<p>" in html
        assert 'alt="cat"' in html

    def test_typographer_and_tables(self, tmp_path: Path) -> None:
        html = render(tmp_path, '"quoted"\n\n| a |\n|---|\n| 1 |\n')
        assert "“quoted”" in html
        assert "<table>" in html

    def test_raw_html_is_kept(self, tmp_path: Path) -> None:
        assert "<div>hi</div>" in render(tmp_path, "<div>hi</div>\n")


class TestCollections:
    @pytest.fixture
    def folder(self, tmp_path: Path) -> Path:
        make(tmp_path, "old.md", date="2025-03-01", tags='["a", "b"]')
        make(tmp_path, "new.md", date="2026-05-01", tags='["a"]')
        make(tmp_path, "same-day.md", date="2026-05-01")
        make(tmp_path, "wip.md", date="2026-06-01", draft="true")
        (tmp_path / "image.png").write_bytes(b"")
        return tmp_path

    def test_load_sorted_newest_first(self, folder: Path) -> None:
        slugs = [a.slug for a in load_articles(folder)]
        assert slugs == ["same-day", "new", "old"]

    def test_drafts(self, folder: Path) -> None:
        assert "wip" not in {a.slug for a in load_articles(folder)}
        with_drafts = load_articles(folder, include_drafts=True)
        assert with_drafts[0].slug == "wip"

    def test_broken_article_fails_loading(self, folder: Path) -> None:
        write(folder, "broken.md", "nope")
        with pytest.raises(ValueError, match=r"broken\.md"):
            load_articles(folder)

    def test_group_by_tag(self, folder: Path) -> None:
        groups = group_by_tag(load_articles(folder))
        assert list(groups) == ["a", "b"]  # most used first
        assert [a.slug for a in groups["a"]] == ["new", "old"]
        assert [a.slug for a in groups["b"]] == ["old"]

    def test_group_by_year(self, folder: Path) -> None:
        groups = group_by_year(load_articles(folder))
        assert list(groups) == [2026, 2025]
        assert [a.slug for a in groups[2026]] == ["same-day", "new"]

    def test_tag_url_is_encoded(self) -> None:
        assert tag_url("c++") == "/blog/tag/c%2B%2B/"
        assert tag_url("a b") == "/blog/tag/a%20b/"


def test_crlf_line_endings(tmp_path: Path) -> None:
    file = write(tmp_path, "a.md", VALID.replace("\n", "\r\n"))
    assert Article.from_file(file).title == "Hello"
