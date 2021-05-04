# lorenzoros.si-website

A repo contanining all the code used in my website

## Details

### Responsivity

I tested this website on multiple resolutions, screen sizes and various devices. It works on PC, tablet and phones. The css for screen smaller than mine (a 15" FHD screen) is contained in *phonestyle.css* stylesheet.
This being said, the website was created to be viewed mostly on PC. As such, some features might look a little bit wonky on mobile.

### GitHub scraping

The website features a coding tracker section. All the data is parsed by a script *(generateresources.py)* located inside the the *python_scripts* folder. That script is ran once in a while. As such it might not always be updated.
I don't actually have a VPS, otherwise I would have built this entire website in flask and it would require less js nonsense. I might consider doing so in the future.

### Email / Telegram / links Privacy

If you look at the html source, you won't find my email or telegram profile. That's because I used a custom script *(secret.js)* to inject an "encrypted" text inside their respective containers. By doing so, I prevent spambots from scraping my email. *So far, I have yet to receive spam!*
You can look at its repo [here](https://github.com/lorossi/email-hide) or try it [here](https://lorossi.github.io/email-hide/)

### Double languages

This website is actually written in two languages (Italian and English). A js script automatically discovers the user's PC language and switches to the correct version.

### Background animation

The background animation is made in pure js using html5 canvas element. Previously it was made in p5js but it lagged heavily on most devices (including mobiles). Now it's lighter on your hardware!

## Visit it [lorenzoros.si](https://www.lorenzoros.si)

## Screenshots (OUTDATED)

## PC / Bigger screens

![page 1](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page1-pc.png?raw=true)
![page 2](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page2-pc.png?raw=true)
![page 3](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page3-pc.png?raw=true)

## Mobile

![page 1](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page1-mobile.png?raw=true)
![page 2](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page2-mobile.png?raw=true)
![page 3](https://github.com/lorossi/lorenzoros.si-website/blob/master/screenshots/page3-mobile.png?raw=true)

## What would I do differently?

I have learned *A LOT* since I finished this website. I'm kinda half-tempted to make a brand new website, but with a few things in mind:

1. Make use of the CSS variable in a more toughtful way
1. Scrap completely jQuery as it's pretty much useless in 2021, novadays vanilla js is good enough
1. Handle more cleverly the double language system (or just make everything in English)
1. Make use of the new css grid instead of the old tables
1. Be more toughtful about css selectors (my stylesheet is pretty garbled in some points)
1. Use monospaced font (like Hack) because I think it's a better fit for what I'm trying to convey
1. Design the website on paper BEFOREHAND instead of randomly trying a lot of styles (and then failing)
1. Design *MOBILE FIRST* so it's not a pain to port it
1. Add a photo of me (something a little bit creative, maybe) also to fill the last page (and because it would make a lot of sense)

I still don't have a VPS so dynamic updating and server-side generation won't be something feasible. I don't really need it since manually updating about once a month it's not a big deal.

## License

The website is distributed under CC 4.0 License.

The logos are sourced from [Simple-Icons](https://github.com/simple-icons/simple-icons).
