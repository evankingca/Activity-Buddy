const darkMode = document.getElementById("darkMode")
const root = document.documentElement
darkMode.addEventListener("change", (e) => {
    if (event.target.checked) {
        // using "true" as localstorage doesn't support non-strings
        localStorage.setItem("darkMode", "true");
        root.classList.add("dark")
    } else {
        localStorage.setItem("darkMode", "false");
        root.classList.remove("dark");
    }
})


window.addEventListener("load", () => {
    let darkModeEnabled = localStorage.getItem("darkMode");
    if (darkModeEnabled === "true") {
        darkMode.checked = darkModeEnabled;
        root.classList.add("dark")
    }
});
