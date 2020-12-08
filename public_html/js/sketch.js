/* jshint esversion: 6 */

class Particle {
    constructor(width, height) {
      this._width = width;
      this._height = height;

      if (this._width > 600) {
        this._min_size = 10;
        this._max_size = 20;
        this._min_alpha = 0.1;
        this._max_alpha = 0.8;
        this._min_speed = 0.5;
        this._max_speed = 3;
      } else {
        this._min_size = 4;
        this._max_size = 8;
        this._min_alpha = 0.1;
        this._max_alpha = 0.8;
        this._min_speed = 0.25;
        this._max_speed = 1;
      }

      this.opacity = this._max_alpha;
      this._radius = random(this._min_size, this._max_size);
      this.speed = random(this._min_speed, this._max_speed);

      let x, y;
      x = random(this._radius, this._width - this._radius);
      y = random(this._radius, this._height - this._radius);
      this._position = new Vector(x, y);

      this.velocity = Vector.random2D();
      this.velocity.multiply_scalar(this.speed);

      this._paired = [];
      this._color = getCssProperty("--text");
    }

    move() {
      this._paired = [];
      this._position.add(this.velocity);

      if (this._position.x + this._radius > this._width || this._position.x - this._radius < 0) this.velocity.invertX();
      if (this._position.y + this._radius > this._height || this._position.y - this._radius < 0) this.velocity.invertY();

    }

    get pos() {
      return {
        x: this._position.x,
        y: this._position.y
      };
    }

    get radius() {
      return this._radius;
    }

    get color() {
      let hex_opacity = parseInt(this.opacity * 255).toString(16).padStart(2, '0');
      return this._color + hex_opacity;
    }

    set paired(i) {
      this._paired.push(i);
    }

    get paired() {
      return this._paired;
    }

    set width(w) {
      this._width = w;
    }

    set height(h) {
      this._height = h;
    }

    get min_alpha() {
      return this._min_alpha;
    }

    get max_alpha() {
      return this._max_alpha;
    }
}


class Sketch {
  constructor(canvas, context, fps) {
    this.canvas = canvas;
    this.ctx = context;
    this.fps = fps || 30;
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

  resized() {
    this.width = this.canvas.width;
    this.height = this.canvas.height;

    this.particles.forEach((p, i) => {
      p.width = this.width;
      p.height = this.height;
    });

  }

  setup() {
    this.background = getCssProperty("--background");

    if (this.width > 600) {
      this.particles_num = 65;
      this.max_dist_sq = Math.pow(this.width * 0.15, 2);
      this.max_connections = 3;
    } else {
      this.particles_num = 30;
      this.max_dist_sq = Math.pow(this.width * 0.5, 2);
      this.max_connections = 2;
    }

    this.particles = [];
    for (let i = 0; i < this.particles_num; i++) {
      let new_part = new Particle(this.width, this.height);
      this.particles.push(new_part);
    }

    // keep track of time to handle fps
    this.then = performance.now();
  }

  draw() {
    window.requestAnimationFrame(this.draw.bind(this));

    let diff;
    diff = performance.now() - this.then;
    if (diff < this.fps_interval) {
     // not enough time has passed, so we request next frame and give up on this render
     return;
    }

    // updated last frame rendered time
    this.then = performance.now();

    this.ctx.save();

    // reset canvas
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);
    // set background
    this.ctx.fillStyle = this.background;
    this.ctx.fillRect(0, 0, canvas.width, canvas.height);

    // move particles
    this.particles.forEach((p, i) => {
      p.move();
    });

    // draw lines
    this.ctx.save();
    let min_alpha, max_alpha;
    max_alpha = this.particles[0].max_alpha;
    min_alpha = this.particles[0].min_alpha;

    // stroke color as set in css
    let stroke_color = getCssProperty("--text");

    for (let i = 0; i < this.particles.length; i++) {
      let pos_1 = this.particles[i].pos;
      if (this.particles[i].paired.length >= this.max_connections) continue;

      for (let j = 0; j < this.particles.length; j++) {
        if (i == j) continue;
        if (this.particles[j].paired.includes(i)) continue;
        if (this.particles[j].paired.length >= this.max_connections) continue;
        let pos_2 = this.particles[j].pos;

        let dist_sq = distSq(pos_1.x, pos_1.y, pos_2.x, pos_2.y);
        if (dist_sq < this.max_dist_sq) {
          this.particles[j].paired = i;
          this.particles[i].paired = j;
          let alpha = map(dist_sq, 0, this.max_dist_sq, max_alpha, min_alpha);
          let stroke_alpha = parseInt(alpha * 255).toString(16).padStart(2, '0');
          this.ctx.strokeStyle = stroke_color + stroke_alpha;
          this.ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(pos_1.x, pos_1.y);
          ctx.lineTo(pos_2.x, pos_2.y);
          ctx.stroke();
        }
      }
    }
    this.ctx.restore();


    // draw particles
    this.ctx.save();
    this.particles.forEach((p, i) => {
      this.ctx.fillStyle = this.background;
      this.ctx.beginPath();
      this.ctx.arc(p.pos.x, p.pos.y, p.radius, 0, 2 * Math.PI);
      this.ctx.fill();

      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.pos.x, p.pos.y, p.radius, 0, 2 * Math.PI);
      this.ctx.fill();
    });
    this.ctx.restore();

    this.ctx.restore();
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

$(window).resize(() => {
  sketch.resized();
});
