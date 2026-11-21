"""This script builds the website and deploys it."""

import argparse
import datetime
import hashlib
import logging
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Any

from modules.article import (
    Article,
    group_by_tag,
    group_by_year,
    load_articles,
    tag_url,
)
from modules.deployer import Deployer
from modules.github import GitHub
from modules.previews import PreviewFetcher
from modules.renderer import Renderer
from modules.repository import Repository
from modules.scraper import Scraper
from modules.settings import BuilderSettings, DeployerSettings, ScraperSettings

logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
PREVIEWS_URL = "/assets/previews/"
LATEST_ARTICLES = 3  # how many articles the homepage shows


def compute_unique_id(static_path: Path) -> str:
    """Hash the static files, so the id changes only when they change.

    Args:
        static_path (Path): folder containing the static files.

    Returns:
        str: short hexadecimal hash.
    """
    digest = hashlib.sha256()
    for path in sorted(static_path.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(static_path).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def load_repos(
    scraper: Scraper, *, offline: bool, repo_path: Path, stats_path: Path
) -> None:
    """Load the repos, either from GitHub or from a local file.

    Args:
        scraper (Scraper): scraper to fill.
        offline (bool): if True, load repos from `repo_path` instead of GitHub.
        repo_path (Path): file to load the repos from or save them to.
        stats_path (Path): file to save the stats to.
    """
    if offline:
        scraper.load_repos(repo_path)
    else:
        scraper.scrape_repos(skip_private=True)
        scraper.save_repos(repo_path)

    scraper.save_stats(stats_path)


def build_previews(
    fetcher: PreviewFetcher,
    scraper: Scraper,
    output: Path,
) -> dict[str, str]:
    """Make the previews of the interactive repos available to the site.

    Args:
        fetcher (PreviewFetcher): fetcher to use.
        scraper (Scraper): scraper with the repos already loaded.
        output (Path): folder the previews are copied to.

    Returns:
        dict[str, str]: preview file name inside `output`, by repo name.
    """
    repos = scraper.interactive_repos
    fetcher.fetch(repos)
    return fetcher.copy_to(repos, output)


def check_slugs(articles: list[Article]) -> None:
    """Check that no article uses a reserved name.

    Args:
        articles (list[Article]): articles to check.

    Raises:
        ValueError: if an article is named "tag", like the tag pages folder.
    """
    if any(a.slug == "tag" for a in articles):
        msg = 'an article cannot be named "tag", it is used by the tag pages'
        raise ValueError(msg)


def build_blog(
    renderer: Renderer, settings: BuilderSettings, articles: list[Article]
) -> None:
    """Render the blog index and the articles.

    Besides the index, each tag gets a filtered copy of it at
    `/blog/tag/<tag>/`. Any file in the blog folder that is not an article
    (e.g. an image) is copied as it is, so it can be referenced as
    `/blog/<file>`.

    Args:
        renderer (Renderer): renderer to use.
        settings (BuilderSettings): builder settings.
        articles (list[Article]): articles to render, newest first.
    """
    output = settings.output_path / "blog"
    check_slugs(articles)
    shutil.copytree(
        settings.blog_path,
        output,
        ignore=shutil.ignore_patterns("*.md"),
        dirs_exist_ok=True,
    )

    groups = group_by_tag(articles)
    tags = {tag: len(tagged) for tag, tagged in groups.items()}

    # the index with every article, then one filtered copy per tag
    pages: list[tuple[str | None, list[Article], Path]] = [
        (None, articles, output / "index.html")
    ]
    pages += [
        (tag, tagged, output / "tag" / tag / "index.html")
        for tag, tagged in groups.items()
    ]
    for active_tag, shown, path in pages:
        renderer.render_file(
            "blog.html",
            path,
            data={
                "total": len(articles),
                "tags": tags,
                "active_tag": active_tag,
                "shown": len(shown),
                "years": group_by_year(shown),
            },
        )

    for article in articles:
        renderer.render_file(
            "article.html",
            output / article.slug / "index.html",
            data={"article": article},
        )


def shell_data(
    scraper: Scraper,
    articles: list[Article],
    contacts: list[dict[str, Any]],
    blog_path: Path,
) -> dict[str, Any]:
    """Collect the data the /shell page turns into its fake file system.

    Contacts without an href (the ones revealed by secret.js) are listed
    with their name only, so nothing hidden ends up in the page.

    Args:
        scraper (Scraper): scraper with the repos already loaded.
        articles (list[Article]): published articles, newest first.
        contacts (list[dict[str, Any]]): the contacts from contacts.toml.
        blog_path (Path): folder with the Markdown sources of the articles.

    Returns:
        dict[str, Any]: JSON-serialisable data, embedded in the page.
    """

    def repo(r: Repository, url: str) -> dict[str, str]:
        return {
            "name": r.name.lower(),
            "description": r.description_formatted,
            "date": r.last_push_formatted,
            "url": url,
        }

    return {
        "built": datetime.date.today().isoformat(),
        "repos_total": len(scraper.repos),
        "interactive": [repo(r, r.interactive_url) for r in scraper.interactive_repos],
        "portfolio": {
            lang.lower().replace(" ", "-"): [repo(r, r.html_url) for r in repos]
            for lang, repos in scraper.repos_list.items()
        },
        "articles": [
            {
                "slug": a.slug,
                "date": a.date_formatted,
                "url": a.url,
                "source": (blog_path / f"{a.slug}.md").read_text(encoding="utf-8"),
            }
            for a in articles
        ],
        "contacts": [
            {
                "name": c["name"],
                "text": c["text"],
                "label": c["label"],
                "href": c.get("href"),
            }
            for c in contacts
        ],
    }


def build_site(
    settings: BuilderSettings,
    scraper: Scraper,
    fetcher: PreviewFetcher,
    unique_id: str | None,
    *,
    include_drafts: bool = False,
) -> None:
    """Build the whole website in the output folder.

    Args:
        settings (BuilderSettings): builder settings.
        scraper (Scraper): scraper with the repos already loaded.
        fetcher (PreviewFetcher): downloads the previews of the interactive
            repos.
        unique_id (str | None): cache-busting id. If None, it is computed
            from the static files.
        include_drafts (bool, optional): if True, draft articles are
            published too. Defaults to False.
    """
    output = settings.output_path
    logger.info("Building website in %s", output)

    # load the articles first, so a broken one fails the build before
    # the output folder is touched
    articles = load_articles(settings.blog_path, include_drafts=include_drafts)
    check_slugs(articles)

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(settings.static_path, output)

    with (settings.data_path / "contacts.toml").open("rb") as f:
        contacts = tomllib.load(f)["contacts"]

    previews = build_previews(fetcher, scraper, output / PREVIEWS_URL.strip("/"))

    renderer = Renderer(
        settings.templates_path,
        unique_id=unique_id or compute_unique_id(settings.static_path),
        tag_url=tag_url,
    )
    renderer.render_file(
        "index.html",
        output / "index.html",
        data={
            "interactive_repos": scraper.interactive_repos,
            "previews": {n: f"{PREVIEWS_URL}{f}" for n, f in previews.items()},
            "repos_list": scraper.repos_list,
            "contacts": contacts,
            "latest_articles": articles[:LATEST_ARTICLES],
        },
    )
    renderer.render_file(
        "shell.html",
        output / "shell" / "index.html",
        data={
            "shell": shell_data(scraper, articles, contacts, settings.blog_path),
        },
    )
    renderer.render_file("404.html", output / "404.html")
    build_blog(renderer, settings, articles)


def healthcheck(settings_path: Path) -> bool:
    """Check that the GitHub token and the SSH key both work.

    Every check is run, even if a previous one failed.

    Args:
        settings_path (Path): settings file path.

    Returns:
        bool: True if all the checks passed.
    """
    ok = True

    logger.info("Checking the GitHub token...")
    try:
        settings = ScraperSettings.from_toml(settings_path)
        GitHub(settings.username, settings.token).check_token()
    except Exception:
        logger.exception("GitHub token check failed")
        ok = False

    logger.info("Checking the SSH key...")
    try:
        with Deployer(DeployerSettings.from_toml(settings_path)) as d:
            d.check()
    except Exception:
        logger.exception("SSH key check failed")
        ok = False

    return ok


def gather_arguments() -> argparse.Namespace:
    """Gather command line arguments.

    Returns:
        argparse.Namespace: the parsed arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "-B",
        "--build",
        "-H",
        "--homepage",
        dest="build",
        action="store_true",
        help="Build the website",
    )
    parser.add_argument(
        "-D",
        "--deploy",
        action="store_true",
        help="Deploy the website",
    )
    parser.add_argument(
        "-C",
        "--check",
        action="store_true",
        help="Check that the GitHub token and the SSH key work, then exit",
    )
    parser.add_argument(
        "-o",
        "--offline",
        action="store_true",
        help="Load repos from local file instead of scraping them",
    )
    parser.add_argument(
        "--drafts",
        action="store_true",
        help="Publish the draft blog articles too (for previewing)",
    )
    parser.add_argument(
        "--repo-filename",
        type=Path,
        help="File to load and save repos from",
        default=SCRIPT_DIR / "repos.json",
    )
    parser.add_argument(
        "--stats-filename",
        type=Path,
        help="File to save stats to",
        default=SCRIPT_DIR / "stats.json",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        help="Settings file path",
        default=SCRIPT_DIR / "settings.toml",
    )
    parser.add_argument(
        "--unique-id",
        type=str,
        help="Id appended to CSS and JS urls for cache busting "
        "(default: hash of the static files)",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    arguments = parser.parse_args()
    if not (arguments.build or arguments.deploy or arguments.check):
        parser.error("nothing to do: pass --build, --deploy and/or --check")
    if arguments.check and (arguments.build or arguments.deploy):
        parser.error("--check cannot be combined with --build or --deploy")
    return arguments


def run(arguments: argparse.Namespace) -> None:
    """Build and/or deploy the website, as requested by the arguments.

    Args:
        arguments (argparse.Namespace): the parsed command line arguments.
    """
    builder_settings = BuilderSettings.from_toml(arguments.settings)

    if arguments.build:
        scraper_settings = ScraperSettings.from_toml(arguments.settings)
        scraper = Scraper(scraper_settings)
        fetcher = PreviewFetcher(
            scraper_settings,
            builder_settings.cache_path / "previews",
            offline=arguments.offline,
        )
        load_repos(
            scraper,
            offline=arguments.offline,
            repo_path=arguments.repo_filename,
            stats_path=arguments.stats_filename,
        )
        build_site(
            builder_settings,
            scraper,
            fetcher,
            arguments.unique_id,
            include_drafts=arguments.drafts,
        )

    if arguments.deploy:
        with Deployer(DeployerSettings.from_toml(arguments.settings)) as d:
            d.deploy(builder_settings.output_path)


def main() -> int:
    """Script entry point.

    Returns:
        int: exit code.
    """
    arguments = gather_arguments()
    logging.basicConfig(
        level=logging.DEBUG if arguments.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if arguments.check:
        if not healthcheck(arguments.settings):
            logger.error("Healthcheck failed.")
            return 1
        logger.info("Healthcheck passed.")
        return 0

    try:
        run(arguments)
    except Exception:
        logger.exception("Build failed, nothing was deployed after the error.")
        return 1

    logger.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
