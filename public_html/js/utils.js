/*jshint esversion: 6 */

let scrolling;
$(window).scroll(function(){
  let ended;
  if (!scrolling) {
    scrolling = true;
    clearInterval(ended);
    setInterval(() => {
      scrolling = false;
    }, 100);
  }
});

const random = (min, max, int) => {
    if (max == null && min != null) {
      max = min;
      min = 0;
    } else if (min == null && max == null) {
      min = 0;
      max = 1;
    }

   let randomNum = Math.random() * (max - min) + min;

   // return an integer value
   if (int) {
     return Math.round(randomNum);
   }

   return randomNum;
};

const map = (val, old_min, old_max, new_min, new_max) => {
  if (val > old_max) {
    val = old_max;
  } else if (val < old_min) {
    val = old_min;
  }

  return (val - old_min) * (new_max - new_min) / (old_max - old_min) + new_min;
};

const dist = (x1, y1, x2, y2) => {
  return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
};

const distSq = (x1, y1, x2, y2) => {
  return Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2);
};

// the only way i found to access css variables
const getCssProperty = (property) => {
  // no type handling
  // returns a string
  let css_property = getComputedStyle(document.documentElement).getPropertyValue(property);
  return css_property.split(" ").join("");
};
