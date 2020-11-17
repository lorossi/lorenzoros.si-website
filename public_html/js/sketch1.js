const s1 = ( sketch ) => {
  let particles, max_particles;
  let particles_scl, noise_scl, time_scl;
  let w, h;

  sketch.setup = () => {
    // SKETCH PARAMETERS
    if ($(window).width() > 600) {
      max_particles = 125;
      particles_scl = 2;
      w = $(window).width();
      h = $("#page1").height();
    } else {
      max_particles = 20;
      particles_scl = 2;
      w = $(window).width() / 3;
      h = $("#page1").height() / 3;
    }
    let canvas = sketch.createCanvas(w, h);
    canvas.parent('sketch1');

    particles = [];
    noise_scl = sketch.map(sketch.width, 0, 1920, 0, 0.0015);
    time_scl = sketch.map(sketch.width, 0, 1920, 0, 0.0004);

    sketch.addParticles();

    sketch.background(0);
  }

  sketch.draw = () => {
    if ($("#page1").visible(true)) {
      particles.forEach((p, i) => {
        p.show();
        p.move();
      });

      for (let i = particles.length - 1; i >= 0; i--) {
        if (!particles[i].isAlive()) {
          particles.splice(i, 1);
        }
      }

      sketch.addParticles();
    }
  }

  sketch.windowResized = () => {
    if ($(window).width() != w) {
      w = $(window).width();
      h = $("#page1").height();
      sketch.resizeCanvas(w, h);
      sketch.addParticles();
    }
  }

  sketch.addParticles = () => {
    for (let i = particles.length; i < max_particles; i++) {
      let x, y;
      x = sketch.random(sketch.width);
      y = sketch.random(sketch.height);

      let new_part = new Particle(x, y, particles_scl, noise_scl, time_scl);
      particles.push(new_part);
    }
  }

  class Particle {
    constructor(x, y, show_scl, noise_scl, time_scl) {
      this.position = sketch.createVector(x, y);
      this.show_scl = show_scl;
      this.noise_scl = noise_scl;
      this.time_scl = time_scl;

      this.alive = true;
      this.noise_offset = 10000;
      this.created_at = sketch.frameCount;
      this.alpha = 25;

      this.max_force = sketch.map(sketch.windowWidth, 0, 1920, 0, 2);
      this.force = sketch.createVector(0, 0);

      this.max_acceleration = sketch.map(sketch.windowWidth, 0, 1920, 0, 10);
      this.acceleration = sketch.createVector(0, 0);

      this.max_velocity = 1;
      this.velocity = sketch.createVector(0, 0);
    }

    move() {
      let noise_position; // position relative to noise scale
      noise_position = this.position.copy().mult(this.noise_scl);

      let n, rho, theta;
      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl);
      rho = n * this.max_force; // force module
      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl + this.noise_offset);
      theta = n * sketch.TWO_PI * 8;

      this.force.mult(0); // reset force
      this.force = p5.Vector.fromAngle(theta).setMag(rho); // create vector

      this.acceleration.add(this.force);
      this.acceleration.limit(this.max_acceleration);

      this.velocity.add(this.acceleration);
      this.velocity.limit(this.max_velocity);

      this.position.add(this.velocity);


      if (this.position.x < 0 || this.position.x > sketch.width || this.position.y < 0 || this.position.y > sketch.height) {
        this.alive = false;
      }

    }

    show() {
      sketch.push();
      sketch.translate(this.position.x, this.position.y);
      sketch.noStroke();
      let age = (sketch.frameCount - this.created_at) / 60 * 6;
      if (age > this.alpha) {
        sketch.fill(255, this.alpha);
      } else {
        sketch.fill(255, age);
      }
      sketch.circle(0, 0, this.show_scl);
      sketch.pop();
    }

    isAlive() {
      return this.alive;
    }
  }

}

let sketch1 = new p5(s1);
