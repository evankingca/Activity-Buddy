const registerForm = document.getElementById("register-form");
const errorElement = document.getElementById("register-error");

// Setting up the search form and adding the search results to the Register form:
const searchButton = document.getElementById("locationSearchButton");
const searchInput = document.getElementById("locationSearch");
const searchResults = document.getElementById("locationSearchResults");

searchButton.addEventListener("click", async (event) => {
  event.preventDefault();
  clearError();

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const query = searchInput.value.trim();

  // Check that query is not empty; WIP: to change into a proper error message
  if (query === "") {
    console.log("Please enter a search term.");
  } else {
    // Add the search term "gyms" to the user input; no effects if it is duplicated:
    const fullQuery = query + " gyms"

    // Then call the backend endpoint to handle the call to Google Places
    // This ensures the Google API key is not exposed to client-side.
    try {
      const response = await fetch("/text-search/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ query: fullQuery }),
    });

    // This should return an array of Place objects from Google Places:
    const data = await response.json();

    // Create document fragment for adding all the checkboxes:
    const fragment = document.createDocumentFragment();

    // Get all results by looping over the "places" array in the response:
    data.places.forEach(place => {
      const displayText = place.displayName.text + " / " + place.formattedAddress;

      const placeDiv = document.createElement("div");

      const placeCheckbox = document.createElement("input");
      placeCheckbox.type = "checkbox";
      placeCheckbox.id = place.id;
      placeCheckbox.name = "location";
      placeCheckbox.value = place.id;

      const placeLabel = document.createElement("label");
      placeLabel.for = place.id;
      placeLabel.textContent = displayText;

      placeDiv.append(placeCheckbox);
      placeDiv.append(placeLabel);

      fragment.append(placeDiv);
    })
    searchResults.innerHTML = ""; // Clear previous results
    searchResults.append(fragment); // Add new results

    } catch (error) {
      showError(error.message);
    }
  }
});

// Handling of the register form itself:
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

    window.location.href = "/user";
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
