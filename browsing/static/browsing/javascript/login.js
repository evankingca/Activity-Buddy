const loginForm = document.getElementById("login-form");
const errorElement = document.getElementById("login-error");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    errorElement.classList.add("hidden");
    errorElement.textContent = "";

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    try {
        const response = await fetch("/auth/login/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            const message =
                data.non_field_errors?.[0] ||
                data.detail ||
                "Invalid username or password.";

            throw new Error(message);
        }

        window.location.href = "/user/";


    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove("hidden");
    }
});