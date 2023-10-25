import { validatePassword } from "../utils/password-validator.js";

const emailInputField = document.getElementById("email");
const passwordInputField = document.getElementById("password");
const confirmPasswordInputField = document.getElementById("confirm_password");

let password = ""; // used to validate confirm password
console.log(emailInputField, passwordInputField, confirmPasswordInputField);

const validateField = (event) => {
  const inputField = event.target;
  const parentElem = inputField.parentElement;
  let passwordValid;
  let confirmPasswordValid;
  let fieldValid = inputField.validity.valid;

  if (inputField === passwordInputField) {
    passwordValid = validatePassword(inputField.value);
    password = inputField.value;
    fieldValid = inputField.validity.valid && passwordValid;
  }

  if (inputField === confirmPasswordInputField) {
    confirmPasswordValid = inputField.value === password;
    fieldValid = inputField.validity.valid && confirmPasswordValid;
  }

  if (!fieldValid) {
    parentElem.classList.add("invalid");
    parentElem.nextElementSibling.classList.remove("hidden");
  } else {
    parentElem.classList.remove("invalid");
    parentElem.nextElementSibling.classList.add("hidden");
  }
};

const formFields = [
  emailInputField,
  passwordInputField,
  confirmPasswordInputField,
];

formFields.forEach((field) =>
  field.addEventListener("blur", (event) => validateField(event))
);
