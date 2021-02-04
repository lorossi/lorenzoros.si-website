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
            if any(word in repo.name for word in self.settings["GitHub"]["skip_names"]):
                continue

            if any(url in repo.html_url for url in self.settings["GitHub"]["skip_urls"]):
                continue

            if not repo.language:
                continue

            if not repo.name in self.settings["GitHub"]["selected_repos"]:
                continue

            language = repo.language
            homepage = repo.homepage
            if homepage:
                homepage_clean = repo.homepage.replace("www.", "").replace("https://", "").replace("http://", "")
                if homepage_clean[-1] == "/":
                    homepage_clean = homepage_clean[:-1]
            else:
                homepage_clean = None

            formatted_name = repo.name.replace("-", " ").lower()

            description = repo.description
            if not description[-1] == "." and description[-1] not in ["!", "?"]:
                description += "."

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
                "homepage_clean": homepage_clean
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
        new_repos = sorted(self._repos, key=lambda x: x["created"], reverse=True)
        # sort by language
        new_repos = sorted(new_repos, key=lambda x: x["main_language"], reverse=False)

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
            del repo["created"]

        for lang in languages:
            languages_list.append({
                "language": lang,
                "absolute_size": languages[lang]["absolute_size"]
            })

        for lang in languages_list:
            lang["relative_size"] = lang["absolute_size"] / total_size
            lang["relative_size_formatted"] = f"{round(lang['relative_size'] * 100, 2)}%"

        languages_list = sorted(languages_list, key=lambda x: x["absolute_size"], reverse=True)
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

    def saveData(self):
        with open(self.settings["json_file"], "w") as json_file:
            ujson.dump(self._repos, json_file, indent=2, sort_keys=True)
        logging.info("Repos saved")

        with open(self.settings["html_file"], "w") as html_file:
            html_file.write(self._table)

    def formatTable(self):
        self._table = ""

        languages = sorted(list(set(x["main_language"] for x in self._repos["repos"])))
        for language in languages:
            selected_repos = [x for x in self._repos["repos"] if x["main_language"] == language]

            if len(selected_repos) == 0:
                continue

            count = 0
            for repo in selected_repos:
                if count == 0:
                    self._table += f"<tr><td class=\"italic language\">{language}</td>"
                else:
                    self._table += f"<tr><td class=\"italic language\"></td>"

                self._table += f"<td class=\"repo\"><a href=\"{repo['url']}\">{repo['formatted_name']}</a></td>"
                self._table += f"<td class=\"description opaque\">{repo['description']}"

                if repo["homepage"]:
                    self._table += f"<a class=\"pc homepage\" href=\"{repo['homepage']}\">Try it here!</a>"

                self._table += "</td></tr>\n"
                count += 1

            self._table += "<tr class=\"empty\"></tr>"

    def loadData(self):
        with open(self.settings["json_file"], "r") as json_file:
            self._repos = ujson.load(json_file)

        # sort by time
        self._repos["repos"] = sorted(self._repos["repos"], key=lambda x: datetime.fromisoformat(x["created_timestamp"]), reverse=True)
        # sort by language
        self._repos["repos"] = sorted(self._repos["repos"], key=lambda x: x["main_language"], reverse=False)


    @property
    def repos(self):
        self.loadData()
        return self._repos


def main():
    logfile = __file__.replace(".py", ".log")
    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode="w")
    print(f"Logging into {logfile}")
    s = Scraper()
    s.scrapeRepos()
    s.formatTable()
    s.saveData()


if __name__ == "__main__":
    main()
