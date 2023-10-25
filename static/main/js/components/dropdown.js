const dropdownBtn = document.getElementById("dropdown-btn");
const dropdownMenu = document.getElementById("dropdown-menu");

if (dropdownBtn && dropdownMenu) {
  let dropdownOpen = false;
  dropdownBtn.addEventListener("click", (e) => {
    if (!dropdownOpen) {
      dropdownMenu.style.display = "block";
      dropdownOpen = true;
    } else {
      dropdownMenu.style.display = "none";
      dropdownOpen = false;
    }
  });
}
