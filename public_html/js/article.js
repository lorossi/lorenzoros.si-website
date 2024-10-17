document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("resize", window_resized);
  document.querySelectorAll("h1, h2, h3").forEach((e) => create_underline(e));
  document.querySelectorAll("pre").forEach((e) => fix_pre(e));
});

const create_underline = (e) => {
  const underline = document.createElement("div");
  underline.classList.add("underline");
  e.appendChild(underline);

  fix_underline(e);
};

const fix_underline = (e) => {
  const width = e.offsetWidth;
  console.log(width);

  const underline = e.querySelector(".underline");
  underline.style.width = `${width}px`;

  e.appendChild(underline);
};

const window_resized = () => {
  document.querySelectorAll("h1, h2, h3").forEach((e) => fix_underline(e));
};

const fix_pre = (e) => {
  const width = e.innerWidth;
  e.style.width = `${width}px`;
  e.style.display = "inline-block";
};
