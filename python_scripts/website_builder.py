import argparse
import logging

from modules.scraper import Scraper
from modules.renderer import Renderer


def main(parser: argparse.ArgumentParser):
    s = Scraper(settings_path="settings.toml")

    arguments = parser.parse_args()
    if arguments.offline:
        s.loadRepos()
    else:
        loaded = s.scrapeRepos(skip_private=True)
        if loaded is None:
            return

        s.saveRepos(arguments.filename)

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


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser()
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
        default="repos.json",
    )

    main(parser)
