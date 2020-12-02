/*jshint esversion: 6 */
// made by Lorenzo Rossi - https://www.lorenzoros.si - https://github.com/lorossi/

// simple 3D vector library
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

  multiply: function(v) {
    if (v instanceof Vector) {
      this.x *= v.x;
      this.y *= v.y;
      this.z *= v.z;
    } else if (typeof(v) === "number") {
      this.x *= v;
      this.y *= v;
      this.z *= v;
    }
  },

  divide: function(v) {
    if (v instanceof Vector) {
      this.x /= v.x;
      this.y /= v.y;
      this.z /= v.z;
    } else if (typeof(v) === "number") {
      this.x /= v;
      this.y /= v;
      this.z /= v;
    }
  },

  multiply_scalar: function(s) {
    this.multiply(s);
  },

  divide_scalar: function(s) {
    this.divide(s);
  },

  dot: function(v) {
    if (v instanceof Vector) {
      this.x *= v.x;
      this.y *= v.y;
      this.z *= v.z;
    }
  },

  cross: function(v) {
    if (v instanceof Vector) {
      this.x = this.y * v.z - this.z * v.y;
      this.y = this.z * v.x - this.x * v.z;
      this.z = this.x * v.y - this.y * v.z;
    }
  },

  dist: function(v) {
    if (v instanceof Vector) {
      return this.sub(v);
    }
  },

  angleBetween: function(v) {
    if (v instanceof Vector) {
      return Math.acos(this.dot(this, v) / (this.mag() * v.mag()));
    }
  },

  equals: function(v) {
    if (v instanceof Vector) {
      return (this.x == v.x && this.y == v.y && this.z == v.z);
    }
  },

  copy: function() {
    return new Vector(this.x, this.y, this.z);
  },

  limit: function(s) {
    if (typeof(s) === "number") {
      let m = this.mag();
      if (m > s) {
        this.multiply(s / m);
      }
    }
  },

  setMag: function(s) {
    if (typeof(s) === "number") {
      let m = this.mag();
      this.multiply(s / m);
    }
  },

  rotate: function(t) {
    if (typeof(t) === "number") {
      let x2 = Math.cos(t) * this.x - Math.sin(t) * this.y;
      let y2 =  Math.sin(t) * this.x + Math.cos(t) * this.y;
      this.x = x2;
      this.y = y2;
    }
  },

  normalize: function() {
    return this.divide_scalar(this.mag());
  },

  invert: function(x, y, z) {
    if (x) {
      this.x *= -1;
    }
    if (y) {
      this.y *= -1;
    }
    if (z) {
      this.z *= -1;
    }

    if (!x && !y && !z) {
      this.x *= -1;
      this.y *= -1;
      this.z *= -1;
    }
  },

  invertX: function() {
    this.invert(true, false, false);
  },

  invertY: function() {
    this.invert(false, true, false);
  },

  invertZ: function() {
    this.invert(false, false, true);
  },


  mag: function() {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  },

  magSq: function() {
    return this.x * this.x + this.y * this.y + this.z * this.z;
  },

  heading2D: function() {
    return Math.atan2(this.y, this.x);
  },

  toString: function() {
    return `x: ${this.x}, y: ${this.y}, z: ${this.z}`;
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

Vector.random3D = function() {
  let theta = Math.random() * 2 * Math.PI;
  let phi = Math.random() * 2 * Math.PI;
  return new Vector.fromAngle3D(theta, phi);
};

Vector.fromArray = function(a) {
  return new Vector(a[0], a[1], a[2]);
};

Vector.fromObject = function(o) {
  return new Vector(o.x, o.y, o.z);
};
