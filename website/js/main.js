// shuffle an array and returns it
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// random float between values
function randomBetween(min = 0, max = 1) {
  return Math.random() * (max - min) + min;
}

// random int between values
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

// ritate background gradient
function rotateBackground() {
  $(".background").css({
    "background-image": `linear-gradient(${angle}deg, ${gradient.from}, ${gradient.to})`
  });
  angle += 3.6; // global variable
}

// select colors from list
function selectColors() {
  gradient = colors[Math.floor(Math.random() * colors.length)]; // global variable
}

function setTextColor(icons_obj, background_obj, color_switch_obj, color_mode) {
  if (color_mode) { // everything is colored
    if (gradient.bright) {
      $("body").css({
        "color": dark_color, // dark
        "filter": ""
      });

      $(icons_obj).each(function() {
        $(this).css({
          "filter": dark_filter
        });
      });

      $(color_switch_obj).css({
        "filter": ""
      });

    } else {
      $("body").css({
        "color": light_color, // light
        "filter": ""
      });

      $(icons_obj).each(function() {
        $(this).css({
          "filter": light_filter
        });
      });

      $(color_switch_obj).css({
        "filter": ""
      });
    }
  } else {
    $("body").css({
      "background-color": dark_background,
      "color": light_text // dark
    });

    $(background_obj).css({
      "background-image": ""
    });

    $(icons_obj).each(function() {
      $(this).css({
        "filter": light_filter
      });
    });

    $(color_switch_obj).css({
      "filter": ""
    });
  }
}

function setProjects(projects_obj) {
  repos.forEach(function(repo, index) {
    // loop through repos list (global variable)
    let string;
    if (repo.language) {
      string = `<a href="${repo.url}" target="_blank">${repo.formatted_name} - <span class="italic">${repo.language}</span></a><br>`;
    } else {
      string = `<a href="${repo.url}" target="_blank">${repo.formatted_name}</a><br>`;
    }
    $(projects_obj).append(string);
  });
}

function setCodeStats(stats_obj) {
  let newl = "<br>";
  let spacing = " - ";
  let string;

  // total repositories tracker
  string = `${total_lines} lines of code between ${total_commits} commits ${newl} in ${repos.length} repositories`;
  $(stats_obj).children().eq(0).html(string); // first child selection

  string = ``;
  let count = 0;
  Object.entries(languages).forEach(([k,v]) => {
    // loop through languages dict
    let language = k;
    let percent = v;
    string += `${language} ${percent}%`;
    count++;

    // every 3 languages, add newline
    if (count % 3 == 0) {
      string += newl;
    } else {
      string += spacing;
    }
  });

  // if the string ends with a newline, remove it
  if (string.endsWith(newl)) {
    string = string.slice(0, -newl.length);
  }

  $(stats_obj).children().eq(1).html(string); // second child selection
}

function setSubTitle(subtitle_obj) {
  // array rotation
  strings.push(strings.shift()); // global variable

  // some animations
  $(subtitle_obj).fadeOut(100, function() {
    $(subtitle_obj).text(strings[0]);
    $(subtitle_obj).fadeIn(100);
  });

}

function moveOrbs(selector) {
  // move all orbs
  orbs.forEach(function(orb, index) {
    // loop through array
    orb.move(mouse_coords);
  });
}


function setOrbsContainerSize(selector) {
  // the size of the orbit container
  let width, height;
  width = $(".background").width();
  height = $(".background").height();

  if (height != $(selector).height() || width != $(selector).width()) {
    $(selector).css({
      "height": height + "px",
      "width": width + "px"
    });
  }

  // loop through each orb to tell them the new size
  orbs.forEach(function(orb, index) {
    orb.resizeContainer(width, height);
  });
}


// filter generated by https://codepen.io/sosuke/pen/Pjoqqp
var light_color = "#F6F6F6"; // light color for text when background is dark
var dark_color = "#131516"; // dark color for text when background is light
var dark_background = "#363538"; // background color (black and white)
var light_text = "#F6F6F6"; // text color (black and white)
var light_filter = "invert(89%) sepia(68%) saturate(3485%) hue-rotate(182deg) brightness(122%) contrast(93%)"; // #f6f6f6
var dark_filter = "invert(5%) sepia(12%) saturate(476%) hue-rotate(155deg) brightness(104%) contrast(93%)"; // #131516
var bw_filter = "invert(50%) sepia(27%) saturate(725%) hue-rotate(145deg) brightness(88%) contrast(95%)"; // #408697 - blue for black and white mode

var angle = 0; // background angle
var gradient = []; // color gradient
var mouse_coords = new Vector(null, null); // mouse coordinates (used with orbs)
var orbs = []; // orbs container

$(document).ready(function() {
  let subtitle_obj = ".title #subtitle";
  let projects_obj = ".myprojects #projects";
  let projects_link_obj = ".myprojects #projects a";
  let stats_obj = ".codestats";
  let icons_obj = ".icons";
  let icons_svg_obj = ".icons a";
  let background_obj = ".background";
  let color_switch_obj = "#colorswitch";

  let orbs_container_obj = ".orbs";
  let orbs_generated = false;
  let max_orbs = 5;

  let color_mode = false; // black and white
  let rotate_interval; // setInterval for background rotation
  let subtitle_interval; // setInterval for subtitle change

  $('html, body').animate({
    scrollTop: 0
  }, 10);

  console.log("%c Curious about this website? Look at the repo here https://github.com/lorossi/lorenzoros.si-website", "font-size: 200%;color:#ddd;background-color:#131516");

  if (color_mode) {
    selectColors(); //REACTIVATE WITH COLORS
    angle = Math.random() * 360;
    rotate_interval = setInterval(rotateBackground, 100); //REACTIVATE WITH COLORS
  }

  setTextColor(icons_svg_obj, background_obj, color_switch_obj, color_mode);
  setProjects(projects_obj);
  setCodeStats(stats_obj);
  setOrbsContainerSize(orbs_container_obj);

  shuffle(strings);
  setSubTitle(subtitle_obj);

  subtitle_interval = setInterval(setSubTitle, 1000 * 7.5, subtitle_obj);
  setInterval(setOrbsContainerSize, 1000, orbs_container_obj);

  $(subtitle_obj).click(
    function() {
      // we clear and reset interval in order to preserve the delay between switches
      clearInterval(subtitle_interval);
      setSubTitle(subtitle_obj); // changes text when clickd on
      subtitle_interval = setInterval(setSubTitle, 1000 * 7.5, subtitle_obj);
    }
  );

  $(icons_svg_obj + ", " + projects_link_obj + ", " + color_switch_obj).mouseenter(function() {
    // changes color when entering or leaving with mouse
    if (color_mode) {
      if (gradient.bright) {
        if ($(this).text() != "") {
          // we found a text div
          $(this).css({
            "filter": "",
            "color": light_color
        });
        } else {
          // we found an image
          $(this).css({
            "filter": light_filter
          });
        }
      } else {
        if ($(this).text() != "") {
          // we found a text div
          $(this).css({
            "filter": "",
            "color": dark_color
        });
        } else {
          // we found an image
          $(this).css({
            "filter": dark_filter
          });
        }
      }
    } else {
      $(this).css({
        "filter": bw_filter
      });
    }
  }).mouseleave(function() {
    if (color_mode) {
      if (gradient.bright) {
        if ($(this).text() != "") {
          // we found a text div
          $(this).css({
            "filter": "",
            "color": dark_color
        });
        } else {
          // we found an image
          $(this).css({
            "filter": dark_filter
          });
        }
      } else {
        if ($(this).text() != "") {
          // we found a text div
          $(this).css({
            "filter": "",
            "color": light_color
        });
        } else {
          // we found an image
          $(this).css({
            "filter": light_filter
          });
        }
      }
    } else {
      if ($(this).text() != "") {
        // we found a text div
        $(this).css({
          "filter": "",
          "color": light_text
      });
      } else {
        // we found an image
        $(this).css({
          "filter": light_filter
        });
      }
    }
  });

  $(color_switch_obj).click(function() {
    // click over color switch

    // we need to reset every color before shifting it
      $(projects_obj + " *").each(function() {
        $(this).css({
          "color": ""
        });
      });

    if (color_mode) {
      color_mode = !color_mode;
      $(this).text("switch to colors");
      clearInterval(rotate_interval); // we don't need rotating background anymore
      setTextColor(icons_svg_obj, background_obj, color_switch_obj, color_mode);
    } else {
      color_mode = !color_mode;
      $(this).text("switch to dark mode");
      selectColors();
      setTextColor(icons_svg_obj, background_obj, color_switch_obj, color_mode);
      angle = Math.random() * 360;
      rotate_interval = setInterval(rotateBackground, 100); // reactivate rotating background
    }
  });

  $(window).resize(function() {
    // we need to tell orbs that the size has changed
    setOrbsContainerSize(orbs_container_obj);
  });


  $("body").mousemove(function(e) {
    // when mouse is moved over body
    if (!orbs_generated) {
      // generate orbs for the first time
      orbs_generated = true;

      let radius, width, height;
      width = $(".background").width();
      height = $(".background").height();

      if (width > 1000) {
        // PC
        radius = 20;
      } else if (width > 500){
        // Tablet
        radius = 10;
      } else {
        // Mobile
        radius = 5;
      }

      for (let i = 0; i < max_orbs; i++) {
        let x, y;
        x = randomBetween(0, width);
        y = randomBetween(0, height);
        orb = new Orb(x, y, radius, i, orbs_container_obj, width, height);
        orbs.push(orb);
      }
      setInterval(moveOrbs, 10, orbs_container_obj);
    }

    // update mouse_coords global variable
    mouse_coords.x = e.pageX;
    mouse_coords.y = e.pageY;
  });

});
