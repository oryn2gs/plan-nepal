document.addEventListener("DOMContentLoaded", function () {
  const messageContainer = document.getElementById("toast-messages");
  const messages = messageContainer.querySelectorAll("li.message");

  if (messageContainer && messages.length > 0) {
    messages.forEach(function (message) {
      setTimeout(function () {
        message.style.display = "none";
      }, 3000);
      const icon = message.querySelector("div.icon");
      icon.addEventListener("click", (e) => {
        message.style.display = "none";
      });
    });
  }
});
