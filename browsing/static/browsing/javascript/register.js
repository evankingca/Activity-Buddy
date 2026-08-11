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

  // Call the backend endpoint to handle the call to Google Places
  // This ensures the Google API key is not exposed to client-side.
  try {
    const response = await fetch("/text-search/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ query: query }),
    });

    // This should return an array of Place objects from Google Places:
    const data = await response.json();

    // Create document fragment for adding all the checkboxes:
    const fragment = document.createDocumentFragment();

    // Check to see if data.places contains data:
    if (!Array.isArray(data.places)) {
      throw new Error("No valid locations results returned from Google Places API.");
    }

    // Get all results by looping over the "places" array in the response:
    data.places.forEach(place => {
      const hr = document.createElement("hr");
      hr.classList.add("mb-1")

      const displayNameSpan = document.createElement("span");
      const separatorSpan = document.createElement("span");
      const addressSpan = document.createElement("span");
      displayNameSpan.classList.add("font-bold")
      displayNameSpan.textContent = place.displayName.text
      separatorSpan.textContent = " | "
      addressSpan.textContent = place.formattedAddress

      const placeDiv = document.createElement("div");

      const placeCheckbox = document.createElement("input");
      placeCheckbox.type = "checkbox";
      placeCheckbox.id = place.id;
      placeCheckbox.name = "location";
      placeCheckbox.value = place.id;
      placeCheckbox.classList.add("mr-2")

      const placeLabel = document.createElement("label");
      placeLabel.htmlFor = place.id;
      placeLabel.append(displayNameSpan, separatorSpan, addressSpan)

      placeDiv.append(hr)
      placeDiv.append(placeCheckbox);
      placeDiv.append(placeLabel);

      fragment.append(placeDiv);
    })
    searchResults.innerHTML = ""; // Clear previous results
    searchResults.append(fragment); // Add new results

  } catch (error) {
    showError(error.message);
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

  const location_ids = document.querySelectorAll('input[name="location"]:checked');
  const checkedLocations = Array.from(location_ids).map((cl) => cl.value);

  const preferences = {
    experience: document.getElementById("experience").value,
    goals: checkedGoals,
    training_styles: checkedTraining,
    gym_frequency: document.getElementById("frequency").value,
    preferred_workout_times: checkedTimes,
    location_ids: checkedLocations,
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

    requireAtLeastOne("location", "Select at least one preferred location.");

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
