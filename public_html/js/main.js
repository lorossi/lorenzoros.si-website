document.addEventListener("DOMContentLoaded", async () => {
  console.clear();
  console.log("%c Curious? Check the repo! https://github.com/lorossi/lorenzoros.si-website", "font-size: 1rem;");
  await print_letters();
});

window.addEventListener("resize", () => {

});

const print_letters = async (selector = ".typer p", speed = 25, newline_pause = 500) => {
  await timeout(500);
  return new Promise(resolve => {
    let to_write = [];
    const dest_items = [...document.querySelectorAll(selector)];
    dest_items.forEach(p => { to_write.push(p.textContent.split("")); p.textContent = ""; });

    let item_count = 0;
    let letter_count = 0;

    const type = async () => {

      if (letter_count == 0) {
        // add the blinking cursor
        dest_items[item_count].classList.add("writing", "newline");
      }

      // next letter to be written
      let current_letter = to_write[item_count][letter_count];
      if (current_letter == undefined) current_letter = "";
      // append letter to container
      dest_items[item_count].append(current_letter);
      // increase letter count to proceed
      letter_count++;

      // finished a a container item
      if (letter_count >= to_write[item_count].length) {
        // wait a little bit
        await timeout(newline_pause);
        // remove the blinking cursor if this isn't the last line
        if (item_count < dest_items.length - 1) {
          dest_items[item_count].classList.remove("writing");
        }

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

function timeout(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}