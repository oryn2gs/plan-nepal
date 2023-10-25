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
