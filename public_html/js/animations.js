/*jshint esversion: 6 */
let selectors = [".sketch", ".navbar", "#page1"];

function animate() {
  let duration = 2000;

  selectors.forEach((s, i) => {
    if ($(s).css("display") == "none") {
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
