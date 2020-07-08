function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function rotateBackground() {
  $("body").css({"backgroundImage": `linear-gradient(${angle}deg, ${gradient[0]}, ${gradient[1]})`});
  angle += 3.6;
}

function selectColors() {
  gradient = colors[Math.floor(Math.random() * colors.length)];
}

function setTextColor() {
  if (gradient[2]) {
    $("body").css({"color": "black"});
    $(".icons a").css({"filter": "invert(0%)"});
  } else {
    $("body").css({"color": "white"});
    $(".icons a").css({"filter": "invert(100%)"});
  }
}

function setSubtitle(selector) {
  shuffle(subtitles);
  if (subtitles[0] == $(selector).text()) {
    random_text = subtitles[1];
  } else {
    random_text = subtitles[0];
  }

  $(selector).text(random_text);
  $(selector).css({"visibility": "block"});
  $(selector).slideDown(300);
}

function moveOrbs(selector) {
  let easing = 0.01;
  $(selector + ' > div').each(function () {
    let x, y, dx, dy, nx, ny, epsilon;
    epsilon = $(this).css("width");
    epsilon = parseInt(epsilon.substring(0, epsilon.length - 2)) * 3;
    x = $(this).css("left");
    y = $(this).css("top");
    x = parseInt(x.substring(0, x.length - 2));
    y = parseInt(y.substring(0, y.length - 2));

    dx = mouse_coords.x - x;
    dy = mouse_coords.y - y;

    if (Math.abs(dx) < epsilon && Math.abs(dy) < epsilon) {
      r = Math.random() * (20 - 3) + 3;
      theta = Math.random() * 2 * Math.PI;
      x = (r * Math.cos(theta) + 1) * 100;
      y = (r * Math.sin(theta) + 1) * 100;
      $(this).css({"left": x + "vw", "top": y + "vh"});
    } else {
      x += dx * easing;
      y += dy * easing;
      $(this).css({"left": x + "px", "top": y + "px"});
    }
 });
}



var angle = 0;
var gradient = [];
var mouse_coords = {"x": 0, "y": 0};
var max_orbs = 100;

$(document).ready(function() {
  let subtitle_obj = ".title #subtitle";
  let icons_obj = ".icons a";
  let orbs_container_obj = ".orbs";

  selectColors();
  setTextColor();
  angle = Math.random() * 360;


  for (let i = 0; i < max_orbs; i++) {
    let r, theta, x, y;

    r = Math.random() * (20 - 3) + 3;
    theta = Math.random() * 2 * Math.PI;
    x = (r * Math.cos(theta) + 1) * 100;
    y = (r * Math.sin(theta) + 1) * 100;
    $("<div>", {
      "id": "orb",
      css: {
          "left": x,
          "top": y
      }
    }).appendTo(orbs_container_obj);
  }

  console.log("%c Curious about this website? Look at the repo here https://github.com/lorossi/lorenzoros.si-website", "font-size: 2rem");

  setTimeout(setSubtitle, 200, subtitle_obj);
  setInterval(setSubtitle, 1000 * 15, subtitle_obj);

  setInterval(rotateBackground, 100);
  setInterval(moveOrbs, 10, orbs_container_obj);

  $(icons_obj).mouseenter(function() {
    if (gradient[2]) {
      $(this).css({"filter": "invert(100%)"});
    } else {
      $(this).css({"filter": "invert(0%)"});
    }
  });

  $(icons_obj).mouseleave(function() {
    if (gradient[2]) {
      $(this).css({"filter": "invert(0%)"});
    } else {
      $(this).css({"filter": "invert(100%)"});
    }
  });

  $(subtitle_obj).click(
    function() {
      setSubtitle(subtitle_obj);
    }
  );

  $("body").mousemove(function(e) {
    mouse_coords.x = e.pageX;
    mouse_coords.y = e.pageY;
  })
})
