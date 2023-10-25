const btnPrevTestimonial = document.getElementById("btn-prev__testimonial");
const btnNextTestimonial = document.getElementById("btn-next__testimonial");
const testimonialTrack = document.getElementById("testimonial-track");

btnNextTestimonial.addEventListener("click", (e) => {
  testimonialTrack.scrollLeft = testimonialTrack.scrollLeft + 300;
});

btnPrevTestimonial.addEventListener("click", (e) => {
  testimonialTrack.scrollLeft = testimonialTrack.scrollLeft - 300;
});
