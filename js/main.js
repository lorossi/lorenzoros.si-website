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



var angle = 0;
var gradient = [];
var colors = [["#1ABC9C", "#2ECC71", true], ["#1ABC9C", "#3498DB", true], ["#1ABC9C", "#27AE60", true], ["#1ABC9C", "#2980B9", true], ["#2ECC71", "#3498DB", true], ["#2ECC71", "#16A085", true], ["#2ECC71", "#2980B9", true], ["#3498DB", "#9B59B6", false], ["#3498DB", "#16A085", true], ["#3498DB", "#27AE60", true], ["#3498DB", "#8E44AD", false], ["#9B59B6", "#2980B9", false], ["#16A085", "#27AE60", true], ["#16A085", "#2980B9", false], ["#27AE60", "#2980B9", false], ["#2980B9", "#8E44AD", false], ["#F1C40F", "#E74C3C", true], ["#F1C40F", "#D35400", true], ["#F1C40F", "#C0392B", true], ["#E67E22", "#E74C3C", false], ["#E67E22", "#C0392B", false], ["#E74C3C", "#F39C12", true], ["#F39C12", "#C0392B", false]]
var subtitles = ["not a designer", "not a full stack programmer", "not (yet) an engineer", "a good programmer", "a creative guy", "many good ideas", "eager to learn", "can use stackoverflow", "visit my GitHub", "likes minimalistic design"];

$(document).ready(function() {
  let subtitle_obj = ".title #subtitle";
  selectColors();
  setTextColor();
  angle = Math.random() * 360;

  console.log("%c Curious about this website? Look at the repo here https://github.com", "font-size: 2rem");

  setTimeout(setSubtitle, 200, subtitle_obj);
  setInterval(setSubtitle, 1000 * 15, subtitle_obj);

  setInterval(rotateBackground, 100);

  $(".icons a").mouseenter(function() {
    if (gradient[2]) {
      $(this).css({"filter": "invert(100%)"});
    } else {
      $(this).css({"filter": "invert(0%)"});
    }
  });

  $(".icons a").mouseleave(function() {
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
})
