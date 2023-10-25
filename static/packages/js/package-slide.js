const prevBtn = document.getElementById("btn-prev__package");
const nextBtn = document.getElementById("btn-next__package");
const slide = document.getElementById("package-slide");

// to fix -- disable the related button if the content if null

prevBtn.addEventListener("click", (e) => {
  slide.scrollLeft = slide.scrollLeft - 200;
});

nextBtn.addEventListener("click", (e) => {
  slide.scrollLeft = slide.scrollLeft + 200;
});
