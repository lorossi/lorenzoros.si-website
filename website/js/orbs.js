class Orb {
  constructor(x, y, r, id, container) {
    this.pos = new Vector(x, y);
    this.vel = new Vector(0, 0);
    this.acc = new Vector(0, 0);
    this.force = new Vector(0, 0);

    this.id = id;
    this.r = r;
    this.container = container;
    this.attachToContainer();

    this.g = Math.pow(10, 6);
    this.maxvel = 5;
    this.maxacc = 0.05;
    this.maxforce = 0.1;
  }

  attachToContainer() {
    $("<div>", {
      "id": "orb",
      css: {
        "left": this.pos.x + "px",
        "top": this.pos.y + "px",
        "width": this.r * 2 + "px",
        "height": this.r * 2 + "px",
        "opacity": 0,
        "animation-name": "fadeinOrb",
        "animation-delay": "2s",
        "animation-duration": "3s",
        "animation-fill-mode": "forwards"
      }
    }).attr("orbid", this.id).appendTo(this.container);
  }

  move(destination) {
    let dist = new Vector(0, 0);
    let force_mag;

    dist.copy(destination);
    dist.sub(this.pos);

    force_mag = this.g / Math.pow(dist.mag(), 2);

    dist.setMag(force_mag);
    this.force.add(dist);
    this.force.limit(this.maxforce);

    this.acc.mult(0);
    this.acc.add(this.force);
    this.acc.limit(this.maxacc);

    this.vel.add(this.acc);
    this.vel.limit(this.maxvel);

    this.pos.add(this.vel);

    let container_width, container_height;
    container_width = $(this.container).width();
    container_height = $(this.container).height();

    let visbility;
    if (this.pos.x - this.r < 0 || this.pos.y - this.r < 0 || this.pos.x + this.r > container_width || this.pos.y + this.r > container_height) {
      $("#orb[orbid=\"" + this.id + "\"]").css({
        "display": "none"
      })
    } else {
      $("#orb[orbid=\"" + this.id + "\"]").css({
        "left": this.pos.x + "px",
        "top": this.pos.y + "px",
        "display": "block"
      })
    }
  }
}
