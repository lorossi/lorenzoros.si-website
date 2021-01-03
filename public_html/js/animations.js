/*jshint esversion: 6 */

let selectors = [".sketch", "#logo", "#description", ".navbar"];

function animate() {
  // fade in animation
  selectors.forEach((s, i) => {
    $(s).css("display", "none");
  });

  let duration = 1000;
  selectors.forEach((s, i) => {
    if ($(s).css("display") == "none") {
      setTimeout(() => {
        $(s).fadeIn(duration);
      }, 250 * (i + 1));
    }
  });
}

$(document).ready(() => {
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
