const darkMode = document.getElementById("switchThemeButton")
const darkModeIcon = document.getElementById("switchThemeButtonIcon")
const root = document.documentElement
darkMode.addEventListener("click", (e) => {
    console.log("woo")
    const darkModeEnabled = localStorage.getItem("darkMode");
    // using "true" as localstorage doesn't support non-strings
    localStorage.setItem("darkMode", darkModeEnabled === "true" ? "false" : "true");
    if (darkModeEnabled === "true") {
        root.classList.remove("dark")
        darkModeIcon.textContent = "light_mode"
    } else {
        root.classList.add("dark")
        darkModeIcon.textContent = "dark_mode"
    }
})


window.addEventListener("load", () => {
    let darkModeEnabled = localStorage.getItem("darkMode");
    if (darkModeEnabled === "true") {
        darkMode.checked = darkModeEnabled;
        root.classList.add("dark")
    }
});
