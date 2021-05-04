document.addEventListener("DOMContentLoaded", () => {
  printLetters();
});

const printLetters = (selector = ".typer p", speed = 50) => {
  let to_write = [];
  const dest_items = [...document.querySelectorAll(selector)];
  dest_items.forEach(p => { to_write.push(p.textContent.split("")); p.textContent = ""; });


  let item_count = 0;
  let letter_count = 0;

  const type = () => {
    const current_letter = to_write[item_count][letter_count];
    dest_items[item_count].textContent += current_letter;
    letter_count++;

    if (letter_count >= to_write[item_count].length) {
      letter_count = 0;
      item_count++;
    }

    if (item_count >= dest_items.length) {
      clearInterval(interval);
    }
  };

  let interval = setInterval(type, speed);

};