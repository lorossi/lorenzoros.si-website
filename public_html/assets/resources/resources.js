// this is my poor man's VPS. Might upgrade, one day.
// every resource you see in this file is generated by a Python script that I occasionally run.
// as such, not everything on my website might be up to date.
// You see, not wanting to spend for a proper VPS and using page templates, I inject the text inside the HTML DOM using JQuery.
// Does this make sense? No. Not at all. But I'm not willing to spend 10eur+ on a website that receives less than 10 visitors a month.
// As soon as I realize that this website is more useful than originally planned, I will consider an hardware update and make this whole part in backend with Flask. Or NodeJS. We'll see.

let resources = {
    "repos": [
        {
            "name": "DPCM-map",
            "formatted_name": "DPCM map",
            "description": null,
            "url": "https://github.com/valerionew/DPCM-map",
            "commits": 23,
            "stars": 0,
            "main_language": "C++",
            "languages": {
                "C++": 1949
            },
            "size": 4733,
            "last_pushed_timestamp": "2021-01-20T08:51:03",
            "created_timestamp": "2021-01-17T10:36:49",
            "created_year": 2021,
            "selected": false,
            "homepage": null
        },
        {
            "name": "fireflies-in-a-jar",
            "formatted_name": "fireflies in a jar",
            "description": "Gife life to a glass jar using some magic (and an Arduino)",
            "url": "https://github.com/lorossi/fireflies-in-a-jar",
            "commits": 14,
            "stars": 0,
            "main_language": "C++",
            "languages": {
                "C++": 6972
            },
            "size": 20,
            "last_pushed_timestamp": "2020-12-25T22:48:45",
            "created_timestamp": "2020-12-21T02:24:22",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "DWC-firmware",
            "formatted_name": "DWC firmware",
            "description": null,
            "url": "https://github.com/lorossi/DWC-firmware",
            "commits": 8,
            "stars": 0,
            "main_language": "C++",
            "languages": {
                "C++": 33821
            },
            "size": 18,
            "last_pushed_timestamp": "2021-01-18T16:05:12",
            "created_timestamp": "2020-12-16T17:02:20",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "empty-html5-project",
            "formatted_name": "empty html5 project",
            "description": "Empty HTML5 project",
            "url": "https://github.com/lorossi/empty-html5-project",
            "commits": 3,
            "stars": 0,
            "main_language": "HTML",
            "languages": {
                "HTML": 574,
                "JavaScript": 83,
                "CSS": 44
            },
            "size": 37,
            "last_pushed_timestamp": "2020-12-09T22:43:08",
            "created_timestamp": "2020-12-03T12:40:15",
            "created_year": 2020,
            "selected": false,
            "homepage": ""
        },
        {
            "name": "blank-p5js-project",
            "formatted_name": "blank p5js project",
            "description": null,
            "url": "https://github.com/lorossi/blank-p5js-project",
            "commits": 2,
            "stars": 0,
            "main_language": "HTML",
            "languages": {
                "HTML": 452,
                "JavaScript": 343,
                "CSS": 64
            },
            "size": 267,
            "last_pushed_timestamp": "2020-11-10T09:51:12",
            "created_timestamp": "2020-11-02T18:30:39",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "random-mondrian",
            "formatted_name": "random mondrian",
            "description": "Procedural generation of Mondrian-like paintings",
            "url": "https://github.com/lorossi/random-mondrian",
            "commits": 10,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 13162,
                "HTML": 1482,
                "CSS": 1266
            },
            "size": 112,
            "last_pushed_timestamp": "2021-01-23T17:29:19",
            "created_timestamp": "2021-01-23T16:11:41",
            "created_year": 2021,
            "selected": true,
            "homepage": "https://lorenzoros.si/random-mondrian/"
        },
        {
            "name": "vaccino-covid19",
            "formatted_name": "vaccino covid19",
            "description": "Controlla in tempo reale (o quasi) la distribuzione del vaccino contro il covid in Italia",
            "url": "https://github.com/lorossi/vaccino-covid19",
            "commits": 757,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 49641,
                "Python": 43512,
                "HTML": 16872,
                "CSS": 7118,
                "Shell": 58
            },
            "size": 2816,
            "last_pushed_timestamp": "2021-01-22T22:55:09",
            "created_timestamp": "2021-01-05T17:12:28",
            "created_year": 2021,
            "selected": true,
            "homepage": "https://www.vaccinocovid19.live"
        },
        {
            "name": "digital-spirograph",
            "formatted_name": "digital spirograph",
            "description": "My parents never bought me a spirograph when I was little... but now I can code.",
            "url": "https://github.com/lorossi/digital-spirograph",
            "commits": 10,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 35515,
                "HTML": 3124,
                "CSS": 1571
            },
            "size": 174,
            "last_pushed_timestamp": "2021-01-22T16:57:42",
            "created_timestamp": "2021-01-04T23:10:16",
            "created_year": 2021,
            "selected": true,
            "homepage": "https://lorenzoros.si/digital-spirograph/"
        },
        {
            "name": "empty-html5-canvas-project",
            "formatted_name": "empty html5 canvas project",
            "description": "Empty HTML5 project with JS canvas",
            "url": "https://github.com/lorossi/empty-html5-canvas-project",
            "commits": 1,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 1651,
                "HTML": 722,
                "CSS": 235
            },
            "size": 38,
            "last_pushed_timestamp": "2021-01-04T10:55:35",
            "created_timestamp": "2021-01-04T10:53:50",
            "created_year": 2021,
            "selected": false,
            "homepage": null
        },
        {
            "name": "painting-bubbles",
            "formatted_name": "painting bubbles",
            "description": "Feel like a painter without having to paint!",
            "url": "https://github.com/lorossi/painting-bubbles",
            "commits": 108,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 27383,
                "CSS": 2859,
                "Python": 2848,
                "HTML": 1439
            },
            "size": 2208964,
            "last_pushed_timestamp": "2021-01-23T16:17:35",
            "created_timestamp": "2020-12-03T12:44:19",
            "created_year": 2020,
            "selected": true,
            "homepage": "https://www.lorenzoros.si/painting-bubbles"
        },
        {
            "name": "js-vectors",
            "formatted_name": "js vectors",
            "description": "A simple 2D and 3D vectors library made in JS",
            "url": "https://github.com/lorossi/js-vectors",
            "commits": 20,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 12539
            },
            "size": 39,
            "last_pushed_timestamp": "2021-01-10T13:46:59",
            "created_timestamp": "2020-12-02T16:20:21",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "pi-montecarlo",
            "formatted_name": "pi montecarlo",
            "description": "Calculating PI by using Montecarlo method",
            "url": "https://github.com/lorossi/pi-montecarlo",
            "commits": 1,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 9500,
                "HTML": 577,
                "CSS": 235
            },
            "size": 3,
            "last_pushed_timestamp": "2020-11-30T18:28:13",
            "created_timestamp": "2020-11-30T18:28:07",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "p5js-perlin",
            "formatted_name": "p5js perlin",
            "description": "A suite of looping animations made with p5js and perlin noise",
            "url": "https://github.com/lorossi/p5js-perlin",
            "commits": 16,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 41416,
                "HTML": 1494,
                "CSS": 760
            },
            "size": 551315,
            "last_pushed_timestamp": "2020-12-08T18:20:16",
            "created_timestamp": "2020-11-17T17:11:05",
            "created_year": 2020,
            "selected": true,
            "homepage": "https://lorenzoros.si/p5js-perlin/"
        },
        {
            "name": "fireworks",
            "formatted_name": "fireworks",
            "description": "A fireworks spectacle made in p5js",
            "url": "https://github.com/lorossi/fireworks",
            "commits": 15,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 13805,
                "HTML": 690,
                "CSS": 496
            },
            "size": 343,
            "last_pushed_timestamp": "2020-12-02T16:51:56",
            "created_timestamp": "2020-10-20T12:20:02",
            "created_year": 2020,
            "selected": true,
            "homepage": "http://lorossi.github.io/fireworks"
        },
        {
            "name": "procedural-snowflakes",
            "formatted_name": "procedural snowflakes",
            "description": null,
            "url": "https://github.com/lorossi/procedural-snowflakes",
            "commits": 5,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 15801,
                "HTML": 609,
                "CSS": 71
            },
            "size": 305,
            "last_pushed_timestamp": "2020-10-15T21:24:08",
            "created_timestamp": "2020-10-13T20:23:11",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "merrychristmas",
            "formatted_name": "merrychristmas",
            "description": "Ho ho ho, merry Christmas!",
            "url": "https://github.com/lorossi/merrychristmas",
            "commits": 20,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 8536,
                "CSS": 1994,
                "HTML": 1861
            },
            "size": 6671,
            "last_pushed_timestamp": "2020-10-19T18:56:42",
            "created_timestamp": "2020-10-13T10:10:50",
            "created_year": 2020,
            "selected": false,
            "homepage": "https://lorossi.github.io/merrychristmas/"
        },
        {
            "name": "quantomancaanatale",
            "formatted_name": "quantomancaanatale",
            "description": "Ce lo siamo chiesti tutti, quanto manca a Natale?",
            "url": "https://github.com/lorossi/quantomancaanatale",
            "commits": 16,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 4309,
                "HTML": 1418,
                "CSS": 1080
            },
            "size": 254,
            "last_pushed_timestamp": "2020-10-20T12:19:39",
            "created_timestamp": "2020-10-12T16:02:58",
            "created_year": 2020,
            "selected": false,
            "homepage": "https://lorossi.github.io/quantomancaanatale/"
        },
        {
            "name": "hexapong",
            "formatted_name": "hexapong",
            "description": "A simple two player games featuring a modern version of Pong",
            "url": "https://github.com/lorossi/hexapong",
            "commits": 37,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 18941,
                "HTML": 923,
                "CSS": 350
            },
            "size": 438,
            "last_pushed_timestamp": "2020-11-02T15:25:06",
            "created_timestamp": "2020-10-07T19:51:53",
            "created_year": 2020,
            "selected": false,
            "homepage": "https://lorossi.github.io/hexapong/"
        },
        {
            "name": "lorenzoros.si-website",
            "formatted_name": "lorenzoros.si website",
            "description": "A repo for my website - lorenzoros.si",
            "url": "https://github.com/lorossi/lorenzoros.si-website",
            "commits": 161,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 41575,
                "HTML": 5976,
                "CSS": 5427,
                "Python": 5351
            },
            "size": 4301,
            "last_pushed_timestamp": "2021-01-23T18:03:41",
            "created_timestamp": "2020-07-08T16:22:03",
            "created_year": 2020,
            "selected": false,
            "homepage": "https://lorenzoros.si/"
        },
        {
            "name": "email-hide",
            "formatted_name": "email hide",
            "description": "A clever way to hide emails inside html web pages using client side JavaScript",
            "url": "https://github.com/lorossi/email-hide",
            "commits": 32,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 7892,
                "HTML": 6965,
                "CSS": 2377
            },
            "size": 409,
            "last_pushed_timestamp": "2020-12-08T14:33:29",
            "created_timestamp": "2020-07-04T17:55:23",
            "created_year": 2020,
            "selected": true,
            "homepage": "https://lorossi.github.io/email-hide/"
        },
        {
            "name": "lissajous",
            "formatted_name": "lissajous",
            "description": "Lissajous curves generator in Processing",
            "url": "https://github.com/lorossi/lissajous",
            "commits": 18,
            "stars": 0,
            "main_language": "Processing",
            "languages": {
                "Processing": 11254
            },
            "size": 44638,
            "last_pushed_timestamp": "2020-09-07T18:57:49",
            "created_timestamp": "2020-07-16T21:27:05",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "pi-day-2020-visualization",
            "formatted_name": "pi day 2020 visualization",
            "description": "A simple yet fascinating way of visualizing the first million digits of PI",
            "url": "https://github.com/lorossi/pi-day-2020-visualization",
            "commits": 8,
            "stars": 0,
            "main_language": "Processing",
            "languages": {
                "Processing": 5854
            },
            "size": 151877,
            "last_pushed_timestamp": "2020-03-14T16:38:50",
            "created_timestamp": "2020-03-14T16:06:55",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "perlin-flow-field",
            "formatted_name": "perlin flow field",
            "description": "My personal implementation of a perlin flow field in Processing 3",
            "url": "https://github.com/lorossi/perlin-flow-field",
            "commits": 7,
            "stars": 0,
            "main_language": "Processing",
            "languages": {
                "Processing": 6179
            },
            "size": 2948,
            "last_pushed_timestamp": "2020-03-01T16:30:19",
            "created_timestamp": "2020-03-01T16:09:42",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "breathing-city",
            "formatted_name": "breathing city",
            "description": "Visualizing a day in Milan by the bike sharing usage",
            "url": "https://github.com/lorossi/breathing-city",
            "commits": 6,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 23512
            },
            "size": 197,
            "last_pushed_timestamp": "2020-12-27T16:39:07",
            "created_timestamp": "2020-12-27T16:32:23",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "iot-stack",
            "formatted_name": "iot stack",
            "description": null,
            "url": "https://github.com/lorossi/iot-stack",
            "commits": 14,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 53070,
                "C++": 9395,
                "Shell": 176
            },
            "size": 39,
            "last_pushed_timestamp": "2021-01-21T11:19:24",
            "created_timestamp": "2020-12-26T18:30:40",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "minimalistic-maps",
            "formatted_name": "minimalistic maps",
            "description": "Famous cities like you've never seen before!",
            "url": "https://github.com/lorossi/minimalistic-maps",
            "commits": 28,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 12242
            },
            "size": 216,
            "last_pushed_timestamp": "2020-12-27T17:59:44",
            "created_timestamp": "2020-12-14T14:48:14",
            "created_year": 2020,
            "selected": false,
            "homepage": ""
        },
        {
            "name": "perlin-italy-map",
            "formatted_name": "perlin italy map",
            "description": "A moving animation of Italy in all of its geological beauty",
            "url": "https://github.com/lorossi/perlin-italy-map",
            "commits": 32,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 16650
            },
            "size": 158941,
            "last_pushed_timestamp": "2021-01-09T18:49:15",
            "created_timestamp": "2020-12-12T18:03:06",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "every-color",
            "formatted_name": "every color",
            "description": "A Python script generating images with all the RGB colors in a set bit depth.",
            "url": "https://github.com/lorossi/every-color",
            "commits": 92,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 21775
            },
            "size": 229063,
            "last_pushed_timestamp": "2021-01-10T14:43:39",
            "created_timestamp": "2020-11-24T13:31:02",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "performances-monitor",
            "formatted_name": "performances monitor",
            "description": "Handy way to constantly check some hardware stats via browser",
            "url": "https://github.com/lorossi/performances-monitor",
            "commits": 52,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 14071,
                "CSS": 6416,
                "JavaScript": 6393,
                "HTML": 4856
            },
            "size": 663,
            "last_pushed_timestamp": "2020-12-06T12:49:55",
            "created_timestamp": "2020-11-18T15:24:37",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "just-memes-telegram",
            "formatted_name": "just memes telegram",
            "description": null,
            "url": "https://github.com/lorossi/just-memes-telegram",
            "commits": 1,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 536054
            },
            "size": 56,
            "last_pushed_timestamp": "2020-09-25T10:01:45",
            "created_timestamp": "2020-09-25T10:00:26",
            "created_year": 2020,
            "selected": false,
            "homepage": null
        },
        {
            "name": "bikemi-python-unofficial-api",
            "formatted_name": "bikemi python unofficial api",
            "description": "An unofficial Python API for BikeMi",
            "url": "https://github.com/lorossi/bikemi-python-unofficial-api",
            "commits": 26,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 14029
            },
            "size": 65,
            "last_pushed_timestamp": "2020-12-27T13:10:43",
            "created_timestamp": "2020-07-13T11:59:30",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "rpi-homepage",
            "formatted_name": "rpi homepage",
            "description": "A flask based dashboard for my Raspberry Pi",
            "url": "https://github.com/lorossi/rpi-homepage",
            "commits": 18,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 9761,
                "CSS": 3155,
                "JavaScript": 2874,
                "HTML": 2054
            },
            "size": 776,
            "last_pushed_timestamp": "2020-12-08T13:42:50",
            "created_timestamp": "2020-07-11T16:18:11",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "zero-width-steganography",
            "formatted_name": "zero width steganography",
            "description": "Hide text informations using invisible text characters",
            "url": "https://github.com/lorossi/zero-width-steganography",
            "commits": 31,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 27902
            },
            "size": 67,
            "last_pushed_timestamp": "2020-07-09T15:01:32",
            "created_timestamp": "2020-06-17T09:29:12",
            "created_year": 2020,
            "selected": true,
            "homepage": ""
        },
        {
            "name": "corgos-telegram-bot",
            "formatted_name": "corgos telegram bot",
            "description": "Free delivery of cute corgis images",
            "url": "https://github.com/lorossi/corgos-telegram-bot",
            "commits": 15,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 22775
            },
            "size": 82,
            "last_pushed_timestamp": "2020-12-08T14:50:50",
            "created_timestamp": "2020-06-05T13:11:52",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "formulario-campi-elettromagnetici",
            "formatted_name": "formulario campi elettromagnetici",
            "description": "Formulario del corso di Campi Elettromagetici - Ing. Elettronica - AA 2019/2020",
            "url": "https://github.com/lorossi/formulario-campi-elettromagnetici",
            "commits": 36,
            "stars": 1,
            "main_language": "TeX",
            "languages": {
                "TeX": 52051
            },
            "size": 3769,
            "last_pushed_timestamp": "2020-10-24T16:53:52",
            "created_timestamp": "2020-03-23T16:55:33",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        },
        {
            "name": "appunti-vhdl",
            "formatted_name": "appunti vhdl",
            "description": "Appunti di VHDL",
            "url": "https://github.com/lorossi/appunti-vhdl",
            "commits": 12,
            "stars": 3,
            "main_language": "TeX",
            "languages": {
                "TeX": 36613
            },
            "size": 1955,
            "last_pushed_timestamp": "2020-02-24T11:55:50",
            "created_timestamp": "2020-01-16T20:16:27",
            "created_year": 2020,
            "selected": true,
            "homepage": null
        }
    ],
    "languages": [
        {
            "language": "Python",
            "absolute_size": 803552,
            "relative_size": 0.5878907464595318,
            "relative_size_formatted": "58.79%"
        },
        {
            "language": "JavaScript",
            "absolute_size": 311359,
            "relative_size": 0.22779493415098634,
            "relative_size_formatted": "22.78%"
        },
        {
            "language": "TeX",
            "absolute_size": 88664,
            "relative_size": 0.06486791787474604,
            "relative_size_formatted": "6.49%"
        },
        {
            "language": "C++",
            "absolute_size": 52137,
            "relative_size": 0.0381442144978304,
            "relative_size_formatted": "3.81%"
        },
        {
            "language": "HTML",
            "absolute_size": 52088,
            "relative_size": 0.03810836535978268,
            "relative_size_formatted": "3.81%"
        },
        {
            "language": "CSS",
            "absolute_size": 35518,
            "relative_size": 0.025985503779157603,
            "relative_size_formatted": "2.6%"
        },
        {
            "language": "Processing",
            "absolute_size": 23287,
            "relative_size": 0.017037119953410753,
            "relative_size_formatted": "1.7%"
        },
        {
            "language": "Shell",
            "absolute_size": 234,
            "relative_size": 0.00017119792455439156,
            "relative_size_formatted": "0.02%"
        }
    ],
    "stats": {
        "total_size": 1366839,
        "total_commits": 1655,
        "total_stars": 4,
        "total_languages": 8,
        "total_repos": 36,
        "last_updated": "2021-01-23T19:14:20.452877"
    }
};