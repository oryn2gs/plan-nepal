const progressBar = document.getElementById("progress-bar");
const formContainer = document.getElementById("form-section");
const forms = formContainer.querySelectorAll(".form");
const formButtons = formContainer.querySelectorAll("button");

let currentStepIndex = 0;
let formContainerWidth = forms[0].clientWidth;

// Set the form container width on every resize
window.addEventListener("resize", () => {
  formContainerWidth = forms[0].clientWidth;
});

const createSteps = () => {
  forms.forEach((form, idx) => {
    const stepWrapper = document.createElement("div");
    stepWrapper.classList.add("step-wrapper");
    stepWrapper.innerHTML = `<p class="step">${idx + 1}</p>`;
    progressBar.appendChild(stepWrapper);
  });
};

const toggleForm = () => {
  formContainer.style.transform = `translateX(-${
    currentStepIndex * formContainerWidth
  }px)`;
  const progressTracker = progressBar.querySelector(".progress-tracker");

  // Set the width based on the current step index
  const widthPercentage = currentStepIndex === 0 ? 0 : currentStepIndex * 50;
  progressTracker.style.width = `${widthPercentage}%`;

  toogleSteps();
};

const toogleSteps = () => {
  const steps = document.querySelectorAll(".step");

  steps.forEach((step, idx) => {
    idx <= currentStepIndex
      ? step.classList.add("complete")
      : step.classList.remove("complete");
  });
};

// * fields validation
const validateField = (field) => {
  const parentElem = field.closest(".form-set");
  let fieldValid = field.value !== "";
  if (!fieldValid) {
    parentElem.classList.add("invalid");
    parentElem.nextElementSibling.classList.remove("hidden");
  } else {
    parentElem.classList.remove("invalid");
    parentElem.nextElementSibling.classList.add("hidden");
  }
  return fieldValid;
};

// * user form validation
const validateUserForm = () => {
  let userFormValid = false;
  const firstname = document.getElementById("id_firstname");
  const lastname = document.getElementById("id_lastname");
  const dateOfBirth = document.getElementById("id_date_of_birth");
  const gender = document.getElementById("id_gender");
  const country = document.getElementById("id_country");
  const countryCode = document.getElementById("id_country_code");
  const phoneNumber = document.getElementById("id_phone_number");

  const userFormFields = [
    firstname,
    lastname,
    dateOfBirth,
    gender,
    country,
    countryCode,
    phoneNumber,
  ];
  userFormFields.forEach((field, _) => {
    userFormValid = validateField(field);
    if (!userFormValid) return userFormValid;
  });
  return userFormValid;
};

// * Booking form validation
const validateBookingForm = () => {
  let bookingFormValid = false;
  const adults = document.getElementById("id_adults");
  const arrivalDate = document.getElementById("id_arrival_date");
  const arrivalTime = document.getElementById("id_arrival_time");
  const airlines = document.getElementById("id_airlines");
  const flightNumber = document.getElementById("id_flight_number");
  const bookingsFormFields = [
    adults,
    arrivalDate,
    arrivalTime,
    airlines,
    flightNumber,
  ];

  bookingsFormFields.forEach((field, _) => {
    bookingFormValid = validateField(field);
    if (!bookingFormValid) return bookingFormValid;
  });
  return bookingFormValid;
};

formButtons.forEach((button) => {
  if (button.type !== "submit") {
    button.addEventListener("click", () => {
      if (button.id === "user_profile_button") {
        if (validateUserForm()) {
          currentStepIndex += 1;
          toggleForm();
        }
      }
      if (button.id === "booking_form_button") {
        if (validateBookingForm()) {
          currentStepIndex += 1;
          toggleForm();
        }
      }
    });
  }
});

progressBar.addEventListener("click", (e) => {
  if (!e.target.classList.contains("step")) return;
  currentStepIndex = parseInt(e.target.textContent) - 1;
  toggleForm();
});

createSteps();

// const progressBar = document.getElementById("progress-bar");
// const formContainer = document.getElementById("form-section");
// const forms = formContainer.querySelectorAll(".form");
// const formButtons = formContainer.querySelectorAll("button");

// let currentStepIndex = 0;
// let formContainerWidth = forms[0].clientWidth;

// // Set the form container width on every resize
// window.addEventListener("resize", () => {
//   formContainerWidth = forms[0].clientWidth;
// });

// const createSteps = () => {
//   forms.forEach((form, idx) => {
//     const stepWrapper = document.createElement("div");
//     stepWrapper.classList.add("step-wrapper");
//     stepWrapper.innerHTML = `<p class="step">${idx + 1}</p>`;
//     progressBar.appendChild(stepWrapper);
//   });
// };

// const toggleForm = () => {
//   formContainer.style.transform = `translateX(-${
//     currentStepIndex * formContainerWidth
//   }px)`;
//   const progressTracker = progressBar.querySelector(".progress-tracker");

//   // Set the width based on the current step index
//   const widthPercentage = currentStepIndex === 0 ? 0 : currentStepIndex * 50;
//   progressTracker.style.width = `${widthPercentage}%`;

//   toogleSteps();
// };

// const toogleSteps = () => {
//   const steps = document.querySelectorAll(".step");

//   steps.forEach((step, idx) => {
//     idx <= currentStepIndex
//       ? step.classList.add("complete")
//       : step.classList.remove("complete");
//   });
// };

// formButtons.forEach((button) => {
//   if (button.type !== "submit") {
//     // check if the button is user_profile_button
//     // if so check the field the fiedls related to user
//     button.addEventListener("click", () => {
//       currentStepIndex += 1;
//       toggleForm();
//     });
//   }
// });

// progressBar.addEventListener("click", (e) => {
//   if (!e.target.classList.contains("step")) return;
//   currentStepIndex = parseInt(e.target.textContent) - 1;
//   toggleForm();
// });

// createSteps();
