const passwordInputField = document.getElementById("id_password");

passwordInputField.addEventListener("blur", (event) => {
  const inputField = event.target;
  const parentElem = inputField.parentElement;
  let fieldValid = inputField.value !== "";
  if (!fieldValid) {
    parentElem.classList.add("invalid");
    parentElem.nextElementSibling.classList.remove("hidden");
  } else {
    parentElem.classList.remove("invalid");
    parentElem.nextElementSibling.classList.add("hidden");
  }
});
