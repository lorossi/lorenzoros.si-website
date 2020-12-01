// this script moves pages according to their final position
/*jshint esversion: 6 */

let page_width;
let canvas_scl;
canvas_scl = 1;

function placeElements() {
  let page_selector = "page";
  let sketch_selector = "#sketch1";

  let pages = $(`.${page_selector}`).length;
  let pages_height = Array(pages).fill(0);

  for (let i = 0; i < pages; i++) {
    let y = 0;
    let h = 0;

    for (let j = 0; j < i; j++) {
      y += $(`#${page_selector}${j+1}`).height();
    }
    h = $(`#${page_selector}${i+1}`).height();
    pages_height[i] = h;
    $(`#${page_selector}${i+1}`).css("top", y + "px");
  }

  canvas_height = pages_height[0] + pages_height[1];
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
