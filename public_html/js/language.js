// this script takes care of language handling
// made by Lorenzo Rossi - www.lorenzoros.si

/*jshint esversion: 6 */

let active_language;
$(document).ready(function() {
  let language = navigator.language || navigator.userLanguage;

  if (language === "it-IT") {
    $("*:lang(it-IT)").css({"display": "inline-block"});
    $("*:lang(en-EN)").css({"display": "none"});
    active_language = "it-IT";
  } else {
    active_language = "en-EN";
  }

  $(".languageswitch").click(function() {
    $(`*:lang(${active_language})`).css({"display": "none"});

    if (active_language === "it-IT") { // switch languages around
      active_language = "en-EN";
    } else {
      active_language = "it-IT";
    }

    $(`*:lang(${active_language})`).css({"display": "inline-block"});
  });

});
