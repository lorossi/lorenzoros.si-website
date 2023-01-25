# lorenzoros.si-website

A repo containing all the code used in my [website](http://lorenzoros.si)

## Details

*Wow, where do I start?*

My website is created to be completely built on static `html.
Given how rarely it needs to be updated, I don't see the point in using a more complex (and expensive) hosting solution like a VPS or a cloud service.
Furthermore, I *really* like to code, so I developed a custom template engine (which ended up being like flask, but more on that later) to generate the html files.

I have also developed a simple markdown to html translator, which I am going to use to crate a blog section in the near future.

## Backend

All the needed scripts are written in Python and are located in the `python_scripts` folder.

### Template engine

Since I wanted a little bit of a challenge and I wanted to learn more about how template engines work, I decided to create my own.
It's not completely safe, but it works well enough for my needs (I don't plan on attacking my own website via XSS, do I? Furthermore, there's no SQL injection risk, since I don't use any database).

The engine parses the html files, reading line by line, and replacing the placeholders located between `{{` and `}}` with the values passed as `context` to the render method of the `Renderer` class.
Those value can be altered using any of the filters available in the `functions.py` file.
To make this process easier, a factory has been created.

The code between the `{%` and `%}` tags is executed as python code, and the output is inserted in the html file.
The supported statements are:

- `if`/`else`/`elif`: if the condition is true, the code between the `if` and `end`
- `for`: for each element in the iterable, the code between the `for` and `end` is executed

All the tokens are parsed via regular expression, and the code is executed using the `exec` function:
while I do agree that this is not the fanciest nor the best way to do it, it works well enough for my needs.
If I ever need to improve it, I will probably use a real parser like `lark` or I could even implement my own recursive descent parser.

I am still working on a formatting class for the rendered html.
So far I have tried:

- beautifulsoup: it works, but it messed up all the spacing in the html file, creating issue with the lists and the code blocks
- yattag: it gave up at the first inline `<script>`, rendering all the html invalid
- custom parser via regex: it kinda works, but it messes up like beautifulsoup does; I am quite confident that I can make something that works, but I am not sure if it's worth the effort

So far the class only throws a `NotImplementedError` while trying to format the html;
I am resorting to format via the VScode Prettify extension.

### Markdown to html translator

While at it, I also decided to create a markdown to html translator.

*Why, you ask?*

Well, mostly because I like writing. And I like coding.

Since studying Formal Languages, I have been eager to try out some of the things I learned in class.
So I tried to write a real parser in `lark` (which is a really nice library, by the way) using custom grammar;
despite my best efforts and a deep dive in google, I was not able to make it work.

I quickly realized that to parse a simple markdown structure all I needed was a few sets of regular expressions and a few lines of code.
What I then built is a simple two-sweep translator from markdown to html.

The first pass is used to split paragraphs, necessary to correctly parse the structure of the document, including all the newlines;
the second pass then parses the images, links, text styling, code blocks and lists.

The only thing that it's missing is table support (which honestly I don't really need, but I might add it in the future) and the support for nested lists (which I don't think would make a lot of sense, but it would be a nice challenge to implement).

The output can then be styled via a custom css file, which I am yet to create (I am not a designer, but I'm pretty sure that it's going to be the same as the one used in the main website).

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
)
One article could relate to the development of this website, giving me the opportunity to document and explain the code I wrote.

## Deployment

After generating the website, I manually upload it to the server via `sftp` using the `filezilla` client.
I plan on automating this task via a script so that I can build and deploy the website with a single command.

## License

The website is distributed under CC 4.0 License.

The logos are sourced from [icon blender](https://icon-blender.com/).
