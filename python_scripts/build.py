"""This script handles the creation of the website."""

import argparse
import logging

from modules.deployer import Deployer
from modules.renderer import Renderer
from modules.scraper import Scraper


def build_homepage(offline: bool = False, filename: str = "repos.json"):
    """Build the homepage.

    Args:
        offline (bool, optional): If True, does not scrape GitHub. Defaults to False.
        filename (str, optional): toml file for the repos. Defaults to "repos.json".
    """
    s = Scraper()

    if offline:
        s.loadRepos()
    else:
        loaded = s.scrapeRepos(skip_private=True)
        if loaded is None:
            return

        s.saveRepos(filename)

    s.saveStats()

    r = Renderer()
    # # render base page
    r.renderFile(
        "base.html",
        context_dict={
            "interactive_repos": s.interactive_repos,
            "repos_list": s.repos_list,
        },
        output_path="../public_html/index.html",
        format=False,
    )


def deploy():
    """Deploy the website."""
    logging.info("Starting to deploy...")
    d = Deployer()
    d.connect()
    d.deploy()
    d.disconnect()
    logging.info("Deployment finished.")


def main(arg_parser: argparse.ArgumentParser):
    """Script entry point."""
    arguments = arg_parser.parse_args()
    if arguments.homepage:
        build_homepage(offline=arguments.offline, filename=arguments.filename)
    if arguments.deploy:
        deploy()

    if not arguments.homepage and not arguments.deploy:
        arg_parser.print_help()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

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
        "-f",
        "--filename",
        type=str,
        help="Filename to load and save repos from",
        default="out/repos.json",
    )

    main(parser)
