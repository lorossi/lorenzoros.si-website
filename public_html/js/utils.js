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

function random(min, max, int) {
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
}


function map(val, old_min, old_max, new_min, new_max) {
  if (val > old_max) {
    val = old_max;
  } else if (val < old_min) {
    val = old_min;
  }

  return (new_max - new_min) / (old_max - old_min) * (val - old_min) + new_max;
}

function dist(x1, y1, x2, y2) {
  return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}

function distSq(x1, y1, x2, y2) {
  return Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2);
}


class Sketch {
  constructor(canvas, context, fps) {
    this.canvas = canvas;
    this.ctx = context;
    this.fps = fps || 60;
    this.fps_interval = 1 / this.fps;
    this.width = canvas.width;
    this.height = canvas.height;

    // save canvas in memory
    this.savedData = new Image();

  }

  run() {
    // run once
    this.setup();
    // anti alias
    this.ctx.beginPath();
    this.ctx.translate(0.5, 0.5);
    // run often draw
    this.draw();
  }

  loop() {
    while (true) {
      window.requestAnimationFrame(this.draw.bind(this));

      while (true) {
        let now = performance.now();
        let elapsed = (now - this.then) / 1000;

        if (elapsed > this.fps_interval) {
          this.then = now;
          break;
        }
      }
    }
  }

  save() {
    this.savedData.src = this.canvas.toDataURL("image/png");
  }

  restore() {
    this.ctx.drawImage(this.savedData, 0, 0);
  }
}
