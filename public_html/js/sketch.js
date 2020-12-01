/* jshint esversion: 6 */

class Planet {
  constructor(x, y, attracted_x, attracted_y, width, height) {
    this.position = new Vector(x, y);

    this._attracted_position = new Vector(attracted_x, attracted_y);
    this.g = 10000;

    this.force = new Vector(0, 0);
    this.acceleration = new Vector(0, 0);
    this.velocity = new Vector(0, 0);

    this.created_at = performance.now();
    this._alpha = 0;
    this.max_alpha = 0.5;
  }

  move() {
    this.direction = this._attracted_position.copy();
    this.direction.sub(this.position);

    let phi, rho; // force heading and module
    phi = this.direction.heading2D();
    rho = this.g / distSq(this.position.x, this.position.y, this._attracted_position.x, this._attracted_position.y);

    if (rho > 10 || !rho) {
      rho = 10;
    }
    this.force = new Vector.fromAngle2D(phi);
    this.force.setMag(rho);

    this.acceleration.add(this.force);
    this.acceleration.limit(20);
    this.velocity.add(this.acceleration);
    this.velocity.limit(2);
    this.position.add(this.velocity);

    let age = performance.now() - this.created_at;
    if (age > 5000) {
      this._alpha = this.max_alpha;
    } else {
      this._alpha = map(age, 0, 5000, 0, this.max_alpha);
    }
  }

  setAttraction(x, y) {
    this._attracted_position = new Vector(x, y);
  }

  get pos() {
    return {
      x: this.position.x,
      y: this.position.y
    };
  }

  get alpha() {
    return this._alpha;
  }


}

class Sketch1 extends Sketch {
  setup() {
    this.planet_scl = 25;
    this.background = "#000000";
    this.planets = [];

    let center_x, center_y;
    center_x = this.width / 2;
    center_y = this.height / 2;

    for (let i = 0; i < 5; i++) {
      let x, y;
      x = random(this.width);
      y = random(this.height);
      let new_planet = new Planet(x, y, center_x, center_y, this.canvas.width, this.canvas.height);
      this.planets.push(new_planet);
    }

    // time tracking
    this.then = performance.now();
  }


  draw() {
      // reset canvas
      this.ctx.clearRect(0, 0, this.width, this.height);
      // set background
      this.ctx.fillStyle = this.background;
      this.ctx.fillRect(0, 0, this.width, this.height);

      this.planets.forEach((p, i) => {
        p.move();
        this.ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha})`;
        this.ctx.beginPath();
        this.ctx.arc(p.pos.x, p.pos.y, this.planet_scl, 0, 2 * Math.PI);
        this.ctx.fill();
      });


    window.requestAnimationFrame(this.draw.bind(this));
  }
}

let s1;

$(document).ready(() => {
  canvas = document.getElementById("sketch1");
  if (canvas.getContext) {
    ctx = canvas.getContext("2d", {alpha: false});
    s1 = new Sketch1(canvas, ctx);
    s1.run();
  }
});

$(document).mousemove((e) => {
  if (s1.planets) {
    s1.planets.forEach((p, i) => {
      p.setAttraction(e.pageX * canvas_scl, e.pageY * canvas_scl);
    });
  }

});
