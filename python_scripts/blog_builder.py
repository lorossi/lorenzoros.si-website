import logging
import os
from glob import glob

from modules.article import Article
from modules.mdparser import MarkdownParser
from modules.renderer import Renderer
from modules.settings import Settings


def create_out_path(s: Settings, a: Article) -> str:
    return s.base_path + s.relative_articles_path + a.link


def create_category_out_path(s: Settings, a: Article) -> str:
    return s.base_path + s.relative_categories_path + a.category + ".html"


def main():
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
    for article in glob(s.base_path + s.relative_articles_path + "*.html"):
        logging.info(f"Deleting {article} ...")
        os.remove(article)
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
    for x, article in enumerate(articles):
        out_path = create_out_path(s, article)

        # check if article is already rendered
        if glob(out_path) and not article.overwrite:
            logging.info(f"Article {article.title} already rendered. Skipping.")
            continue

        context_dict = {
            "content": article.content,
            "title": article.title,
            "date": article.date,
            "prev_link": articles[x + 1].link if x < len(articles) - 1 else "",
            "next_link": articles[x - 1].link if x > 0 else "",
        }

        # render and save the article
        logging.info(f"Rendering article {article.title} to {out_path} ...")
        r.renderFile(
            "article.html",
            context_dict=context_dict,
            output_path=out_path,
        )
        logging.info("Done.")

    for category in set([article.category for article in articles]):
        category_articles = [
            article for article in articles if article.category == category
        ]

        r.renderFile(
            "category.html",
            context_dict={
                "articles": category_articles,
                "category": category,
                "base_url": "../",
            },
            output_path=f"{s.base_path}{s.relative_categories_path}{category}.html",
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
