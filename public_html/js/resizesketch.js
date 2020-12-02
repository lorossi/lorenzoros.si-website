// this script moves pages according to their final position
/*jshint esversion: 6 */

let page_width = 0;

function placeElements() {
  sketch_selector = "#sketch";
  fade_selector = ".canvasfade";

  let canvas_height = $("#page1").height() + $("#page2").height() + $("#page3").height();
  let canvas_width = $(window).width();
  let fade_height = canvas_height / 4;

  $(sketch_selector).prop("width", canvas_width);
  $(sketch_selector).prop("height", canvas_height);
  $(sketch_selector).css({
    "width": canvas_width + "px",
    "height": canvas_height + "px"
  });

  $(fade_selector).css({
    "top": canvas_height - fade_height + "px",
    "height": fade_height + "px"
  });
}

$(document).ready(() => {
  page_width = $(window).width();
  placeElements();
});

$(window).resize(() => {
  if ($(window).width() != page_width) {
    page_width = $(window).width();
    placeElements();
  }
});
