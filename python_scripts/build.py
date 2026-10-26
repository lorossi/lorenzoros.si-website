"""This script builds the website and deploys it."""

import argparse
import hashlib
import logging
import shutil
import sys
import tomllib
from pathlib import Path

from modules.article import Article, load_articles
from modules.deployer import Deployer
from modules.renderer import Renderer
from modules.scraper import Scraper
from modules.settings import BuilderSettings, DeployerSettings, ScraperSettings

logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent


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


def build_blog(
    renderer: Renderer, settings: BuilderSettings, articles: list[Article]
) -> None:
    """Render the blog index and the articles.

    Any file in the blog folder that is not an article (e.g. an image) is
    copied as it is, so it can be referenced as `/blog/<file>`.

    Args:
        renderer (Renderer): renderer to use.
        settings (BuilderSettings): builder settings.
        articles (list[Article]): articles to render, newest first.
    """
    output = settings.output_path / "blog"
    shutil.copytree(
        settings.blog_path,
        output,
        ignore=shutil.ignore_patterns("*.md"),
        dirs_exist_ok=True,
    )

    renderer.render_file(
        "blog.html", output / "index.html", data={"articles": articles}
    )
    for article in articles:
        renderer.render_file(
            "article.html",
            output / article.slug / "index.html",
            data={"article": article},
        )


def build_site(
    settings: BuilderSettings,
    scraper: Scraper,
    unique_id: str | None,
    *,
    include_drafts: bool = False,
) -> None:
    """Build the whole website in the output folder.

    Args:
        settings (BuilderSettings): builder settings.
        scraper (Scraper): scraper with the repos already loaded.
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

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(settings.static_path, output)

    with (settings.data_path / "contacts.toml").open("rb") as f:
        contacts = tomllib.load(f)["contacts"]

    renderer = Renderer(
        settings.templates_path,
        unique_id=unique_id or compute_unique_id(settings.static_path),
    )
    renderer.render_file(
        "index.html",
        output / "index.html",
        data={
            "interactive_repos": scraper.interactive_repos,
            "repos_list": scraper.repos_list,
            "contacts": contacts,
        },
    )
    renderer.render_file("404.html", output / "404.html")
    build_blog(renderer, settings, articles)


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
    if not arguments.build and not arguments.deploy:
        parser.error("nothing to do: pass --build and/or --deploy")
    return arguments


def run(arguments: argparse.Namespace) -> None:
    """Build and/or deploy the website, as requested by the arguments.

    Args:
        arguments (argparse.Namespace): the parsed command line arguments.
    """
    builder_settings = BuilderSettings.from_toml(arguments.settings)

    if arguments.build:
        scraper = Scraper(ScraperSettings.from_toml(arguments.settings))
        load_repos(
            scraper,
            offline=arguments.offline,
            repo_path=arguments.repo_filename,
            stats_path=arguments.stats_filename,
        )
        build_site(
            builder_settings,
            scraper,
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

    try:
        run(arguments)
    except Exception:
        logger.exception("Build failed, nothing was deployed after the error.")
        return 1

    logger.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
