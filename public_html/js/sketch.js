/* jshint esversion: 6 */

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

  save() {
    this.savedData.src = this.canvas.toDataURL("image/png");
  }

  restore() {
    this.ctx.drawImage(this.savedData, 0, 0);
  }

  setup() {

  }


  draw() {

    window.requestAnimationFrame(this.draw.bind(this));
  }
}

let sketch;
$(document).ready(() => {
  canvas = document.getElementById("sketch");
  if (canvas.getContext) {
    ctx = canvas.getContext("2d", {alpha: false});
    sketch = new Sketch(canvas, ctx);
    sketch.run();
  }
});
