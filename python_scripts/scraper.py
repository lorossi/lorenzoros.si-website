import argparse
import logging

from modules.scraper import Scraper


def main(parser: argparse.ArgumentParser):
    s = Scraper(settings_path="resources/settings.toml")

    arguments = parser.parse_args()
    if arguments.offline:
        s.loadRepos()
    else:
        s.scrapeRepos(skip_private=True)
        s.saveRepos()

    s.createHTMLLists()
    s.saveHTMLLists()


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

    main(parser)
