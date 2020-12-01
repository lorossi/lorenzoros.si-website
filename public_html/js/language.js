// this script takes care of language handling
// made by Lorenzo Rossi - www.lorenzoros.si

$(document).ready(function() {
  let list_selector = "li"; // elements that must be displayed as list
  let cell_selector = "td"; // elements that must be displayed as table cell
  let language = navigator.language || navigator.userLanguage;

  if (language === "it-IT") {
    $("*:lang(it)").css({"display": "inline-block"});
    $("*:lang(it) " + list_selector).css({"display": "list-item"});
    $("*:lang(en)").css({"display": "none"});
    active_language = "it-IT";
  } else {
    active_language = "en-EN";
  }

  $(".languageswitch").click(function() {
    let short_language, selector;

    short_language = active_language.slice(0, 2); // en for english and it for italian
    selector = `*:lang(${short_language})`;
    $(selector).css({"display": "none"});

    if (active_language === "it-IT") { // switch languages around
      active_language = "en-EN";
    } else {
      active_language = "it-IT";
    }

    short_language = active_language.slice(0, 2); // en for english and it for italian
    selector = `*:lang(${short_language})`;
    $(selector).css({"display": "inline-block"});

    $(selector + " " + list_selector).css({"display": "list-item"});
    $(selector + " " + list_selector).css({"display": "table-cell"});
  })

});
