# lorenzoros.si-website
A repo contanining all the code used in my website

## Details

### Scalability
I tested this website on multiple resolutions, screensizes and various devices. It works on PC, tablet and phones. The css for screen smaller than mine (a 15" FHD screen) is contained in *smallscreen.css* stylesheet.
This being said, the website was created to be viewed mostly on PC. As such, some features might look a little bit wonky on mobile.

### Colors
The website features both a colored and a black and white mode. The colors were carefully hand picked in order to make the text as legible as possible. Toggle between the two modes by clicking the text in the top right corner.

### GitHub scraping
The website features a coding tracker section. All the data is parsed by a script *(generateresources.py)* located inside the the *python_scripts* folder. That script is ran once a day, ad midnight (my timezone) and it's hosted on a RaspberryPi.
I don't actually have a VPS, otherwise I would have built this entire website in flask. I might consider doing so in the future.

### Email / Telegram Privacy
If you look at the html source, you won't find my email or telegram profile. That's because I used a custom script *(hide.js)* to inject an "encrypted" text inside their respective containers. By doing so, I prevent spambots from scraping my email.
You can look at its repo [here](https://github.com/lorossi/email-hide) or try it [here](https://lorossi.github.io/email-hide/)

# Visit it [lorenzoros.si](https://www.lorenzoros.si)

# License
The website is distributed under CC 4.0 License.

Through the website I used [Roboto font](https://fonts.google.com/specimen/Roboto) distribute under Apache 2.0 License.

The logos are sourced from [Simple-Icons](https://github.com/simple-icons/simple-icons).
