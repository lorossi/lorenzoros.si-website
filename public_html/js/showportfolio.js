// this script takes care of showing my projects
// one day i'll update my hosting to a VPS so all of this won't be necessary at all - flask ftw
// made by Lorenzo Rossi - www.lorenzoros.si

$(document).ready(function() {
  let repo_container = "#portfolio .projectscontainer";
  let stats_container = "#portfolio .codestats";

  let languages = new Set(resources.repos.map((r) => {
    return r.main_language
  }));
  languages = Array.from(languages);

  languages.forEach((l, i) => {
      let new_element = "";
      new_element += `<tr>`;
      new_element += `<td class="italic language">${l}</td>`;

      new_element += `<td class="repo">`;
      let selected_repos = [];
      resources.repos.forEach((r, j) => {
        if (r.selected && r.main_language === l) {
          let string = `<a href="${r.url}">${r.formatted_name}</a>`
          selected_repos.push(string);
        }
      })
      new_element += `${selected_repos.join(", ")}`;
      new_element += `</td>`;

      $(repo_container).append(new_element);
  })

  $(stats_container + " #repos").text(resources.stats.total_repos);
  $(stats_container + " #commits").text(resources.stats.total_commits);
  $(stats_container + " #languages").text(resources.stats.total_languages);
  $(stats_container + " #stars").text(resources.stats.total_stars);

  placeElements(); // ...
});