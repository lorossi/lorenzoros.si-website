import argparse
import logging
import os
import re
from glob import glob

import pysftp
from modules.mdparser import MarkdownParser
from modules.renderer import Renderer
from modules.scraper import Scraper
from modules.settings import Settings


def build_homepage(offline=False, filename="repos.json"):
    s = Scraper(settings_path="settings.toml")

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
    for a in glob(s.base_path + s.relative_articles_path + "*.html"):
        logging.info(f"Deleting {a} ...")
        os.remove(a)
    logging.info("All old articles deleted.")

    # render blog homepage
    r.renderFile(
        "blog.html",
        context_dict={
            "articles": articles,
            "base_url": s.relative_articles_path,
            "category_path": s.relative_categories_path,
        },
        output_path=s.base_path + "blog.html",
    )

    # render articles
    for x, a in enumerate(articles):
        out_path = s.base_path + s.relative_articles_path + a.link

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

    for c in set([article.category for article in articles]):
        category_articles = [article for article in articles if article.category == c]

        r.renderFile(
            "category.html",
            context_dict={
                "articles": category_articles,
                "category": c,
                "base_url": "../",
            },
            output_path=f"{s.base_path}{s.relative_categories_path}{c}.html",
        )


def deploy():
    s = Settings.from_toml("settings.toml", "Deploy")

    logging.info(f"Connecting to {s.url} ...")
    sftp = pysftp.Connection(
        s.url,
        username=s.username,
        private_key=s.key_path,
        private_key_pass=s.private_key_pass,
    )
    logging.info("Connected.")

    for file in glob(s.local_path + "/**/*", recursive=True):
        remote_path = s.remote_path + re.sub(r".*" + s.local_path, "", file)
        logging.info(f"Uploading {file} ...")

        if os.path.isdir(file):
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass
        else:
            # get remote file mtime
            try:
                remote_mtime = sftp.stat(remote_path).st_mtime
            except IOError:
                remote_mtime = None

            # get local file mtime
            local_mtime = int(os.path.getmtime(file))
            if remote_mtime is None or local_mtime > remote_mtime:
                sftp.put(file, remote_path, preserve_mtime=True)
                logging.info("Uploaded.")
            else:
                time_diff = remote_mtime - local_mtime
                logging.info(f"Skipped (remote file is {time_diff} seconds newer).")

    logging.info("All files uploaded. Closing connection ...")
    sftp.close()
    logging.info("Connection closed.")


def main(parser: argparse.ArgumentParser):
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
        default="repos.json",
    )

    main(parser)
