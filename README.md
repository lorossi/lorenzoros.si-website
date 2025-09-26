# lorenzoros.si-website

A repo containing all the code used in my [website](http://lorenzoros.si)

## Details

*Wow, where do I start?*

My website is created to be completely built on static html5.
Given how rarely it needs to be updated, I don't see the point in using a more complex (and expensive) hosting solution like a VPS or a cloud service.
Furthermore, I *really* like to code, so I developed a custom template engine (which ended up being like flask, but more on that later) to generate the html files.

I have also developed a simple markdown to html translator, which I am going to use to crate a blog section in the near future.

## Backend

All the needed scripts are written in Python and are located in the `python_scripts` folder.

### Template engine

While previously I used a custom template engine, I later switched to using `jinja2`'s sandboxed environment, which is way more robust and secure.

## Frontend

The whole website is just a static page with a few javascript functions to create the animations, the typer effect and the contact links.

I made it all without using any framework, just by using html and css styling.
I tested the website on multiple browsers with different screen sizes and it seems to scale well.
It might have some issues on really small desktop screens, but I am not too worried about that since most of the traffic comes from mobile devices.

### Contact hiding

Since I didn't really want to put my Telegram nickname, my email and my curriculum out there in the wild, I used a [small script of mine](https://lorossi.github.io/email-hide/) to make it less obvious for spambots.
I think it's working well enough, because since creating it (a few years ago) I am yet to receive a single spam mail.

The only downside is that those fields don't work if javascript is disabled;
however, nobody but TOR users disable javascript, so I am not too worried.

A workaround would be setting it as an image, but it would make the image not-selectable and non-clickable, which is not ideal.
Another solution would be writing the email from right to left, and later setting the CSS `direction` property to `rtl`;
this would make the email readable, but not copyable, which is not ideal either.

## Blog

I am currently working on a blog section, which will be created using the markdown translator.
I plan on writing some articles about my projects, my studies and my life in general.
I also like to write some short stories (sadly, in Italian only).

One article could relate to the development of this website, giving me the opportunity to document and explain the code I wrote.

## Deployment

After generating the website, I manually upload it to the server via `sftp` using the `filezilla` client.
I plan on automating this task via a script so that I can build and deploy the website with a single command.

## License

The website is distributed under the [MIT license](LICENSE).

The logos are sourced from [icon blender](https://icon-blender.com/).
