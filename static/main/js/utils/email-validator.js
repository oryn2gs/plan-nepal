const emailInputField = document.getElementById("id_email");
emailInputField.addEventListener("blur", (event) => {
  const inputField = event.target;
  const parentElem = inputField.parentElement;
  let fieldValid = inputField.validity.valid && inputField.value !== "";
  if (!fieldValid) {
    parentElem.classList.add("invalid");
    parentElem.nextElementSibling.classList.remove("hidden");
  } else {
    parentElem.classList.remove("invalid");
    parentElem.nextElementSibling.classList.add("hidden");
  }
});
