document.addEventListener("DOMContentLoaded", (e) => {
  const faqTypeBtns = document.querySelectorAll(".btn-pill");

  faqTypeBtns.forEach((btn, _) => {
    btn.addEventListener("click", (e) => {
      removeActiveClass(faqTypeBtns); // remove the active class other butn

      btn.classList.add("active");
      const queryStr = btn.innerText;
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
  const faqWrapper = document.getElementById("faq-wrapper");

  fetch(`/booking/faq/filter/?query=${queryStr}`)
    .then((response) => response.text())
    .then((data) => {
      faqWrapper.innerHTML = data;
    })
    .catch((error) => (faqWrapper.innerHTML = error));
};
