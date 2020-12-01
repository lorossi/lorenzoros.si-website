# lorenzoros.si-website
A repo contanining all the code used in my website

## Details

### Scalability
I tested this website on multiple resolutions, screen sizes and various devices. It works on PC, tablet and phones. The css for screen smaller than mine (a 15" FHD screen) is contained in *phonestyle.css* stylesheet.
This being said, the website was created to be viewed mostly on PC. As such, some features might look a little bit wonky on mobile.

### GitHub scraping
The website features a coding tracker section. All the data is parsed by a script *(generateresources.py)* located inside the the *python_scripts* folder. That script is ran once in a while. As such it might not always be updated.
I don't actually have a VPS, otherwise I would have built this entire website in flask and it would require less js nonsense. I might consider doing so in the future.

### Email / Telegram / links Privacy
If you look at the html source, you won't find my email or telegram profile. That's because I used a custom script *(secret.js)* to inject an "encrypted" text inside their respective containers. By doing so, I prevent spambots from scraping my email. *So far, I have yet to receive spam!*
You can look at its repo [here](https://github.com/lorossi/email-hide) or try it [here](https://lorossi.github.io/email-hide/)

# Visit it [lorenzoros.si](https://www.lorenzoros.si)

# License
The website is distributed under CC 4.0 License.

The logos are sourced from [Simple-Icons](https://github.com/simple-icons/simple-icons).

Thanks to [customd](https://github.com/customd) for his wonderful [jQuery isvisible plugin.](https://github.com/customd/jquery-visible)

Thanks to [josephg](https://github.com/josephg) for his marvelous (noisejs library.)[https://github.com/josephg/noisejs]
