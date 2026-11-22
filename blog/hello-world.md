+++
title = "Hello, world"
date = 2026-10-26
description = "An example article, showing what the blog can render"
tags = ["meta", "example"]
draft = true # remove this line (or set it to false) to actually publish the article
+++

This is an **example** article. The file name (`hello-world.md`) becomes the url: `/blog/hello-world/`.

## Formatting

Articles are written in [Markdown](https://commonmark.org/), with a few extras:

- *italic*, **bold**, ~~strikethrough~~ and `inline code`
- "smart quotes" -- and dashes
- tables and raw HTML

> A quote, because every blog needs one.

```python
def hello() -> str:
    return "world"
```

| Language | Repos |
| -------- | ----: |
| Python   |    42 |
| C        |    17 |

Images and other files placed in the `blog/` folder are copied to `/blog/`, so `blog/img/photo.png` is shown with `![alt text](/blog/img/photo.png)`.

## Images and math

An image alone in its paragraph becomes a figure, with the alt text as caption:

![Me, looking at you](/assets/img/photo.png)

Formulas are written in LaTeX and pre-rendered to MathML at build time: inline like $e^{i\pi} + 1 = 0$, or as a block:

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$
