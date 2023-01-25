document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("h1, h2, h3").forEach((e) => create_underline(e));
  document.querySelectorAll("pre").forEach((e) => fix_pre(e));
});

const create_underline = (e) => {
  const underline = document.createElement("div");
  underline.classList.add("underline");

  const width = e.innerWidth;
  underline.style.width = `${width}px`;

  e.appendChild(underline);
};

const fix_pre = (e) => {
  const width = e.innerWidth;
  e.style.width = `${width}px`;
  e.style.display = "inline-block";
};
