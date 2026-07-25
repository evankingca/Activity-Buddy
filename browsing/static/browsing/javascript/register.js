const registerForm = document.getElementById("register-form");
const errorElement = document.getElementById("register-error");

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();

  const csrfToken = registerForm.querySelector(
    "[name=csrfmiddlewaretoken]",
  ).value;

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  const goals = document.querySelectorAll('input[name="goals"]:checked');
  const checkedGoals = Array.from(goals).map((cg) => cg.value);

  const training = document.querySelectorAll('input[name="training"]:checked');
  const checkedTraining = Array.from(training).map((ct) => ct.value);

  const times = document.querySelectorAll('input[name="time"]:checked');
  const checkedTimes = Array.from(times).map((ct) => ct.value);

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
    display_name: username,
    email: document.getElementById("email").value.trim(),
    bio_text: document.getElementById("summary").value.trim(),
    preferences,
  };

  try {
    requireAtLeastOne("goals", "Select at least one goal.");

    requireAtLeastOne("training", "Select at least one training style.");

    requireAtLeastOne("time", "Select at least one preferred workout time.");

    const response = await fetch("/auth/signup/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(registrationData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(getErrorMessage(data));
    }
  } catch (error) {
    showError(error.message);
  }
});

function showError(message) {
  errorElement.textContent = message;
  errorElement.classList.remove("hidden");
  console.log(errorElement.textContent);
}

function clearError() {
  errorElement.textContent = "";
  errorElement.classList.add("hidden");
}

function requireAtLeastOne(name, message) {
  const checked = registerForm.querySelectorAll(
    `input[name="${name}"]:checked`,
  );

  if (checked.length === 0) {
    throw new Error(message);
  }
}
function getErrorMessage(data) {
  for (const value of Object.values(data)) {
    if (Array.isArray(value) && value.length > 0) {
      return value[0];
    }

    if (typeof value === "object" && value !== null) {
      for (const nestedValue of Object.values(value)) {
        if (Array.isArray(nestedValue) && nestedValue.length > 0) {
          return nestedValue[0];
        }
      }
    }

    if (typeof value === "string") {
      return value;
    }
  }

  return "Registration failed. Please check your information.";
}
