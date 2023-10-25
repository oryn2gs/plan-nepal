const timeline = document.getElementById("timeline");
const line = timeline.querySelector("#line");

const events = ["DOMContentLoaded", "resize"];

events.forEach((e) => {
  window.addEventListener(e, () => adjustLineHeight());
});

function adjustLineHeight() {
  const timelineHeight = timeline.clientHeight;

  const spacing =
    window.innerWidth >= 744 ? timelineHeight - 100 : timelineHeight - 140;

  line.style.height = `${spacing}px`;
}
