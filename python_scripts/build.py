"""This script handles the creation of the website and the blog."""

import argparse
import logging
import os
from glob import glob

from modules.deployer import Deployer
from modules.mdparser import MarkdownParser
from modules.renderer import Renderer
from modules.scraper import Scraper
from modules.settings import Settings


def build_homepage(offline: bool = False, filename: str = "repos.json"):
    """Build the homepage.

    Args:
        offline (bool, optional): If True, does not scrape GitHub. Defaults to False.
        filename (str, optional): json file for the repos. Defaults to "repos.json".
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


def build_blog():
    """Build the blog."""
    # TODO: encapsulate this into a class
    s = Settings.from_toml("settings.toml", "Blog")

    m = MarkdownParser()
    # load articles
    articles = sorted(
        [m.parseFile(article) for article in glob(f"{s.articles_path}/*.md")],
        key=lambda x: x.date_obj,
        reverse=True,
    )

    r = Renderer()

    # delete all rendered articles
    for a in glob(s.out_path + "*.html"):
        logging.info(f"Deleting {a} ...")
        os.remove(a)
    logging.info("All old articles deleted.")

    # render blog homepage
    r.renderFile(
        "blog.html",
        context_dict={
            "articles": articles,
        },
        output_path=s.out_path + "blog.html",
    )

    # render articles
    for x, a in enumerate(articles):
        out_path = f"{s.out_path}{a.link}"

        # check if article is already rendered
        if glob(out_path) and not a.overwrite:
            logging.info(f"Article {a.title} already rendered. Skipping.")
            continue

        context_dict = {
            "content": a.content,
            "title": a.title,
            "date": a.date,
            "prev_link": articles[x + 1].link if x < len(articles) - 1 else "",
            "next_link": articles[x - 1].link if x > 0 else "",
        }

        # render and save the article
        logging.info(f"Rendering article {a.title} to {out_path} ...")
        r.renderFile(
            "article.html",
            context_dict=context_dict,
            output_path=out_path,
        )
        logging.info("Done.")

    categories = set([article.category.upper() for article in articles])
    for c in sorted(categories):
        category_articles = [article for article in articles if article.category == c]

        r.renderFile(
            "category.html",
            context_dict={
                "articles": category_articles,
                "category": c,
            },
            output_path=f"{s.out_path}category-{c}.html",
        )


def deploy():
    """Deploy the website."""
    logging.info("Starting to deploy...")
    d = Deployer()
    d.connect()
    d.deploy()
    d.disconnect()
    logging.info("Deployment finished.")


def main(parser: argparse.ArgumentParser):
    """Script entry point."""
    arguments = parser.parse_args()
    if arguments.homepage:
        build_homepage(offline=arguments.offline, filename=arguments.filename)
    if arguments.blog:
        build_blog()
    if arguments.deploy:
        deploy()

    if not arguments.homepage and not arguments.blog and not arguments.deploy:
        parser.print_help()


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
        "-B",
        "--blog",
        action="store_true",
        help="Build the blog",
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
