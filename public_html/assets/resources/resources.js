// this is my poor man's VPS. Might upgrade, one day.
// every resource you see in this file is generated by a Python script that I occasionally run.
// as such, not everything on my website might be up to date.
// You see, not wanting to spend for a proper VPS and using page templates, I inject the text inside the HTML DOM using JQuery.
// Does this make sense? No. Not at all. But I'm not willing to spend 10eur+ on a website that receives less than 10 visitors a month.
// As soon as I realize that this website is more useful than originally planned, I will consider an hardware update and make this whole part in backend with Flask. Or NodeJS. We'll see.

let resources = {
    "repos": [
        {
            "name": "minimalistic-maps",
            "formatted_name": "minimalistic maps",
            "description": null,
            "url": "https://github.com/lorossi/minimalistic-maps",
            "commits": 20,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 10337
            },
            "size": 202,
            "last_pushed_timestamp": "2020-12-14T22:06:06",
            "created_timestamp": "2020-12-14T14:48:14",
            "created_year": 2020,
            "selected": false
        },
        {
            "name": "perlin-italy-map",
            "formatted_name": "perlin italy map",
            "description": "A moving animation of Italy in all of its geological beauty",
            "url": "https://github.com/lorossi/perlin-italy-map",
            "commits": 27,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 15977
            },
            "size": 158842,
            "last_pushed_timestamp": "2020-12-14T10:50:02",
            "created_timestamp": "2020-12-12T18:03:06",
            "created_year": 2020,
            "selected": true
        },
        {
            "name": "painting-bubbles",
            "formatted_name": "painting bubbles",
            "description": "Feel like a painter without having to paint!",
            "url": "https://github.com/lorossi/painting-bubbles",
            "commits": 107,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 27383,
                "CSS": 2875,
                "Python": 2848,
                "HTML": 1439
            },
            "size": 2208964,
            "last_pushed_timestamp": "2020-12-10T22:29:15",
            "created_timestamp": "2020-12-03T12:44:19",
            "created_year": 2020,
            "selected": true
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
            "selected": false
        },
        {
            "name": "js-vectors",
            "formatted_name": "js vectors",
            "description": "A simple 2D and 3D vectors library made in JS",
            "url": "https://github.com/lorossi/js-vectors",
            "commits": 14,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 11455
            },
            "size": 25,
            "last_pushed_timestamp": "2020-12-08T14:17:24",
            "created_timestamp": "2020-12-02T16:20:21",
            "created_year": 2020,
            "selected": true
        },
        {
            "name": "every-color",
            "formatted_name": "every color",
            "description": "A Python script generating images with all the RGB colors in a set bit depth.",
            "url": "https://github.com/lorossi/every-color",
            "commits": 67,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 20375
            },
            "size": 169434,
            "last_pushed_timestamp": "2020-12-13T22:36:10",
            "created_timestamp": "2020-11-24T13:31:02",
            "created_year": 2020,
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": false
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
            "selected": false
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
            "selected": true
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
            "selected": true
        },
        {
            "name": "bikemi-python-unofficial-api",
            "formatted_name": "bikemi python unofficial api",
            "description": "An unofficial Python API for BikeMi",
            "url": "https://github.com/lorossi/bikemi-python-unofficial-api",
            "commits": 22,
            "stars": 0,
            "main_language": "Python",
            "languages": {
                "Python": 13383
            },
            "size": 53,
            "last_pushed_timestamp": "2020-12-08T15:00:19",
            "created_timestamp": "2020-07-13T11:59:30",
            "created_year": 2020,
            "selected": true
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
            "selected": true
        },
        {
            "name": "lorenzoros.si-website",
            "formatted_name": "lorenzoros.si website",
            "description": "A repo for my website - lorenzoros.si",
            "url": "https://github.com/lorossi/lorenzoros.si-website",
            "commits": 133,
            "stars": 0,
            "main_language": "JavaScript",
            "languages": {
                "JavaScript": 30803,
                "HTML": 6874,
                "Python": 5254,
                "CSS": 3976
            },
            "size": 4249,
            "last_pushed_timestamp": "2020-12-09T18:11:06",
            "created_timestamp": "2020-07-08T16:22:03",
            "created_year": 2020,
            "selected": false
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
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": true
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
            "selected": true
        }
    ],
    "languages": [
        {
            "language": "JavaScript",
            "absolute_size": 173890,
            "relative_size": 0.36137116969212063,
            "relative_size_formatted": "36.14%"
        },
        {
            "language": "Python",
            "absolute_size": 142683,
            "relative_size": 0.2965180436205696,
            "relative_size_formatted": "29.65%"
        },
        {
            "language": "TeX",
            "absolute_size": 88664,
            "relative_size": 0.18425794116730224,
            "relative_size_formatted": "18.43%"
        },
        {
            "language": "HTML",
            "absolute_size": 29148,
            "relative_size": 0.060574195492471866,
            "relative_size_formatted": "6.06%"
        },
        {
            "language": "CSS",
            "absolute_size": 23523,
            "relative_size": 0.04888454784442897,
            "relative_size_formatted": "4.89%"
        },
        {
            "language": "Processing",
            "absolute_size": 23287,
            "relative_size": 0.04839410218310664,
            "relative_size_formatted": "4.84%"
        }
    ],
    "stats": {
        "total_size": 481195,
        "total_commits": 726,
        "total_stars": 4,
        "total_languages": 6,
        "total_repos": 23,
        "last_updated": "2020-12-14T23:07:59.187667"
    }
}