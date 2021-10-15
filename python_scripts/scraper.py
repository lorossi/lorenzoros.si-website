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

    def _loadSettings(self, path="settings.json"):
        """
        load settings from path
        """

        with open(path, "r") as json_file:
            self._settings = ujson.load(json_file)
        logging.info("Settings loaded")

    def _GitHubLogin(self):
        """
        login into GitHub
        """

        self._github = Github(self._settings["GitHub"]["access_token"])
        logging.info("Logged into GitHub")

    def _createReposDict(self):
        """
        format repos dict
        """

        ordered_repos = {}
        languages = {}
        total_commits = 0
        total_stars = 0
        total_size = 0

        # sort by time
        new_repos = sorted(
            self._repos, key=lambda x: x["created"], reverse=True
        )
        # sort by language
        new_repos = sorted(
            new_repos, key=lambda x: x["main_language"], reverse=False
        )

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
                        languages[language]["absolute_size"] += \
                            repo["languages"][language]
                    else:
                        languages[language] = {
                            "absolute_size": repo["languages"][language]}
        languages_list = [
            {"language": lang, "absolute_size": value["absolute_size"]}
            for lang, value in languages.items()
        ]

        for lang in languages_list:
            lang["relative_size"] = lang["absolute_size"] / total_size
            lang["relative_size_formatted"] = \
                f"{round(lang['relative_size'] * 100, 2)}%"

        languages_list = sorted(
            languages_list, key=lambda x: x["absolute_size"], reverse=True)
        del languages

        ordered_repos["repos"] = new_repos
        ordered_repos["languages"] = languages_list
        ordered_repos["stats"] = {
            "total_size": total_size,
            "total_commits": total_commits,
            "total_stars": total_stars,
            "total_languages": len(languages_list),
            "total_new_repos": len(new_repos),
            "last_updated": datetime.now().isoformat()
        }
        self._repos = copy.deepcopy(ordered_repos)
        logging.info("Repos formatted")

    def scrapeRepos(self):
        """
        load repos from Github
        """

        new_repos = []

        for repo in self._github.get_user().get_repos():
            # check if any repo topic in in the list of wanted topics
            repo_topics = repo.get_topics()
            wanted_topics = self._settings["GitHub"]["topics"]
            if all(t not in repo_topics for t in wanted_topics):
                logging.info(
                    f"skipping {repo.full_name}. "
                    f"Reason: topics are not interesting "
                )
                continue

            # hide from list of interactive sites if found an unwanted topic
            unwanted_topics = self._settings["GitHub"]["skip_websites"]
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
            new_repos.append({
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
                "tags": [t.name for t in repo.get_tags()]
            })

        self._repos = copy.deepcopy(new_repos)
        logging.info("Repos scraped")

        # now format all repos
        self._createReposDict()

    def formatRepos(self):
        """
        format the repos in the list form, to be embedded into the homepage
        """

        # create list of projects
        self._projects_list = ""
        self._projects_list += "<ul class=\"projects-list\">"

        # sorted list of unique languages
        languages = sorted(list({x["main_language"]
                                 for x in self._repos["repos"]}))
        # filter repos by language
        for language in languages:
            selected_repos = [x for x in self._repos["repos"]
                              if x["main_language"] == language]

            if not selected_repos:
                continue

            # create html element
            self._projects_list += "<div class=\"language\">"
            self._projects_list += f"{language}</div>"

            for repo in selected_repos:
                self._projects_list += "<li class=\"project-container\">"
                self._projects_list += "<a class=\"project-title\" "
                self._projects_list += f"href=\"{repo['url']}\">"
                self._projects_list += f"{repo['formatted_name']}</a>"
                self._projects_list += "<span class=\"project-description\">"
                self._projects_list += f" {repo['description']}</span>"
                self._projects_list += "</li>"

        self._projects_list += "</ul>"

        # create list of interactive projects
        self._interactive_list = ""
        self._interactive_list += "<ul class=\"projects-list\">"

        selected_repos = [x for x in self._repos["repos"] if x["homepage"]]
        selected_repos = sorted(
            selected_repos, key=lambda x: datetime.fromisoformat(
                x["created_timestamp"]
            ),
            reverse=False
        )

        # add links
        for repo in selected_repos:

            if not repo["homepage"]:
                continue

            if repo["name"] == "lorenzoros.si-website":
                continue

            if repo["hide_interactive"]:
                continue

            self._interactive_list += "<li class=\"interactive-container\">"
            self._interactive_list += "<a class=\"project-title\" "
            self._interactive_list += f"href=\"{repo['homepage']}\">"
            self._interactive_list += f"{repo['formatted_name']}</a>"
            self._interactive_list += "<span class=\"project-date\">"
            self._interactive_list += " created: "
            self._interactive_list += f"{repo['created_date']}</span>"
            self._interactive_list += "</li>"

        self._interactive_list += "</ul>"

        logging.info("Repos list generated")

    def loadRepos(self):
        """
        load repos from json file
        """
        with open(self._settings["json_file"], "r") as json_file:
            self._repos = ujson.load(json_file)

        # sort by time
        self._repos["repos"] = sorted(
            self._repos["repos"],
            key=lambda x: datetime.fromisoformat(
                x["created_timestamp"]
            ),
            reverse=True
        )

        # sort by language
        self._repos["repos"] = sorted(
            self._repos["repos"], key=lambda x: x["main_language"],
            reverse=False)

    def saveRepos(self):
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

    def embedRepos(self):
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
            "{{ INTERACTIVE PLACEHOLDER }}",
            self._interactive_list
        )

        # replace the placeholder
        homepage = homepage.replace(
            "{{ PROJECTS PLACEHOLDER }}",
            self._projects_list
        )

        # save the file with the lists
        with open("index.html", "w") as html_file:
            html_file.write(homepage)

    @property
    def repos(self):
        """
        get the dict containing all the repos
        """
        self.loadRepos()
        return self._repos


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
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
