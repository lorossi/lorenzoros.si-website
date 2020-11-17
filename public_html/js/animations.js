$(document).ready(function() {
  let duration = 1000;

  if ($("#sketch1").visible(true)) {

    setTimeout(function() {
      $("#logo").fadeIn(duration);
    }, 250);
    setTimeout(function() {
      $("#description").fadeIn(duration);
    }, 500);
    setTimeout(function() {
      $(".navbar").fadeIn(duration, function() {
        $(".navbar").css("display", "flex");
      });
    }, 1000);

    setTimeout(function() {
      $("#portfolio").fadeIn(duration);
    }, 1500);
    setTimeout(function() {
      $(".projectscontainer").fadeIn(duration);
    }, 1750);
    setTimeout(function() {
      $(".morerepos").fadeIn(duration, placeElements);
    }, 2000);

    setTimeout(function() {
      $("#contacts").fadeIn(duration);
    }, 2500);
    setTimeout(function() {
      $(".contactscontainer").fadeIn(duration);
    }, 2750);
  }



})
