async function toggleFollow(username) {
  const response = await fetch("/api/users/follow", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username }),
  });

  if (response.ok) {
    const { isFollowing } = await response.json();
    const followButton = document.getElementById("follow_button");
    const followersNumber = document.getElementById("followers_number");

    if (isFollowing) {
      followButton.textContent = "Unfollow";
      followButton.classList.add("unfollow");
      followersNumber.textContent = parseInt(followersNumber.textContent) + 1;
    } else {
      followButton.textContent = "Follow";
      followButton.classList.remove("unfollow");
      followersNumber.textContent = parseInt(followersNumber.textContent) - 1;
    }
  }
}

async function toggleFavorite(albumId) {
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
  } else {
    button.setAttribute("data-checked", "true");
  }
}

async function handleSubmit(e) {
  console.log("handleSubmit");
  const form = document.getElementById("user_search");
  if (!form) {
    console.error("Form not found");
    return;
  }

  const formData = new FormData(form);
  console.dir(formData);
  const search = formData.get("username");
  if (!search) {
    console.error("No search term");
    return;
  }

  const url = new URL(window.location.href);
  url.pathname = `/user/${search}`;
  window.location.href = url.toString();
  e.preventDefault();
  e.stopPropagation();
}
