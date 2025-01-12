async function toggleFavorite(albumId) {
  console.log("toggleFavorite: " + albumId);

  const response = await fetch(`/api/favorites/${albumId}`, {
    method: "POST",
  });
  if (!response.ok) {
    console.error("Failed to toggle favorite: " + albumId);
    return;
  }
  const element = document.getElementById(albumId);
  if (!element) {
    console.log("Element not found: " + albumId);
    return;
  }

  const button = element.querySelector("button");
  if (!button) {
    console.log("Button not found: " + albumId);
    return;
  }

  const dataChecked = button.getAttribute("data-checked");
  if (dataChecked === "true") {
    button.removeAttribute("data-checked");
    innerHTML = element.querySelector(".search_result_stars")?.innerHTML;
    if (innerHTML) {
      element.querySelector(".search_result_stars").innerHTML =
        Number(innerHTML) - 1;
    }
  } else {
    button.setAttribute("data-checked", "true");
    innerHTML = element.querySelector(".search_result_stars")?.innerHTML;
    if (innerHTML) {
      element.querySelector(".search_result_stars").innerHTML =
        Number(innerHTML) + 1;
    }
  }
}

function goToPage(page) {
  const url = new URL(window.location.href);
  url.searchParams.set("page", page);
  window.location.href = url.toString();
}
