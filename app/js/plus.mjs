const API = window["electronAPI"];

const fetchUserId = async () => {
  try {
    const response = await API.fetchUserId();
    return response.user_id;
  } catch (error) {
    console.error("Failed to fetch user_id:", error);
    throw error;
  }
};

// Handle tab clicks to load respective views.
document.getElementById("aboutPage").addEventListener("click", () => {
  API.loadAboutView();
});

document.getElementById("searchPage").addEventListener("click", () => {
  API.loadSearchView();
});

// Highlight selected special characters.
document.querySelectorAll(".spec-char-li").forEach(li => {
  li.addEventListener("click", () => {
    li.classList.toggle("selected");
  });
});

// Handle form submission for adding a password.
document.getElementById("addPasswordForm").addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent the default form submission.

  const site_name = document.getElementById("websiteInput").value;
  const account_name = document.getElementById("emailInput").value;
  const password = document.getElementById("passwordInput").value;
  const confirmPassword = document.getElementById("confirmPasswordInput").value;

  // Check if password matches confirm password.
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  // Send data to backend to add the password.
  if (API) {
    try {
      const user_id = await fetchUserId();
      await API.addPassword({user_id, site_name, account_name, password});
    } catch (error) {
      console.error("Failed to add password:", error);
    }
  } else {
    console.error("electronAPI is not available");
  }
});

// Update label when pwLength input changes.
const pwLengthInput = document.querySelector("input[name='pwLength']");
const rangeLabel = document.getElementById("rangeLabel");

pwLengthInput.addEventListener("input", (event) => {
  const value = event.target.value;
  const labelTextNode = rangeLabel.firstChild;

  // Update the text node with the new value.
  if (labelTextNode) {
    labelTextNode.nodeValue = value;
  } else {
    rangeLabel.textContent = value;
  }
});

// Handle generate random password.
document.getElementById("generatePasswordButton").addEventListener("click", () => {
  const specChars = Array.from(document.querySelectorAll(".spec-char-li"))
    .filter(li => li.classList.contains("selected"))
    .map(li => li.getAttribute("value"))
    .join("");
  const pwLength = document.querySelector("input[name='pwLength']").value;

  // Send data to backend to generate a random password.
  if (API) {
    API.generateRandomPassword({ specChars, pwLength });
  } else {
    console.error("electronAPI is not available");
  }
});


// Listen for the backend responses.
if (API) {
  API.onAddPasswordSuccess((event, message) => {
    alert("Password added successfully!");
    document.getElementById("addPasswordForm").reset();
  });

  API.onAddPasswordFailure((event, message) => {
    alert(`Failed to add password: ${message}`);
  });

  API.onGenerateRandomPasswordSuccess((event, { password }) => {
    document.getElementById("passwordInput").value = password;
    document.getElementById("confirmPasswordInput").value = password;
  });

  API.onGenerateRandomPasswordFailure((event, message) => {
    alert(`Failed to generate password: ${message}`);
  });
} else {
  console.error("Electron APIs are not available.");
}
