const registerForm = document.getElementById("register-form");
const errorElement = document.getElementById("register-error");

registerForm.addEventListener("submit", async(event)=>{
event.preventDefault();

function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.remove("hidden");
    console.log(errorElement.textContent);;
}


function requireAtLeastOne(name, message) {
    const checked = registerForm.querySelectorAll(
        `input[name="${name}"]:checked`
    );

    if (checked.length === 0) {
        showError(message);
        throw new Error(message);
    }
}

requireAtLeastOne(
    "goals",
    "Select at least one goal."
);

requireAtLeastOne(
    "training",
    "Select at least one training style."
);

requireAtLeastOne(
    "time",
    "Select at least one preferred workout time."
);

  const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const goals = document.querySelectorAll('input[name="goals"]:checked');
    const checkedGoals = Array.from(goals).map(cg=>cg.value);

    const training = document.querySelectorAll('input[name="training"]:checked');
    const checkedTraining = Array.from(training).map(ct=>ct.value);

    const times = document.querySelectorAll('input[name="time"]:checked');
    const checkedTimes = Array.from(times).map(ct=>ct.value);

    const preferences = {
      experience: document.getElementById("experience").value,
      goals: checkedGoals,
      training_styles: checkedTraining,
      gym_frequency: document.getElementById("frequency").value,
      preferred_workout_times: checkedTimes,
    };

    const registrationData = {
        username,
        password,
        display_name: document.getElementById("username").value.trim(),
        email: document.getElementById("email").value,
        bio_text: document.getElementById("summary").value,
        preferences
    }

    try{
    const response = await fetch("/auth/signup/", {

        method: "POST",
        credentials: "same-origin",
        headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                },
        body: JSON.stringify(registrationData)
    });

    const text = await response.json();
    console.log(text);

    window.location.href = "/user";
        
    }catch(error){
        showError(error.message);
    }

    });
