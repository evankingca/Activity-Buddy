const navbar = document.getElementById("navbar")
const bergieMenu = document.getElementById("bergieMenu")

function navbar_scrollbar() {
    let prevScrollPos = window.pageYOffset;
    const header = document.getElementById("header")
    window.addEventListener("scroll", () => {
        let currentScrollPos = window.pageYOffset;
        if (!navbar.classList.contains("collapsed")) {
            navbar.classList.add("collapsed")
        }
        if (prevScrollPos > currentScrollPos) {
            header.classList.add("top-0");
            header.classList.remove("-top-28");
        } else {
            header.classList.add("-top-28");
            header.classList.remove("top-0");
        }
        prevScrollPos = currentScrollPos;
    });
}

window.addEventListener("load", navbar_scrollbar());

bergieMenu.addEventListener("click", () => {
    if (navbar.classList.contains("collapsed")) {
        navbar.classList.remove("collapsed")
    } else {
        navbar.classList.add("collapsed")
    }
})