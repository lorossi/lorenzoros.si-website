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
  // fade in animation
  selectors.forEach((s, i) => {
    $(s).css("display", "none");
  });
  // now actually fade in
  animate();

  // mouse enters the grid
  $(".projectscontainer tr *").mouseenter((e) => {
    if ($(e.target).hasClass("description")) {
      $(e.target).removeClass("opaque");
    } else {
      $(e.target).parent().siblings().toArray().forEach((p, i) => {
        if ($(p).hasClass("description")) {
          $(p).removeClass("opaque");
        }
      });
    }
  });

  // mouse leaves the grid
  $(".projectscontainer tr *").mouseleave((e) => {
    if ($(e.target).hasClass("description")) {
      $(e.target).addClass("opaque");
    } else {
      $(e.target).parent().siblings().toArray().forEach((p, i) => {
        if ($(p).hasClass("description")) {
          $(p).addClass("opaque");
        }
      });
    }
  });

});
