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

  // highlight projects when mouse is over them
  $(".projectscontainer .opaque").mouseenter((e) => {
    let nodes = [];
    if ($(e.target).prop('nodeName') === "A") {
      nodes.push($(e.target).parent("td").toArray()[0]);
      nodes.push($(e.target).parent("td").siblings(".opaque").toArray()[0]);
    } else {
      nodes.push($(e.target));
      nodes.push($(e.target).siblings(".opaque").toArray()[0]);
    }

    nodes.forEach((n, i) => {
      if ($(n).hasClass("opaque")) {
        $(n).removeClass("opaque");
        $(n).addClass("bright");
      }
    });
  });

  $(document).on("mouseleave", ".bright", (e) => {
    let nodes = $(".bright").toArray();
    nodes.forEach((n, i) => {
      $(n).removeClass("bright");
      $(n).addClass("opaque");
    });
  });
});
