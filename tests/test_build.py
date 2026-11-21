"""Tests for the build helpers and a smoke test of the real templates."""

import datetime
from pathlib import Path
from typing import Any

import pytest

from build import build_blog, compute_unique_id
from modules.article import Article, load_articles, tag_url
from modules.renderer import Renderer
from modules.settings import BuilderSettings

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "python_scripts" / "templates"


def test_unique_id_changes_with_content(tmp_path: Path) -> None:
    (tmp_path / "a.css").write_text("a")
    first = compute_unique_id(tmp_path)
    assert first == compute_unique_id(tmp_path)
    assert len(first) == 12

    (tmp_path / "a.css").write_text("b")
    assert compute_unique_id(tmp_path) != first


def test_unique_id_changes_with_names(tmp_path: Path) -> None:
    (tmp_path / "a.css").write_text("a")
    first = compute_unique_id(tmp_path)
    (tmp_path / "a.css").rename(tmp_path / "b.css")
    assert compute_unique_id(tmp_path) != first


@pytest.fixture
def renderer() -> Renderer:
    return Renderer(TEMPLATES, unique_id="test", tag_url=tag_url)


def test_404_renders(renderer: Renderer, tmp_path: Path) -> None:
    html = renderer.render_file("404.html", tmp_path / "404.html")
    assert "<html" in html


def make_settings(tmp_path: Path, blog: Path) -> BuilderSettings:
    return BuilderSettings(
        templates_path=TEMPLATES,
        static_path=tmp_path,
        data_path=tmp_path,
        blog_path=blog,
        output_path=tmp_path / "dist",
        cache_path=tmp_path,
    )


def write_article(blog: Path, slug: str, **extra: Any) -> None:
    meta = {"title": f'"{slug}"', "date": "2026-01-02", **extra}
    front = "\n".join(f"{k} = {v}" for k, v in meta.items())
    (blog / f"{slug}.md").write_text(f"+++\n{front}\n+++\nHi $x$\n", encoding="utf-8")


def test_build_blog(renderer: Renderer, tmp_path: Path) -> None:
    blog = tmp_path / "blog"
    blog.mkdir()
    write_article(blog, "first", tags='["x", "y"]')
    write_article(blog, "second", tags='["x"]', date="2025-05-05")
    (blog / "pic.png").write_bytes(b"png")
    settings = make_settings(tmp_path, blog)

    build_blog(renderer, settings, load_articles(blog))

    out = tmp_path / "dist" / "blog"
    assert (out / "index.html").is_file()
    assert (out / "first" / "index.html").is_file()
    assert (out / "second" / "index.html").is_file()
    assert (out / "tag" / "x" / "index.html").is_file()
    assert (out / "tag" / "y" / "index.html").is_file()
    assert (out / "pic.png").is_file()  # non-Markdown files are copied
    assert not (out / "first.md").exists()
    assert "<math" in (out / "first" / "index.html").read_text(encoding="utf-8")


def test_article_named_tag_is_rejected(renderer: Renderer, tmp_path: Path) -> None:
    blog = tmp_path / "blog"
    blog.mkdir()
    article = Article(slug="tag", title="T", date=datetime.date(2026, 1, 1), content="")
    with pytest.raises(ValueError, match="tag"):
        build_blog(renderer, make_settings(tmp_path, blog), [article])


def test_real_blog_posts_build(renderer: Renderer, tmp_path: Path) -> None:
    """The articles in the repository must parse and render."""
    blog = ROOT / "blog"
    articles = load_articles(blog, include_drafts=True)
    settings = make_settings(tmp_path, blog)
    build_blog(renderer, settings, articles)
    for article in articles:
        assert (tmp_path / "dist" / "blog" / article.slug / "index.html").is_file()
