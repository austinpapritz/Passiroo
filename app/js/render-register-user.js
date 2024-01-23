document.getElementById('registerButton').addEventListener('click', () => {
  const username = document.getElementById('usernameInput').value;
  const password = document.getElementById('passwordInput').value;
  
  const log = document.getElementById('log');
  log.innerHTML = "Ok";

  if (window['electronAPI']) {
    window['electronAPI'].sendRegister({ username, password });
  } else {
    console.error('electronAPI is not available');
  }
});

if (window['electronAPI']) {
  window['electronAPI'].onRegisterReply((event, response) => {
    return
  });
} else {
  console.error('electronAPI is not available');
}