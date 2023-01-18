import argparse
import logging

from modules.scraper import Scraper
from modules.renderer import Renderer


def main(parser: argparse.ArgumentParser):
    s = Scraper(settings_path="resources/settings.toml")

    arguments = parser.parse_args()
    if arguments.offline:
        s.loadRepos()
    else:
        s.scrapeRepos(skip_private=True)
        s.saveRepos()

    s.createHTMLLists()

    r = Renderer(settings_path="resources/settings.toml")
    r.render(
        template="resources/base.html",
        context={"interactive_list": s.interactive_list, "static_list": s.static_list},
        out_path="../public_html/index.html",
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

    main(parser)
