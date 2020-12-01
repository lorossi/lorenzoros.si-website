/*jshint esversion: 6 */


function animate() {
  let duration = 1000;
  let bottom = $(document).scrollTop() + $(window).height();

  if (bottom <= $("#page1").outerHeight() * 1.5 && $("#logo").css("display") == "none") {

    setTimeout(() => {
      $("#logo").fadeIn(duration);
      $("#sketch").fadeIn(duration);
    }, 0);

    setTimeout(() => {
      $("#description").fadeIn(duration);
    }, duration / 2);

    setTimeout(() => {
      $(".navbar").fadeIn(duration);
    }, duration);
  }

  if (bottom > $("#page2").offset().top && $("#page2").css("display") == "none" && $("#logo").css("display") == "block") {
    setTimeout(() => {
      $("#page2").fadeIn(duration);
    }, duration / 2);
  }

  if (bottom > $("#page3").offset().top && $("#page3").css("display") == "none" && $("#page2").css("display") == "block") {
    setTimeout(() => {
      $("#page3").fadeIn(duration);
    }, duration / 2);
  }

}

$(document).ready(() => {
  $("#logo, #description, .navbar, #page2, #page3").css("display", "none");
  animate();
});


$(document).on("scroll", () => {
  animate();
});
