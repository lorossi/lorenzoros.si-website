"""This script handles the creation of the website."""

import argparse
import logging

from modules.deployer import Deployer
from modules.renderer import Renderer
from modules.scraper import Scraper


def build_homepage(
    offline: bool = False,
    repo_filename: str = "repos.json",
    stats_filename: str = "stats.json",
    settings_path: str = "settings.toml",
    unique_id: str | None = None,
) -> None:
    """Build the homepage.

    Args:
        offline (bool, optional): If True, does not scrape GitHub. Defaults to False.
        filename (str, optional): toml file for the repos. Defaults to "repos.json".
        settings_path (str, optional): settings file path. Defaults to "settings.toml".
    """
    s = Scraper(settings_path=settings_path)

    if offline:
        s.loadRepos()
    else:
        loaded = s.scrapeRepos(skip_private=True)
        if loaded is None:
            return

        s.saveRepos(repo_filename)

    s.saveStats(path=stats_filename)

    r = Renderer(settings_path=settings_path)

    # render base page
    r.renderFile(
        "base.html",
        data={
            "interactive_repos": s.interactive_repos,
            "repos_list": s.repos_list,
            "unique_id": unique_id,
        },
        output_path="../public_html/index.html",
    )


def deploy(settings_path: str = "settings.toml") -> None:
    """Deploy the website."""
    logging.info("Starting to deploy...")
    d = Deployer(settings_path=settings_path)
    d.connect()
    d.deploy()
    d.disconnect()
    logging.info("Deployment finished.")


def gather_arguments() -> argparse.Namespace:
    """Gather command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-H",
        "--homepage",
        action="store_true",
        help="Build the homepage",
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
        "--repo-filename",
        type=str,
        help="Filename to load and save repos from",
        default="out/repos.json",
    )

    parser.add_argument(
        "--stats-filename",
        type=str,
        help="Filename to save stats to",
        default="out/stats.json",
    )

    parser.add_argument(
        "--settings",
        type=str,
        help="Settings file path",
        default="settings.toml",
    )

    parser.add_argument(
        "--unique_id",
        type=str,
        help="Unique ID to append to CSS and JS files for cache busting",
        default=None,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args()


def main():
    """Script entry point."""
    arguments = gather_arguments()
    log_level = logging.DEBUG if arguments.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if not arguments.homepage and not arguments.deploy:
        return

    if arguments.homepage:
        build_homepage(
            offline=arguments.offline,
            repo_filename=arguments.repo_filename,
            stats_filename=arguments.stats_filename,
            settings_path=arguments.settings,
            unique_id=arguments.unique_id,
        )
    if arguments.deploy:
        deploy(
            settings_path=arguments.settings,
        )


if __name__ == "__main__":
    main()
