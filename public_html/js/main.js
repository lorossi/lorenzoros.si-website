document.addEventListener("DOMContentLoaded", () => {
  main();
});

const main = async () => {
  console.clear();
  console.log(
    "%c Curious? Check the repo! https://github.com/lorossi/lorenzoros.si-website",
    "font-size: 1rem;"
  );
  window.addEventListener("resize", window_resized);
  add_lines();
  await print_letters();
};

const window_resized = () => {
  resize_animation_container();
  move_lines();
};

const get_page_height = () => {
  return [...document.querySelectorAll("body > *")]
    .filter((e) => !e.classList.contains("animations-container"))
    .filter((e) => e.scrollHeight != undefined)
    .reduce((acc, e) => acc + e.scrollHeight, 0);
};

const resize_animation_container = () => {
  const container = document.querySelector(".animations-container");
  container.style.height = `${get_page_height()}px`;
  return container;
};

const move_lines = () => {
  const page_height = get_page_height();
  document.querySelectorAll(".line").forEach((l) => {
    const percent = l.getAttribute("percent");
    const pos = Math.floor(percent * 0.01 * page_height);
    l.style.top = `${pos}px`;
  });
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
    const percent = Math.random() * 100;
    const position = Math.floor(percent * 0.01 * page_height);

    line.style.top = `${position}px`;
    line.style.animationDuration = `${Math.random() * 0.3 + 0.2}s`;
    line.style.animationDelay = `${Math.random() * 2}s`;
    line.setAttribute("percent", percent);
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
  const start_pause = 500;

  const container = document.querySelector(".typer");

  const line_separator = container.getAttribute("separator") || "|";

  let to_write = container
    .getAttribute("data-text")
    .replaceAll(line_separator, "\n")
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
const random_between = (a, b) => Math.random() * (b - a) + a;
