const s3 = ( sketch ) => {
  let points, max_points;
  let points_scl,max_dist_sq;

  sketch.setup = () => {
    let w, h;
    w = $(window).width();
    h = $("#page3").height();
    let canvas = sketch.createCanvas(w, h);
    canvas.parent('sketch3');
    if ($(window).width() > 600) {
      points_scl = 24;
      max_points = 50;
      max_dist_sq = Math.pow(sketch.width / 5, 2);
    } else {
      points_scl = 16;
      max_points = 10;
      max_dist_sq = Math.pow(sketch.width, 2);
    }

    points = [];
    for (let i = 0; i < max_points; i++) {
      x = sketch.random(sketch.width);
      y = sketch.random(sketch.height);
      let new_point = new Point(x, y, points_scl, max_dist_sq);
      points.push(new_point);
    }
  }

  sketch.draw = () => {
    if ($("#page3").visible(true)) {
      sketch.background(0);
      for (let i = 0; i < points.length; i++) {
        p = points[i];
        p.show();
        p.move();

        for (let j = 0; j < points.length; j++) {
          if (i != j) {
            q = points[j];
            if (p.isClose(q)) {
              let current_dist = sketch.dist(p.position.x, p.position.y, q.position.x, q.position.y);
              let max_dist = Math.sqrt(p.max_dist_sq);
              let alpha = sketch.map(current_dist, 0, max_dist, p.alpha/2, 0);
              sketch.strokeWeight(2);
              sketch.stroke(255, alpha);
              sketch.line(p.position.x, p.position.y, q.position.x, q.position.y);
            }
          }
        }
      }
    }
  }

  sketch.windowResized = () => {
    let w, h;
    w = $(window).width();
    h = $("#sketch3").height();
    sketch.resizeCanvas(w, h);
  }

  sketch.calculateRight = () => {
    return ($(window).width() - $(".contactscontainer").width() - $(".contactscontainer").position().left - $(".content").position().left) * .9;
  }

  class Point {
    constructor(x, y, show_scl, max_dist_sq) {
      this.position = sketch.createVector(x, y);
      this.show_scl = show_scl;

      this.z = sketch.random(1);
      this.speed = sketch.map(this.z, 0, 1, 0.5, 3);
      this.size = sketch.map(this.z, 0, 1, .5, 1) * this.show_scl;
      this.velocity = p5.Vector.random2D().setMag(this.speed);
      this.alpha = 50;
      this.max_dist_sq = max_dist_sq;
    }

    move() {
      this.position.add(this.velocity);

      if (this.position.x + this.size / 2 > sketch.width || this.position.x - this.size / 2 < 0) {
        this.velocity.x *= -1;
      }

      if (this.position.y + this.size / 2 > sketch.height || this.position.y - this.size / 2 < 0) {
        this.velocity.y *= -1;
      }
    }

    show() {
      sketch.push();
      sketch.translate(this.position.x, this.position.y);
      sketch.noStroke();
      sketch.fill(255, this.alpha);
      sketch.circle(0, 0, this.size);
      sketch.pop();
    }

    isClose(point) {
      let mag_sq = this.position.copy().sub(point.position).magSq();

      if (mag_sq < this.max_dist_sq) {
        return true;
      }
    }
  }
}

let sketch3 = new p5(s3);
