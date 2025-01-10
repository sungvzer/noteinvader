function syncSearchBoxes(isNavbar) {
  navbarId = "navbar_search_input";
  searchId = "search_input";
  navbarSearch = document.getElementById(navbarId);
  search = document.getElementById(searchId);
  if (!navbarSearch || !search) {
    return;
  }
  if (isNavbar) {
    search.value = navbarSearch.value;
  } else {
    navbarSearch.value = search.value;
  }
}
