/* jshint esversion: 6 */

class Particle {
    constructor(width, height) {
      this._width = width;
      this._height = height;

      if (this._width > 600) {
        this._min_size = 5;
        this._max_size = 15;
        this._min_alpha = 0.1;
        this._max_alpha = 0.3;
      } else {
        this._min_size = 2;
        this._max_size = 6;
        this._min_alpha = 0.05;
        this._max_alpha = 0.2;
      }


      this.z = random(10);
      this.opacity = map(this.z, 0, 10, this._min_alpha, this._max_alpha);
      this._radius = map(this.z, 0, 10, this._min_size, this._max_size);
      this.velocity = map(this.z, 0, 10, 0.5, 1.25);

      let x, y;
      x = random(this._radius, this._width - this._radius);
      y = random(this._radius, this._height - this._radius);
      this._position = new Vector(x, y);

      this.speed = Vector.random2D();
      this.speed.multiply_scalar(this.velocity);

      this._paired = [];
    }

    move() {
      this._paired = [];
      this._position.add(this.speed);

      if (this._position.x + this._radius > this._width || this._position.x - this._radius < 0) this.speed.x *= -1;
      if (this._position.y + this._radius > this._height || this._position.y - this._radius < 0) this.speed.y *= -1;

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
      return `rgba(255, 255, 255, ${this.opacity})`;
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

  resized() {
    this.width = canvas.width;
    this.height = canvas.height;

    this.particles.forEach((p, i) => {
      p.width = this.width;
      p.height = this.height;
    });

  }

  setup() {
    this.background = "#000000";

    if (this.width > 600) {
      this.particles_num = 70;
      this.max_dist_sq = Math.pow(this.width * 0.2, 2);
    } else {
      this.particles_num = 40;
      this.max_dist_sq = Math.pow(this.width * 0.4, 2);
    }

    this.particles = [];
    for (let i = 0; i < this.particles_num; i++) {
      let new_part = new Particle(this.width, this.height);
      this.particles.push(new_part);
    }
  }

  draw() {
    this.ctx.save();

    // reset canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // set background
    ctx.fillStyle = this.background;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // move particles
    this.particles.forEach((p, i) => {
      p.move();
    });

    // draw lines
    this.ctx.save();
    let min_alpha, max_alpha;
    min_alpha = this.particles[0].min_alpha;
    max_alpha = this.particles[0].max_alpha;

    for (let i = 0; i < this.particles.length; i++) {
      let pos_1 = this.particles[i].pos;

      for (let j = 0; j < this.particles.length; j++) {
        if (i == j) continue;
        if (this.particles[j].paired.includes(i)) continue;
        let pos_2 = this.particles[j].pos;

        let dist_sq = distSq(pos_1.x, pos_1.y, pos_2.x, pos_2.y);
        if (dist_sq < this.max_dist_sq) {
          this.particles[j].paired = i;
          this.particles[i].paired = j;

          let alpha = map(dist_sq, 0, this.max_dist_sq, max_alpha, min_alpha);
          this.ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
          this.ctx.lineWidth = 2;
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
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.pos.x, p.pos.y, p.radius, 0, 2 * Math.PI);
      this.ctx.fill();
    });
    this.ctx.restore();

    this.ctx.restore();

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

$(window).resize(() => {
  sketch.resized();
});
