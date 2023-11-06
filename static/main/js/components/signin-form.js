const loginInputField = document.getElementById("email");
const passwordInputField = document.getElementById("password");

const loginBtn = document.getElementById("login_button");

const validateField = (event) => {
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
};

const formFields = [loginInputField, passwordInputField];

formFields.forEach((field, _) => {
  field.addEventListener("blur", (event) => validateField(event));
});
