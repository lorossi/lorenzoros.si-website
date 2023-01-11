document.addEventListener("DOMContentLoaded", async () => {
  console.clear();
  console.log(
    "%c Curious? Check the repo! https://github.com/lorossi/lorenzoros.si-website",
    "font-size: 1rem;"
  );
  window.addEventListener("resize", resize_animation_container);
  add_lines();
  await print_letters();
});

const get_page_height = () => {
  // get the full page height without considering the animation container
  return [".navbar", ".container"]
    .map((s) => document.querySelector(s))
    .reduce((acc, e) => acc + e.scrollHeight, 0);
};

const resize_animation_container = () => {
  const container = document.querySelector(".animations-container");
  container.style.height = `${get_page_height()}px`;
  return container;
};

const add_lines = () => {
  // select the animations container
  const container = resize_animation_container();
  const page_height = get_page_height();

  // loop to create the lines
  for (let i = 0; i < 500; i++) {
    const line = document.createElement("div");
    line.classList.add("line");
    // random position
    line.style.top = `${Math.random() * page_height}px`;
    line.style.animationDuration = `${Math.random() * 0.3 + 0.2}s`;
    line.style.animationDelay = `${Math.random() * 2}s`;
    // add to container
    container.appendChild(line);
  }
};

const add_paragraph = (container) => {
  const p = document.createElement("p");
  p.classList.add("writing");
  container.appendChild(p);
  return p;
};

const remove_cursor = (p) => p.classList.remove("writing");

const print_letters = async () => {
  const typing_pause = 30;
  const newline_pause = 500;
  const start_pause = 250;

  const container = document.querySelector(".typer");
  let to_write = container
    .getAttribute("data-text")
    .replaceAll("<br>", "\n")
    .split("");
  let current_p = add_paragraph(container);

  await timeout(start_pause);

  while (to_write.length > 0) {
    const current_char = to_write.shift();

    if (current_char == "\n") {
      await timeout(newline_pause);
      remove_cursor(current_p);
      current_p = add_paragraph(container);
    } else {
      current_p.innerHTML += current_char;
      await timeout(typing_pause);
    }
  }
};

const timeout = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
