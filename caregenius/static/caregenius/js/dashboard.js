const body = document.querySelector("body");
const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".toggle");
// const modeSwitch = document.querySelector(".toggle-switch");
// const modeText = document.querySelector(".mode-text");

// modeSwitch.addEventListener("click", () => {
//   body.classList.toggle("dark");
//   if (body.classList.contains("dark")) {
//     modeText.innerText = "Light mode";
//   } else {
//     modeText.innerText = "Dark mode";
//   }
// }

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
})