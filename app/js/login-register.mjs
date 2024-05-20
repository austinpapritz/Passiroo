const API = window['electronAPI'];

// Disable form submit if there are any invalid fields.
(function() {
  'use strict';
  window.addEventListener('load', function() {
    let q;
    document.getElementsByID('loginButton').addEventListener('Click') = () => {
      q = "login"
    }
    document.getElementsByID('registerButton').addEventListener('Click') = () => {
      q = "register"
    }
    var form = document.getElementsByClassName('needs-validation');
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
          return;
        } else {
          if (q === "register") {
            handleRegister(event);
          } else if (q === "register") {
            handleLogin(event);
          }
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);


// Handle login.
document.getElementById('loginButton').addEventListener('click', (e) => {
  e.preventDefault();
  const email = document.getElementById('emailInput').value;
  const password = document.getElementById('passwordInput').value;

  if (API) {
    if (email && password) {
      API.sendLogin({ email, password });
    } else {
      console.error('please provide a valid email and password')
    }
  } else {
    console.error('electronAPI is not available');
  }
});


// Handle register.
document.getElementById('registerButton').addEventListener('click', (e) => {
  e.preventDefault();

  const email = document.getElementById('emailInput');
  const confirmPassword = document.getElementById('confirmPasswordInput');
  const password = document.getElementById('passwordInput');
  const errorH3 = document.getElementById('error-msg');

  // Ensure confirmPasswordInput is required
  confirmPassword.setAttribute("required", "");

  // Check if the password matches the confirm password.
  if (passwordInput.value !== confirmPasswordInput.value) {
    // If they don't match, add Bootstrap's is-invalid class to show the error.
    confirmPassword.classList.add('is-invalid');
    errorH3.innerHTML = "Passwords do not match."; // Assumes there is a div for feedback immediately following the input.
    return; // Stop the function from proceeding.
  } else {
    // If they match, remove any invalid class that might have been added previously.
    confirmPassword.classList.remove('is-invalid');

    if (API) {
      if (email.value && password.value) {
        API.sendRegister({ email: email.value, password: password.value });
      } else {
        console.error('please enter a valid email and password')
      }
    } else {
      console.error('electronAPI is not available');
    }
  }; 
});



if (API) {
  const errorH3 = document.getElementById('error-msg')

  API.onRegisterSuccess((event, message) => {
    console.log(message);
    API.loadPlusView();
  });

  API.onRegisterFailure((event, message) => {
    (message); // Handle registration failure
    errorH3.innerHTML = message;
  });

  API.onLoginSuccess((event, message) => {
    API.loadPlusView();
  });

  API.onLoginFailure((event, message) => {
    console.log(message); // Handle login failure
    errorH3.innerHTML = message;
  });
} else {
  console.error('Electron APIs are not available.');
}