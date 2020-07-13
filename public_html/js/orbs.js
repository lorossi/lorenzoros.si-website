class Orb {
  constructor(x, y, id, container, width, height) {
    this.pos = new Vector(x, y);
    this.vel = new Vector(0, 0);
    this.acc = new Vector(0, 0);
    this.force = new Vector(0, 0);

    this.id = id;
    this.container = container;

    this.container_width = width;
    this.container_height = height;
    this.setRadius(width);

    this.attachToContainer(this.container);
    // tweakable parameters
    // the maxforce limits the amount of force "stored" in each element
    //    the higher it is, the further the orb will orbit
    this.maxvel = 6;
    this.maxacc = 0.2;
    this.maxforce = 0.1;
    // the G factor sacles with the size
    this.g = 2 * Math.pow(10, 5) * Math.pow(this.container_width/2114.44, 2);
  }

  resizeContainer(width, height) {
    // we update the container size
    this.container_width = width;
    this.container_height = height;
  }

  setRadius(width) {
    if (width > 1000) {
      // PC
      this.r = 20;
    } else if (width > 500){
      // Tablet
      this.r = 10;
    } else {
      // Mobile
      this.r = 5;
    }
  }

  attachToContainer() {
    // add orb element to container
    // each orb has an attribute, "orbid", made to select it
    $("<div>", {
      "id": "orb",
      css: {
        "left": this.pos.x + "px",
        "top": this.pos.y + "px",
        "width": this.r * 2 + "px",
        "height": this.r * 2 + "px",
        "animation-name": "fadeinOrb",
        "animation-delay": "1s",
        "animation-duration": "3s",
        "animation-fill-mode": "forwards",
        "animation-timing": "ease-in"
      }
    }).attr("orbid", this.id).appendTo(this.container);
  }

  move(destination) {
    let dist = new Vector(0, 0);
    let force_mag;

    dist.copy(destination);
    dist.sub(this.pos);

    // calculate magnitude force
    force_mag = this.g / Math.pow(dist.mag(), 2);

    // calculate force vector
    dist.setMag(force_mag);
    this.force.add(dist);
    this.force.limit(this.maxforce);

    // reset acceleration and add force to it
    this.acc.mult(0);
    this.acc.add(this.force);
    this.acc.limit(this.maxacc);

    // add acceleration to velocity
    this.vel.add(this.acc);
    this.vel.limit(this.maxvel);

    // add velocity to position
    this.pos.add(this.vel);

    if (this.pos.x - this.r < 0 || this.pos.y - this.r < 0 || this.pos.x + this.r > this.container_width || this.pos.y + this.r > this.container_height) {
      // the orbit is outside its container, so we don't want to render it
      $(`#orb[orbid="${this.id}"]`).css({
        "display": "none"
      })
    } else {
      // the orbit is outside the container. Render it normally
      $(`#orb[orbid="${this.id}"]`).css({
        "left": this.pos.x + "px",
        "top": this.pos.y + "px",
      })

      // reset its visibility
      if ($(`#orb[orbid="${this.id}"]`).css("display") == "none") {
        $(`#orb[orbid="${this.id}"]`).css({"display": "block"});
      }
    }
  }
}
