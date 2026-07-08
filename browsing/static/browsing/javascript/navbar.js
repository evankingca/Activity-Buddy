function navbar_scrollbar() {
    let prevScrollPos = window.pageYOffset;
    const header = document.getElementById("header")
    window.addEventListener("scroll", () => {
        let currentScrollPos = window.pageYOffset;
        if (prevScrollPos > currentScrollPos) {
            header.classList.add("top-0");
            header.classList.remove("-top-24");
        } else {
            header.classList.add("-top-24");
            header.classList.remove("top-0");
        }
        prevScrollPos = currentScrollPos;
    });
}

window.addEventListener("load", navbar_scrollbar());