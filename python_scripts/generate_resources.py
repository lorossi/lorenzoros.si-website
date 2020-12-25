import json
import logging
from github import Github
from datetime import datetime


# Load settings from path
def loadSettings(path="settings.json"):
    path = "settings.json"
    with open(path) as json_file:
        settings = json.load(json_file)
    return settings


# load repos from Github
def loadRepos(g, skip_names=None, skip_urls=None, selected_repos=None):
    repos = []

    for repo in g.get_user().get_repos():
        if any(word in repo.name for word in skip_names):
            continue

        if any(url in repo.html_url for url in skip_urls):
            continue

        if not repo.language:
            continue

        language = repo.language
        selected = repo.name in selected_repos

        repos.append({
            "name": repo.name,
            "formatted_name": repo.name.replace("-", " "),
            "description": repo.description,
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
            "selected": selected
        })

    return repos


# format repos dict
def formatRepos(repos):
    return_dict = {}
    languages = {}
    languages_list = []
    total_commits = 0
    total_stars = 0
    total_size = 0

    # sort by language
    repos = sorted(repos, key=lambda x: x["main_language"], reverse=False)
    # sort by time
    repos = sorted(repos, key=lambda x: x["created"], reverse=True)

    for repo in repos:
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

    return_dict["repos"] = repos
    return_dict["languages"] = languages_list
    return_dict["stats"] = {
        "total_size": total_size,
        "total_commits": total_commits,
        "total_stars": total_stars,
        "total_languages": len(languages_list),
        "total_repos": len(repos),
        "last_updated": datetime.now().isoformat()
    }
    return return_dict


# save to file
def saveToFile(path, repos):
    newl = "\n"
    output_string = ""

    output_string += (
        f"// this is my poor man's VPS. Might upgrade, one day.{newl}"
        f"// every resource you see in this file is generated by a Python script that I occasionally run.{newl}"
        f"// as such, not everything on my website might be up to date.{newl}"
        f"// You see, not wanting to spend for a proper VPS and using page templates, I inject the text inside the HTML DOM using JQuery.{newl}"
        f"// Does this make sense? No. Not at all. But I'm not willing to spend 10eur+ on a website that receives less than 10 visitors a month.{newl}"
        f"// As soon as I realize that this website is more useful than originally planned, I will consider an hardware update and make this whole part in backend with Flask. Or NodeJS. We'll see."
        f"{newl}{newl}"
    )

    output_string += "let resources = "
    # convert dict to json (will be read by js)
    output_string += json.dumps(repos, indent=4)
    output_string += ";"

    output_file = open(path, "w+")
    output_file.write(output_string)
    output_file.close()


def main():
    logfile = __file__.replace(".py", ".log")
    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode="w")
    print(f"Logging into {logfile}")

    logging.info("started script")
    settings = loadSettings()
    logging.info("settings loaded")

    github_credential = settings["GitHub"]
    g = Github(github_credential["access_token"])
    logging.info("logged into Github")

    skip_names = github_credential["skip_names"]
    skip_urls = github_credential["skip_urls"]
    selected_repos = github_credential["selected_repos"]
    repos = loadRepos(g, skip_names, skip_urls, selected_repos)
    logging.info("repos loaded")

    repos = formatRepos(repos)
    logging.info("repos formatted")

    outpath = settings["output_file"]
    saveToFile(outpath, repos)
    logging.info("file saved")

    print("script ended")
    logging.info("script ended")


if __name__ == "__main__":
    main()
