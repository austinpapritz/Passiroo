const API = window["electronAPI"];

// Disable form submit if there are any invalid fields.
(function() {
  "use strict";
  window.addEventListener("load", function() {
    var forms = document.getElementsByClassName("needs-validation");
    Array.prototype.filter.call(forms, function(form) {
      form.addEventListener("submit", function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      }, false);
    });
  }, false);
})();

// Handle login.
document.getElementById("loginButton").addEventListener("click", () => {
  const email = document.getElementById("emailInput").value;
  const password = document.getElementById("passwordInput").value;

  if (API) {
    API.sendLogin({ email, password });
  } else {
    console.error("electronAPI is not available");
  }
});

// Handle register.
document.getElementById("registerButton").addEventListener("click", (e) => {
  e.preventDefault();

  const emailInput = document.getElementById("emailInput");
  const confirmPasswordInput = document.getElementById("confirmPasswordInput");
  const passwordInput = document.getElementById("passwordInput");

  confirmPasswordInput.setAttribute("required", "");

  if (passwordInput.value !== confirmPasswordInput.value) {
    confirmPasswordInput.classList.add("is-invalid");
    confirmPasswordInput.nextElementSibling.innerHTML = "Passwords do not match.";
    return; 
  } else {
    confirmPasswordInput.classList.remove("is-invalid");
  }

  if (API) {
    API.sendRegister({ email: emailInput.value, password: passwordInput.value });
  } else {
    console.error("electronAPI is not available");
  }
});

if (API) {
  const errorLabel = document.getElementById("error-msg");

  API.onRegisterSuccess((event, message) => {
    console.log(message);
    API.loadPlusView();
  });

  API.onRegisterFailure((event, message) => {
    console.error(message);
    errorLabel.innerHTML = message;
  });

  API.onLoginSuccess((event, message) => {
    console.log(message);
    API.loadPlusView();
  });

  API.onLoginFailure((event, message) => {
    console.error(message);
    errorLabel.innerHTML = message;
  });
} else {
  console.error("Electron APIs are not available.");
}
