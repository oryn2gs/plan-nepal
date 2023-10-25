const faqAnswers = document.querySelectorAll(".faq-answer");

document.addEventListener("DOMContentLoaded", () => {
  const faqBtnsContainer = document.getElementById("faq-wrapper");

  faqBtnsContainer.addEventListener("click", (e) => {
    if (!e.target.closest(".btn-faq__toggler")) return;
    const targetNode = e.target.closest(".btn-faq__toggler");
    // ! check the button Text if it containes ""unresiolved" change the card icon to replay and toggle the form --Optional

    if (targetNode.classList.contains("active")) {
      toggleFaqCard((btn = targetNode), (type = "add"));
      return;
    }

    resetFaqCards(faqBtnsContainer.querySelectorAll(".btn-faq__toggler"));

    toggleFaqCard(targetNode);
  });
});

const toggleFaqCard = (btn = null, type = "remove") => {
  btn.classList.toggle("active");
  const parentElem = btn.closest(".faq-question__container");
  const nextSibling = parentElem.nextElementSibling;
  if (type === "add") {
    nextSibling.classList.add("hidden");
  } else {
    nextSibling.classList.remove("hidden");
  }
};

const resetFaqCards = (faqBtns) => {
  const activeBtn = Array.from(faqBtns).find((btn) =>
    btn.classList.contains("active")
  );
  const activeAnswer = Array.from(faqAnswers).find(
    (answer) => !answer.classList.contains("hidden")
  );

  if (activeBtn && activeAnswer) {
    activeBtn.classList.remove("active");
    activeAnswer.classList.add("hidden");
  }
};
// const faqAnswers = document.querySelectorAll(".faq-answer");

// document.addEventListener("DOMContentLoaded", () => {
//   const faqBtns = document.querySelectorAll(".btn-faq__toggler");

//   // need some ways to add a event listener to a button when the content is changes
//   //
//   faqBtns.forEach((btn, _) => {
//     btn.addEventListener("click", (e) => {
//       if (btn.classList.contains("active")) {
//         toggleFaqCard((btn = btn), (type = "add"));
//         return;
//       }

//       resetFaqCards(faqBtns); // closse active cards

//       toggleFaqCard((btn = btn));
//     });
//   });
// });

// const toggleFaqCard = (btn = null, type = "remove") => {
//   btn.classList.toggle("active");
//   const parentElem = btn.closest(".faq-question__container");
//   const nextSibling = parentElem.nextElementSibling;
//   if (type === "add") {
//     nextSibling.classList.add("hidden");
//   } else {
//     nextSibling.classList.remove("hidden");
//   }
// };

// const resetFaqCards = (faqBtns) => {
//   const activeBtn = Array.from(faqBtns).find((btn) =>
//     btn.classList.contains("active")
//   );
//   const activeAnswer = Array.from(faqAnswers).find(
//     (answer) => !answer.classList.contains("hidden")
//   );

//   if (activeBtn && activeAnswer) {
//     activeBtn.classList.remove("active");
//     activeAnswer.classList.add("hidden");
//   }
// };
