const logoutButton = document.getElementById("logout-btn");

if (logoutButton) {
    logoutButton.addEventListener("click", async (event) => {
        event.preventDefault();

        const csrfToken = document.querySelector(
            "#logout-csrf-form [name=csrfmiddlewaretoken]"
        ).value;

        const response = await fetch("/auth/logout/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrfToken,
            },
        });

        if (response.ok) {
            window.location.href = "/";
        }
    });
}