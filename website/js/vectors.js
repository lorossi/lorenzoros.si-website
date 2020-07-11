// simple library made for handling 2D vectors

class Vector {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  add(other) {
    this.x = (other.x + this.x);
    this.y = (other.y + this.y);
  }

  sub(other) {
    this.x = (this.x - other.x);
    this.y = (this.y - other.y);
  }

  mult(scalar) {
    this.x *= scalar;
    this.y *= scalar;
  }

  copy(other) {
    this.x = other.x;
    this.y = other.y;
  }

  normalize() {
    let mag = this.mag();
    this.x *= 1 / mag;
    this.y *= 1 / mag;
  }

  mag() {
    return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2));
  }

  setMag(nmag) {
    let mag = this.mag();
    this.x *= nmag / mag
    this.y *= nmag / mag
  }

  limit(nmag) {
    let mag = this.mag();
    if (mag > nmag) {
      this.x *= nmag / mag
      this.y *= nmag / mag
    }
  }

  heading() {
    return Math.atan2(this.y, this.x);
  }
}
