const s2 = ( sketch ) => {

  let particles, max_particles, particles_scl;
  let noise_scl, time_scl, max_dpos;

  sketch.setup = () => {

    let w, h;
    if ($(window).width() > 600) {
      max_particles = 150;
      particles_scl = 32;
      w = $(window).width();
      h = $("#page2").height();
    } else {
      max_particles = 20;
      particles_scl = 32;
      w = $(window).width() / 3;
      h = $("#page2").height() / 3;
    }
    let canvas = sketch.createCanvas(w, h);
    canvas.parent('sketch2');

    particles = [];
    noise_scl = sketch.map(sketch.width, 0, 1920, 0, 0.00075);
    time_scl = sketch.map(sketch.width, 0, 1920, 0, 0.01);
    max_dpos = sketch.width / 25;

    for (let i = particles.length; i < max_particles; i++) {
      let x, y;
      x = sketch.random(particles_scl, sketch.width - particles_scl);
      y = sketch.random(particles_scl, sketch.height - particles_scl);

      let new_part = new Particle(x, y, particles_scl, noise_scl, time_scl, max_dpos);
      particles.push(new_part);
    }


  }

  sketch.draw = () => {
    if ($("#page2").visible(true) || $(".projectscontainer").visible(true)) {
      sketch.background(0);
      particles.forEach((p, i) => {
        p.show();
        p.move();
      });
    }
  }

  sketch.windowResized = () => {
    let w, h;
    w = $(window).width();
    h = $("#page2").height();
    sketch.resizeCanvas(w, h);
    particles = [];
    sketch.addParticles();
    sketch.background(0);
  }

  sketch.addParticles = () => {
    for (let i = particles.length; i < max_particles; i++) {
      let x, y;
      x = sketch.random(max_dpos, sketch.width - max_dpos);
      y = sketch.random(max_dpos, sketch.height - max_dpos);

      let new_part = new Particle(x, y, particles_scl, noise_scl, time_scl, max_dpos);
      particles.push(new_part);
    }
  }

  class Particle {
    constructor(x, y, particles_scl, noise_scl, time_scl, max_dpos) {
      this.position = sketch.createVector(x, y);
      this.particles_scl = particles_scl;
      this.noise_scl = noise_scl;
      this.time_scl = time_scl;

      this.dpos = sketch.createVector(0, 0);
      this.max_dpos = max_dpos
      this.alpha = 150;
      this.size = particles_scl;
      this.noise_offset = 10000;
    }

    move() {
      let noise_position; // position relative to noise scale
      noise_position = this.position.copy().mult(this.noise_scl);

      let n, rho, theta;
      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl);
      rho = n * this.max_dpos;
      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl + this.noise_offset);
      theta = n * sketch.TWO_PI * 4;
      this.dpos = p5.Vector.fromAngle(theta).setMag(rho);

      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl + this.noise_offset * 2);
      this.size = n * this.particles_scl;
      n = sketch.noise(noise_position.x, noise_position.y, sketch.frameCount * this.time_scl + this.noise_offset * 3);
      this.alpha = n * 128;

    }

    show() {
      sketch.push();
      sketch.translate(this.position.x + this.dpos.x, this.position.y + this.dpos.y)
      sketch.noStroke();
      sketch.fill(255, this.alpha);
      sketch.circle(0, 0, this.size);
      sketch.pop();
    }
  }
}

let sketch2 = new p5(s2);
