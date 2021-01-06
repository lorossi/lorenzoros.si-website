/* jshint esversion: 8 */

// this script takes care of showing my projects
// one day i'll update my hosting to a VPS so all of this won't be necessary at all - flask ftw
// made by Lorenzo Rossi - www.lorenzoros.si

$(document).ready(function() {
  let repo_container = "#portfolio .projectscontainer";

  let languages = new Set(resources.repos.map((r) => {
    return r.main_language;
  }));
  languages = Array.from(languages);

  languages.forEach((l, i) => {
      let new_element = "";
      new_element += `<tr><td class="italic language">${l}</td>`;

      let selected_repos = [];
      resources.repos.forEach((r, j) => {
        if (r.selected && r.main_language === l) {
          if (selected_repos.length > 0) {
            new_element += `<td class="language"></td>`;
          }
          new_element += `<td class="repo"><a href="${r.url}">${r.formatted_name}</a></td><td class="description opaque">${r.description.toLowerCase()}</td></tr>`;

          selected_repos.push(r);
        }
      });

      // skips languages that don't have any repo
      if (selected_repos.length > 0) {
          new_element += `<tr class="empty"></tr>`;
          $(repo_container).append(new_element);
      }
  });
});
