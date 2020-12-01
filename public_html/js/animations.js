/*jshint esversion: 6 */


function animate() {
  let duration = 1000;
  let bottom = $(document).scrollTop() + $(window).height();

  if (bottom <= $("#page1").outerHeight() && $("#logo").css("display") == "none") {
    setTimeout(function() {
      $("#logo").fadeIn(duration);
    }, 0);

    setTimeout(function() {
      $("#description").fadeIn(duration);
    }, duration / 2);

    setTimeout(function() {
      $(".navbar").fadeIn(duration);
    }, duration);
  }

  if (bottom > $("#page2").offset().top && $("#portfolio").css("display") == "none") {
    setTimeout(function() {
      $("#portfolio").fadeIn(duration);
    }, 0);

    setTimeout(function() {
      $("#projectscontainer").fadeIn(duration);
    }, duration);

    setTimeout(function() {
      $(".morerepos").fadeIn(duration);
    }, duration * 2);
  }

  if (bottom > $("#page3").offset().top && $("#contacts").css("display") == "none") {
    setTimeout(function() {
      $("#contacts").fadeIn(duration);
    }, 0);

    setTimeout(function() {
      $(".contactscontainer").fadeIn(duration);
    }, duration);
  }

}

$(document).ready(() => {
  animate();
});


$(document).on("scroll", () => {
  animate();
});
