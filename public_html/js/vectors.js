/*jshint esversion: 6 */

// simple and uncomplete vector library

function Vector(x, y, z) {
  this.x = x || 0;
  this.y = y || 0;
  this.z = z || 0;
}

Vector.prototype = {
  add: function(v) {
    if (v instanceof Vector) {
      this.x += v.x;
      this.y += v.y;
      this.z += v.z;
    }
  },

  sub: function(v) {
    if (v instanceof Vector) {
      this.x -= v.x;
      this.y -= v.y;
      this.z -= v.z;
    }
  },

  multiply_scalar: function(s) {
    this.x *= s;
    this.y *= s;
    this.z *= s;
  },

  divide_scalar: function(s) {
    this.x /= s;
    this.y /= s;
    this.z /= s;
  },

  copy: function() {
    return new Vector(this.x, this.y, this.z);
  },

  limit: function(s) {
    let m = this.mag();
    if (m > s) {
      this.multiply_scalar(s / m);
    }
  },

  setMag: function(s) {
    let m = this.mag();
    this.multiply_scalar(s / m);
  },

  normalize: function() {
    return this.divide_scalar(this.mag());
  },

  mag: function() {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  },

  magSq: function() {
    return this.x * this.x + this.y * this.y + this.z * this.z;
  },

  heading2D: function() {
    return Math.atan2(this.y, this.x);
  }
};

Vector.fromAngle3D = function(theta, phi) {
  return new Vector(Math.cos(theta) * Math.cos(phi), Math.sin(phi), Math.sin(theta) * Math.cos(phi));
};

Vector.fromAngle2D = function(theta) {
  return new Vector(Math.cos(theta), Math.sin(theta), 0);
};

Vector.random2D = function() {
  let theta = Math.random() * 2 * Math.PI;
  return new Vector.fromAngle2D(theta);
};
