// this script moves pages according to their final position
/*jshint esversion: 6 */


function placeElements() {
  sketch_selector = "#sketch"
  canvas_height = $("#page1").height() + $("#page2").height();
  canvas_width = $(window).width();

  $(sketch_selector).prop("width", canvas_width);
  $(sketch_selector).prop("height", canvas_height);
  $(sketch_selector).css({
    "width": canvas_width + "px",
    "height": canvas_height + "px"
  });
}

$(document).ready(function() {
  page_width = $(window).width();
  placeElements();
});

$(window).resize(function() {
  if ($(window).width() != page_width) {
    page_width = $(window).width();
    placeElements();
  }
});
