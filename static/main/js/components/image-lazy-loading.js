const imageContainer = document.querySelectorAll(".blur-load");

imageContainer.forEach((container, _) => {
  let img = container.querySelector("img");
  let url = img.src;
  let modifiedUrl = url.replace(/\.png$/, "-small.png");
  container.style.backgroundImage = `url(${modifiedUrl})`;

  function loaded() {
    container.classList.add("loaded");
  }
  if (img.complete) {
    loaded();
  } else {
    img.addEventListener("load", loaded);
  }
});
