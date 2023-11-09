const passwordInputField = document.getElementById("id_password");
const confirmPasswordInputField = document.getElementById(
  "id_confirm_password"
);

let password = "";

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

const formFields = [passwordInputField, confirmPasswordInputField];

formFields.forEach((field) =>
  field.addEventListener("blur", (event) => validateField(event))
);

export const validatePassword = (password) => {
  const patterns =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
  const passwordValid = password.length > 8 && patterns.test(password);

  if (!passwordValid) return false;
  return true;
};
