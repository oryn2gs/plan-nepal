const selectInput = document.getElementById("inquiry_type");
const menuToggler = document.getElementById("select-menu__toggler");

menuToggler.addEventListener("click", (e) => {
  if (menuToggler.classList.contains("active")) {
    toggleMenu(menuToggler, "add");
    return;
  }

  toggleMenu(menuToggler, "remove");

  const options = document.querySelectorAll(".options-menu li");

  options.forEach((option) => {
    option.addEventListener("click", (e) => {
      const selectedValue = option.innerText;
      selectInput.value = selectedValue;
      toggleMenu(menuToggler, "add");
    });
  });
});

const toggleMenu = (toggleBtn = null, type = "remove") => {
  const customSelect = menuToggler.previousElementSibling;

  const selectMenu = customSelect.querySelector(".options-menu");
  if (type === "add") {
    selectMenu.classList.add("hidden");
    toggleBtn.classList.remove("active");
  } else {
    selectMenu.classList.remove("hidden");
    toggleBtn.classList.add("active");
  }
};
