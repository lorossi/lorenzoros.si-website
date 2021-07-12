import ujson
import logging
import copy
from github import Github
from datetime import datetime


class Scraper:
    def __init__(self):
        # GitHub object
        self.g = None
        self.loadSettings()
        self.GitHubLogin()

    # Load settings from path
    def loadSettings(self, path="settings.json"):
        with open(path, "r") as json_file:
            self.settings = ujson.load(json_file)
        logging.info("Settings loaded")

    # login into GitHub
    def GitHubLogin(self):
        self.g = Github(self.settings["GitHub"]["access_token"])
        logging.info("Logged into GitHub")

    # load repos from Github
    def scrapeRepos(self):
        new_repos = []

        for repo in self.g.get_user().get_repos():
            # check if any repo topic in in the list of wanted topics
            repo_topics = repo.get_topics()
            wanted_topics = self.settings["GitHub"]["topics"]
            if not any(t in repo_topics for t in wanted_topics):
                logging.info(
                    f"skipping {repo.full_name}."
                    f"Reason: topics are not interesting "
                )
                continue

            # hide from list of interactive sites if found an unnwated topic
            unwanted_topics = self.settings["GitHub"]["skip_websites"]
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
            formatted_name = repo.name.replace("-", " ").lower()

            description = repo.description
            if not description[-1] == ".":
                if description[-1] not in ["!", "?"]:
                    description += "."

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
                "last_pushed_timestamp": repo.pushed_at.isoformat(),
                "created_timestamp": repo.created_at.isoformat(),
                "created_year": repo.created_at.year,
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
        self.formatRepos()

    # format repos dict
    def formatRepos(self):
        ordered_repos = {}
        languages = {}
        languages_list = []
        total_commits = 0
        total_stars = 0
        total_size = 0

        # sort by time
        new_repos = sorted(
            self._repos, key=lambda x: x["created"], reverse=True)
        # sort by language
        new_repos = sorted(
            new_repos, key=lambda x: x["main_language"], reverse=False)

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
                        languages[language]["absolute_size"] += repo["languages"][language]
                    else:
                        languages[language] = {}
                        languages[language]["absolute_size"] = repo["languages"][language]

        for lang in languages:
            languages_list.append({
                "language": lang,
                "absolute_size": languages[lang]["absolute_size"]
            })

        for lang in languages_list:
            lang["relative_size"] = lang["absolute_size"] / total_size
            lang["relative_size_formatted"] = f"{round(lang['relative_size'] * 100, 2)}%"

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

    # save repos and html formatted files
    def saveData(self):
        repos_to_dump = copy.deepcopy(self._repos)
        for repo in repos_to_dump["repos"]:
            # remove date as it's not serializable
            del repo["created"]

        with open(self.settings["json_file"], "w") as json_file:
            ujson.dump(repos_to_dump, json_file, indent=2, sort_keys=True)

        with open(self.settings["html_projects_file"], "w") as html_file:
            html_file.write(self._projects_list)

        with open(self.settings["html_interactive_file"], "w") as html_file:
            html_file.write(self._interactive_list)

        logging.info("Files saved")

    # format the repos in the list form, to be embedded into the homepage
    def formatList(self):
        # create list of projects
        self._projects_list = ""

        # sorted list of unique languages
        languages = sorted(list(set(x["main_language"]
                                    for x in self._repos["repos"])))
        # filter repos by language
        for language in languages:
            selected_repos = [x for x in self._repos["repos"]
                              if x["main_language"] == language]

            if len(selected_repos) == 0:
                continue

            # create html element
            self._projects_list += "<ul class=\"projects-list\">\n"
            self._projects_list += f"\t<div class=\"language\">{language}</div>\n"

            for repo in selected_repos:
                self._projects_list += "\t<li class=\"project-container\">\n"
                self._projects_list += f"\t\t<a class=\"project-title\" href=\"{repo['url']}\">{repo['formatted_name']}</a>\n"
                self._projects_list += f"\t\t<span class=\"project-description\">{repo['description']}</span>\n"
                self._projects_list += "\t</li>\n"

            self._projects_list += "</ul>\n\n"

        self._interactive_list = ""
        self._interactive_list += "<ul class=\"projects-list\">\n"

        selected_repos = [x for x in self._repos["repos"] if x["homepage"]]
        selected_repos = sorted(
            selected_repos, key=lambda x: x["created"], reverse=False)

        # create list of links
        for repo in selected_repos:

            if not repo["homepage"]:
                continue

            if repo["name"] == "lorenzoros.si-website":
                continue

            if repo["hide_interactive"]:
                continue

            self._interactive_list += "\t<li class=\"interactive-container\">\n"
            self._interactive_list += f"\t\t<a class=\"project-title\" href=\"{repo['homepage']}\">{repo['formatted_name']}</a>\n"
            self._interactive_list += "\t</li>\n"

        self._interactive_list += "</ul>\n\n"

        logging.info("Repos list generated")

    # load repos from file
    def loadData(self):
        with open(self.settings["json_file"], "r") as json_file:
            self._repos = ujson.load(json_file)

        # sort by time
        self._repos["repos"] = sorted(self._repos["repos"], key=lambda x: datetime.fromisoformat(
            x["created_timestamp"]), reverse=True)
        # sort by language
        self._repos["repos"] = sorted(
            self._repos["repos"], key=lambda x: x["main_language"], reverse=False)

    # getter
    @property
    def repos(self):
        self.loadData()
        return self._repos


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    s = Scraper()
    s.scrapeRepos()
    s.formatList()
    s.saveData()


if __name__ == "__main__":
    main()
