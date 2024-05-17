// Disable form submit if there are any invalid fields.
(function() {
  'use strict';
  window.addEventListener('load', function() {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

// Grab content size to resize window.
document.addEventListener('DOMContentLoaded', () => {
  const width = document.documentElement.clientWidth;
  const height = document.documentElement.clientHeight;

  if (window['electronAPI']) {
    window['electronAPI'].resizeWindow(width, height);
  } else {
    console.error('electronAPI is not available');
  }
});

document.getElementById('registerButton').addEventListener('click', () => {
  const email = document.getElementById('emailInput').value;
  const password = document.getElementById('passwordInput').value;

  if (window['electronAPI']) {
    window['electronAPI'].sendRegister({ email, password });
  } else {
    console.error('electronAPI is not available');
  }
});

if (window['electronAPI']) {
  window['electronAPI'].onRegisterReply((event, response) => {
    //pull in function from main.js that will create a login window
  });
} else {
  console.error('electronAPI is not available');
}

document.getElementById('loginButton').addEventListener('click', () => {
  const email = document.getElementById('emailInput').value;
  const password = document.getElementById('passwordInput').value;

  if (window['electronAPI']) {
    window['electronAPI'].sendRegister({ email, password });
  } else {
    console.error('electronAPI is not available');
  }
});