import copy
import ujson
import logging

from sys import argv
from github import Github
from datetime import datetime


class Scraper:
    def __init__(self):
        # GitHub object
        self._github = None
        self._loadSettings()
        self._GitHubLogin()

    def _loadSettings(self, path: str = "settings.json") -> None:
        """Loads settings from path

        Args:
            path (str, optional): Setting settings path. Defaults to "settings.json".
        """
        with open(path, "r") as json_file:
            self._settings = ujson.load(json_file)
        logging.info("Settings loaded")

    def _GitHubLogin(self) -> None:
        """Logs into github"""
        self._github = Github(self._settings["GitHub"]["access_token"])
        logging.info("Logged into GitHub")

    def _createReposDict(self) -> None:
        """
        format repos dict
        """

        ordered_repos = {}
        languages = {}
        total_commits = 0
        total_stars = 0
        total_size = 0

        # sort by time
        new_repos = sorted(self._repos, key=lambda x: x["created"], reverse=True)
        # sort by language
        new_repos = sorted(new_repos, key=lambda x: x["main_language"], reverse=False)

        # update global stats:
        #   - total commits
        #   - total starred
        #   - languages sizes

        for repo in new_repos:
            total_commits += repo["commits"]
            total_stars += repo["stars"]

            for language in repo["languages"]:
                if language:
                    total_size += repo["languages"][language]

                    if any(language in key for key in languages):
                        languages[language]["absolute_size"] += repo["languages"][
                            language
                        ]
                    else:
                        languages[language] = {
                            "absolute_size": repo["languages"][language]
                        }
        languages_list = [
            {"language": lang, "absolute_size": value["absolute_size"]}
            for lang, value in languages.items()
        ]

        for lang in languages_list:
            lang["relative_size"] = lang["absolute_size"] / total_size
            lang[
                "relative_size_formatted"
            ] = f"{round(lang['relative_size'] * 100, 2)}%"

        languages_list = sorted(
            languages_list, key=lambda x: x["absolute_size"], reverse=True
        )
        del languages

        ordered_repos["repos"] = new_repos
        ordered_repos["languages"] = languages_list
        ordered_repos["stats"] = {
            "total_size": total_size,
            "total_commits": total_commits,
            "total_stars": total_stars,
            "total_languages": len(languages_list),
            "total_new_repos": len(new_repos),
            "last_updated": datetime.now().isoformat(),
        }
        self._repos = copy.deepcopy(ordered_repos)
        logging.info("Repos formatted")

    def scrapeRepos(self) -> None:
        """
        load repos from Github
        """

        new_repos = []

        for repo in self._github.get_user().get_repos():
            # check if any repo topic in in the list of wanted topics
            repo_topics = repo.get_topics()
            wanted_topics = self._settings["GitHub"]["topics"]

            if repo.private:
                logging.warning(f"skipping {repo.full_name}. " f"Reason: private repo ")
                continue

            if all(t not in repo_topics for t in wanted_topics):
                logging.warning(
                    f"skipping {repo.full_name}. "
                    f"Reason: topics are not interesting "
                )
                continue

            # hide from list of interactive sites if found an unwanted topic
            unwanted_topics = self._settings["GitHub"]["topics_skip_websites"]
            hide_interactive = any(t in repo_topics for t in unwanted_topics)

            logging.info(f"scraping repo {repo.full_name}")

            language = repo.language
            homepage = repo.homepage
            homepage_mask = ["www.", "https://", "http://"]
            # get link for projects but skip unwanted projects
            if homepage:
                # clean the link by removing the prefixes
                homepage_clean = homepage
                for h in homepage_mask:
                    homepage_clean = homepage_clean.replace(h, "")
                if homepage_clean[-1] == "/":
                    homepage_clean = homepage_clean[:-1]
            else:
                homepage_clean = None

            # clean name and description
            formatted_name = repo.name.replace("-", " ").lower().strip()

            description = repo.description
            if description[-1] not in [".", "!", "?"]:
                description += "."

            last_pushed = repo.pushed_at.isoformat()
            created = repo.created_at.isoformat()
            # serialize all repos
            new_repos.append(
                {
                    "name": repo.name,
                    "formatted_name": formatted_name,
                    "description": description,
                    "url": repo.html_url,
                    "commits": repo.get_commits().totalCount,
                    "stars": repo.stargazers_count,
                    "main_language": language,
                    "languages": repo.get_languages(),
                    "size": repo.size,
                    "last_pushed_timestamp": last_pushed,
                    "created_timestamp": created,
                    "created_date": created[:-9],
                    "created": repo.created_at,
                    "homepage": homepage,
                    "homepage_clean": homepage_clean,
                    "hide_interactive": hide_interactive,
                    "topics": repo.get_topics(),
                    "tags": [t.name for t in repo.get_tags()],
                }
            )

        self._repos = copy.deepcopy(new_repos)
        logging.info("Repos scraped")

        # now format all repos
        self._createReposDict()

    def formatRepos(self) -> None:
        """
        format the repos in the list form, to be embedded into the homepage
        """

        # create list of projects
        html_list = ""
        html_list += '<ul class="projects-list">\n'

        # sorted list of unique languages
        languages = sorted(list({x["main_language"] for x in self._repos["repos"]}))
        # filter repos by language
        for language in languages:
            selected_repos = [
                x for x in self._repos["repos"] if x["main_language"] == language
            ]

            if not selected_repos:
                continue

            # create html element
            html_list += '<div class="language">'
            html_list += f"{language}</div>"

            for repo in selected_repos:
                html_list += '<li class="project-container">'
                html_list += '<a class="project-title" '
                html_list += f"href=\"{repo['url']}\">"
                html_list += f"{repo['formatted_name']}</a>"
                html_list += '<span class="project-description">'
                html_list += f" {repo['description']}</span>"
                html_list += "</li>\n"

        html_list += "</ul>"
        self._projects_list = html_list

        # create list of interactive projects
        html_list = ""
        html_list += '<ul class="projects-list">\n'

        selected_repos = [x for x in self._repos["repos"] if x["homepage"]]
        selected_repos = sorted(
            selected_repos,
            key=lambda x: datetime.fromisoformat(x["created_timestamp"]),
            reverse=False,
        )

        # add links
        for repo in selected_repos:

            if not repo["homepage"]:
                continue

            if repo["name"] == "lorenzoros.si-website":
                continue

            if repo["hide_interactive"]:
                continue

            html_list += '<li class="interactive-container">'
            html_list += '<a class="project-title" '
            html_list += f"href=\"{repo['homepage']}\">"
            html_list += f"{repo['formatted_name']}</a>"
            html_list += '<span class="project-date">'
            html_list += " created: "
            html_list += f"{repo['created_date']}</span>"
            html_list += "</li>\n"

        html_list += "</ul>"

        self._interactive_list = html_list

        logging.info("Repos list generated")

    def loadRepos(self) -> None:
        """
        load repos from json file
        """
        with open(self._settings["json_file"], "r") as json_file:
            self._repos = ujson.load(json_file)

        # sort by time
        self._repos["repos"] = sorted(
            self._repos["repos"],
            key=lambda x: datetime.fromisoformat(x["created_timestamp"]),
            reverse=True,
        )

        # sort by language
        self._repos["repos"] = sorted(
            self._repos["repos"], key=lambda x: x["main_language"], reverse=False
        )

    def saveRepos(self) -> None:
        """
        save repos and html formatted files
        """

        repos_to_dump = copy.deepcopy(self._repos)
        for repo in repos_to_dump["repos"]:
            # remove date as it's not serializable
            if "created" in repo:
                del repo["created"]

        with open(self._settings["json_file"], "w") as json_file:
            ujson.dump(repos_to_dump, json_file, indent=2, sort_keys=True)

        with open(self._settings["html_projects_file"], "w") as html_file:
            html_file.write(self._projects_list)

        with open(self._settings["html_interactive_file"], "w") as html_file:
            html_file.write(self._interactive_list)

        logging.info("Files saved")

    def embedRepos(self) -> None:
        """
        save repos to base file
        """

        # check if repos were scraped
        if not (self._interactive_list and self._projects_list):
            logging.error(
                "Cannot embed into base file, "
                "first you have to scrape the repos and format them"
            )
            return

        # open the base file
        with open(self._settings["html_base_file"], "r") as html_file:
            homepage = html_file.read()

        # replace the placeholder
        homepage = homepage.replace(
            "{{ INTERACTIVE PLACEHOLDER }}", self._interactive_list
        )

        # replace the placeholder
        homepage = homepage.replace("{{ PROJECTS PLACEHOLDER }}", self._projects_list)

        # save the file with the lists
        with open("index.html", "w") as html_file:
            html_file.write(homepage)

    @property
    def repos(self) -> list[dict]:
        """
        get the dict containing all the repos
        """
        self.loadRepos()
        return self._repos


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    s = Scraper()

    # call with argument --offline to avoid scraping
    if len(argv) > 1 and "--offline" in argv[1]:
        s.loadRepos()
    else:
        s.scrapeRepos()

    s.formatRepos()
    s.saveRepos()
    s.embedRepos()


if __name__ == "__main__":
    main()
