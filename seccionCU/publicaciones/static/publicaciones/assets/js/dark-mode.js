let darkMode = localStorage.getItem("darkMode");

const darkModeToggle = document.querySelector("#dark-mode-toggle");

const enableDarkMode = () => {
  document.body.classList.add("dark-mode");
  localStorage.setItem("darkMode", "enabled");
  
};

const disableDarkMode = () => {
  document.body.classList.remove("dark-mode");
  localStorage.removeItem("darkMode");
  
};

darkModeToggle.addEventListener("click", () => {
  darkMode = localStorage.getItem("darkMode");
  if (darkMode !== "enabled") {
    enableDarkMode();
    console.log(darkMode);
  } else {
    disableDarkMode();
    console.log(darkMode);
  }
});

darkMode = localStorage.getItem("darkMode");
if (darkMode === "enabled") {
  enableDarkMode();
  console.log(darkMode);
} else {
  disableDarkMode();
  console.log(darkMode);
}