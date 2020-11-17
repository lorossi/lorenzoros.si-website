// this script moves pages according to their final position
let page_width;

function placeElements() {
  let page_selector = "page";
  let sketch_selector = "sketch";
  let pages = $(`.${page_selector}`).length;

  for (let i = 0; i < pages; i++) {
    let y = 0;
    let h = 0;

    for (let j = 0; j < i; j++) {
      y += $(`#${page_selector}${j+1}`).height();
    }
    h = $(`#${page_selector}${i+1}`).height();

    $(`#${sketch_selector}${i+1}`).css("height", h + "px");
    $(`#${sketch_selector}${i+1}`).css("top", y + "px");
    $(`#${page_selector}${i+1}`).css("top", y + "px");
  }
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
