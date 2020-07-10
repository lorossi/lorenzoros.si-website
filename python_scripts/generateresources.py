import json
from github import Github

# Calculates hue of an rbg color. Inputs a string like #FFFFFF
def calculateHue(color):
    r = int(color[1:3], 16) / 255
    g = int(color[3:5], 16) / 255
    b = int(color[5:7], 16) / 255

    minval = min(r, g, b)
    maxval = max(r, g, b)
    if (r > g and r > b):
        # red is max
        hue = (g - b) / (maxval - minval)
    elif (g > r and g > b):
        # green is max
        hue = 2 + (b - r) / (maxval - minval)
    elif (b > r and b > g):
        # blue is max
        hue = 4 + (r - g) / (maxval - minval)
    else:
        hue = 0

    hue *= 60;
    if (hue < 0): hue += 360

    return hue

# Calculate brightness of a color
def averageColor(colors):
    r = [int(c[1:3], 16) for c in colors]
    g = [int(c[3:5], 16) for c in colors]
    b = [int(c[5:7], 16) for c in colors]

    average = []
    average.append((r[0] + r[1]) / 2)
    average.append((g[0] + g[1]) / 2)
    average.append((b[0] + b[1]) / 2)

    brightness = (0.2126 * average[0] + 0.7152 * average[1] + 0.0722 * average[2])
    return brightness

# Load settings from path
def loadSettings(path="settings.json"):
    path = "settings.json"
    with open(path) as json_file:
        settings = json.load(json_file)
    return settings


def saveToFile(combinations, strings, repos, path):
    newl = "\n"
    tab = "    "
    output_string = ""

    output_string = "var colors = ["
    for c in combinations:
        line = str(c)
        # convert to js notation
        line = line.replace("(", "[")
        line = line.replace(")", "]")
        line = line.replace("True", "true")
        line = line.replace("False", "false")
        output_string += f"{newl}{tab}{line},"

    # we remove last comma
    output_string = output_string[:-1]
    output_string += f"{newl}];{newl}{newl}"

    output_string += "var strings = ["
    for s in strings:
        line = str(s)
        output_string += f"{newl}{tab}'{line}',"

    output_string = output_string[:-1]
    output_string += f"{newl}];{newl}{newl}"

    output_string += "var repos = ["
    for r in repos:
        line = str(r)
        line = line.replace("None", "null")
        output_string += f"{newl}{tab}{line},"

    output_string = output_string[:-1]
    output_string += f"{newl}];"

    output_file = open(path,"w+")
    output_file.write(output_string)
    output_file.close()
    return


settings = loadSettings()
colors = settings["colors"]
min_angle = settings["min_angle"]
max_angle = settings["max_angle"]
threshold_brightness = settings["threshold_brightness"]
strings = settings["strings"]
output_file = settings["output_file"]
github_credentials = settings["GitHub"]

# list that will hold every color combination
colors_combinations = []

# loop through colors
for c1 in colors:
    # keep track of original list of colrs
    colors_copy = [c for c in colors]

    # calculate the hue of the first color
    c1_hue = calculateHue(c1)

    # loop through colors again
    for c2 in colors_copy:
        if c1 == c2:
            continue

        c2_hue = calculateHue(c2)
        angle_between = abs(c2_hue - c1_hue)
        if angle_between > min_angle and angle_between < max_angle:
            # the two colors are not too far (they are not complementary)
            brightness = averageColor([c1, c2])
            # we want to know if the gradient is "dark" or "light"
            bright = brightness > threshold_brightness

            # we check if the couple hasn't been checked already
            if not (c2, c1, bright) in colors_combinations:
                colors_combinations.append((c1, c2, bright))

repos = []
g = Github(github_credentials["username"], github_credentials["password"])

for repo in g.get_user().get_repos():
    if any(word in repo.name for word in github_credentials["skip_names"]):
        continue

    if any(url in repo.html_url for url in github_credentials["skip_urls"]):
        continue

    if not repo.language:
        language = ""
    else:
        language = repo.language

    repos.append({
        "name": repo.name,
        "url": repo.html_url,
        "commits": repo.get_commits().totalCount,
        "language": language
    })

repos = sorted(repos, key=lambda d: d['commits'], reverse=True)

saveToFile(colors_combinations, strings, repos, output_file)
