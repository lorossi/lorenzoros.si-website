/*jshint esversion: 6 */
let selectors = [".sketch", ".navbar", "#page1", "#page2", "#page3"];

function animate() {
  let duration = 1000;
  let bottom = $(document).scrollTop() + $(window).height();

  selectors.forEach((s, i) => {
    if (bottom >= $(s).offset().top && $(s).css("display") == "none") {
      $(s).fadeIn(duration);
    }
  });
}

$(document).ready(() => {
  selectors.forEach((s, i) => {
    $(s).css("display", "none");
  });

  animate();
});


$(document).on("scroll", () => {
  animate();
});
