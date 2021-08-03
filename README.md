# lorenzoros.si-website

A repo containing all the code used in my website

## Details

Wow, where do I start?

My website is created to be completely built on static html, mostly because I still haven't figured out how to correctly configure an email server.
As soon as I figure that out, I will move to a vps. *Why are you telling me this?* I hear you asking.

Well, to create the list of repos that I want to be seen on my website, I run a script (inside the `python_scripts`) folder that manually scrapes my GitHub profile (using the beautifully documented Python API) and creates 2 output files: one for the list of interactive projects, and one for the list of "featured" repos. I then manually copy the output and paste it into the `index.html` file.

**This does not make a lot of sense** but given how rarely I update it, it is still quite a reasonable use case. As soon as I am able to ditch the simple web hosting and move to a more suitable VPN, I will convert this manual labor into a more automated task (using, for example Flask. This choice would make sense since it's already written in Python).]

The script also generates a JSON file containing some useful informations as well (like the distribution of code languages and total stars/forks/commits).

Since I didn't really want to put my Telegram nickname/email/curriculum out there in the wild, I used a [small script of mine](https://lorossi.github.io/email-hide/) to make it less obvious for spambots. I think it's working well enough, because in more than a year I am yet to receive a single spam mail.

This small part aside, the website works 100% even with Javascript not enabled. But let's be serious, who isn't using Javascript in 2021?

## License

The website is distributed under CC 4.0 License.

The logos are sourced from [icon blender](https://icon-blender.com/).
