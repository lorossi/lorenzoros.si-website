document.addEventListener("DOMContentLoaded", async () => {
  glitch_background();
  await print_letters();
  await timeout(5000);
  destroy_letters();
});

const glitch_background = (items = 50) => {
  const height = document.body.scrollHeight;
  const container = document.querySelector(".lines-container");

  for (let i = 0; i < items; i++) {
    const line = document.createElement("line");
    line.classList.add("glitchline");
    line.style.animationDelay = Math.random() * 2 + "s";
    line.style.animationDuration = Math.random() * 500 + "ms";
    line.style.top = Math.random() * height + "px";
    container.append(line);
  }
};

const print_letters = async (selector = ".typer p", speed = 50, newline_pause = 500) => {
  return new Promise(resolve => {
    let to_write = [];
    const dest_items = [...document.querySelectorAll(selector)];
    dest_items.forEach(p => { to_write.push(p.textContent.split("")); p.textContent = ""; });


    let item_count = 0;
    let letter_count = 0;

    const type = async () => {

      if (letter_count == 0) {
        // add the blinking cursor
        dest_items[item_count].classList.add("writing", "newline", "aberration");
      }

      // next letter to be written
      const current_letter = to_write[item_count][letter_count];
      // append letter to container
      dest_items[item_count].append(current_letter);
      // increase letter count to proceed
      letter_count++;

      // finished a a container item
      if (letter_count >= to_write[item_count].length) {
        // wait a little bit
        await timeout(newline_pause);
        // remove the blinking cursor
        dest_items[item_count].classList.remove("writing");
        letter_count = 0;
        item_count++;
      }

      if (item_count < dest_items.length) {
        // if the full write isn't ended yet, call this function again
        await timeout(speed);
        type();
      } else if (item_count == dest_items.length) {
        return resolve("done");
      }
    };

    // bootstrap the function
    type();
  });
};

const destroy_letters = () => {
  // the letters should now fall
  // rigid body phisics...
  // that kinda hard
  // https://www.toptal.com/game/video-game-physics-part-i-an-introduction-to-rigid-body-dynamics
};

function timeout(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}