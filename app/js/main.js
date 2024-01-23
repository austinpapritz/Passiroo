const { ipcMain } = require('electron');
const { spawn } = require('child_process');

new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'preload.js'),
  }
});

ipcMain.on('register', (event, userData) => {
    const pyProcess = spawn('python', ['py/main.py', 'register_user', userData.username, userData.password]);
    
    pyProcess.stdout.on('data', (data) => {
        event.reply('register-reply', data.toString());
    });
});