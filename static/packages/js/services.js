document.addEventListener("DOMContentLoaded", (e) => {
  const servicesBtn = document.querySelectorAll(".btn-pill");

  servicesBtn.forEach((btn, _) => {
    btn.addEventListener("click", (e) => {
      removeActiveClass(servicesBtn);

      const targetNode = e.target;
      targetNode.classList.add("active");

      const queryStr = targetNode.innerText;
      sendRequest(queryStr);
    });
  });
});

const removeActiveClass = (btnArr = []) => {
  btnArr.forEach((btn, _) => {
    btn.classList.remove("active");
  });
};

const sendRequest = (queryStr) => {
  const cardContainer = document.getElementById("card-container");

  fetch(`/packages/filter/?query=${queryStr}`)
    .then((response) => response.text())
    .then((data) => {
      cardContainer.innerHTML = data;
    })
    // ! add error to django message.
    .catch((error) => (cardContainer.innerHTML = error));
};
