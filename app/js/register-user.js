document.getElementById('registerButton').addEventListener('click', () => {
  const username = document.getElementById('usernameInput').value;
  const password = document.getElementById('passwordInput').value;

  if (window['electronAPI']) {
    window['electronAPI'].sendRegister({ username, password });
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

if (window['electronAPI']) {
  window['electronAPI'].setupWindowControls();
}