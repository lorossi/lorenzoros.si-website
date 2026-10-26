document.addEventListener("DOMContentLoaded", () => {
  main();
});

const LINES_COUNT = 500;
const LINE_MAX_OPACITY = 0.5;

const main = async () => {
  // evil console manipulation!
  console.clear();
  console.log(
    "%c Curious? Check the repo! https://github.com/lorossi/lorenzoros.si-website",
    "font-size: 1rem;"
  );

  const reduced_motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!reduced_motion.matches) start_lines();

  await print_letters();
};

const start_lines = () => {
  // the canvas covers the viewport; each line has a fixed position relative
  // to the whole page, and only the visible ones are drawn
  const canvas = document.querySelector(".animations-container");
  const ctx = canvas.getContext("2d");
  const color = getComputedStyle(document.documentElement)
    .getPropertyValue("--line-color")
    .trim();

  const lines = Array.from({ length: LINES_COUNT }, () => ({
    position: Math.random(), // fraction of the page height
    duration: random_between(200, 500), // ms
    delay: random_between(0, 2000), // ms
  }));

  const resize = () => {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.floor(window.innerWidth * dpr);
    canvas.height = Math.floor(window.innerHeight * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  window.addEventListener("resize", resize);
  resize();

  const draw = (time) => {
    const page_height = document.documentElement.scrollHeight;
    const line_height = window.innerWidth >= 770 ? 2 : 5;

    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
    ctx.fillStyle = color;

    for (const line of lines) {
      const y = Math.floor(line.position * page_height) - window.scrollY;
      if (y < -line_height || y > window.innerHeight) continue;

      const opacity = line_opacity(line, time);
      if (opacity <= 0) continue;

      ctx.globalAlpha = opacity;
      ctx.fillRect(0, y, window.innerWidth, line_height);
    }

    requestAnimationFrame(draw);
  };
  requestAnimationFrame(draw);
};

const line_opacity = (line, time) => {
  // fade from max opacity to 0 and back (alternate, ease-in-out), after a delay
  const t = (time - line.delay) / line.duration;
  if (t < 0) return 0;

  const cycle = Math.floor(t);
  const progress = cycle % 2 === 0 ? t - cycle : 1 - (t - cycle);
  const eased = 0.5 - 0.5 * Math.cos(Math.PI * progress);
  return LINE_MAX_OPACITY * (1 - eased);
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
  const separator = container.dataset.separator || "|";
  const to_write = [...container.dataset.text.replaceAll(separator, "\n")];

  let current_p = add_paragraph(container);
  await timeout(start_pause);

  for (const char of to_write) {
    if (char === "\n") {
      await timeout(newline_pause);
      remove_cursor(current_p);
      current_p = add_paragraph(container);
    } else {
      current_p.textContent += char;
      await timeout(typing_pause);
    }
  }
};

const timeout = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const random_between = (a, b) => Math.random() * (b - a) + a;
