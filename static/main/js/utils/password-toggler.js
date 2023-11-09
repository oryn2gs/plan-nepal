// ! password toggler
const passwordToggler = document.querySelectorAll(".password-toggler");

if (passwordToggler) {
  passwordToggler.forEach((togglebtn) => {
    togglebtn.addEventListener("click", (e) => {
      console.log(235423);
      const passwordElem = togglebtn.previousElementSibling;
      if (!passwordElem) return;
      if (passwordElem.type === "password") {
        passwordElem.type = "text";
        togglebtn.innerHTML = `<i class="fa-solid fa-eye-slash"></i>`;
      } else {
        passwordElem.type = "password";
        togglebtn.innerHTML = `<i class="fa-solid fa-eye"></i>`;
      }
    });
  });
}

// ! adding a invalid to the the form-set related to the error
document.addEventListener("DOMContentLoaded", () => {
  const errorMessages = document.querySelectorAll(".field-error");
  console.log(errorMessages);
  if (errorMessages.length > 0) {
    errorMessages.forEach((message) => {
      if (!message.classList.contains("hidden")) {
        message.previousElementSibling.classList.add("invalid");
      }
    });
  }
});
