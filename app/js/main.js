const { ipcMain } = require('electron');
const { spawn } = require('child_process');
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadFile('app/index.html');
}

app.whenReady().then(createWindow);

ipcMain.on('register', (event, userData) => {
  const pythonScriptPath = path.join(__dirname, '../../py/main.py');
    const pyProcess = spawn('python', [pythonScriptPath, 'register_user', userData.username, userData.password]);

    pyProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });
  
  pyProcess.on('close', (code) => {
      console.log(`Python script exited with code ${code}`);
  });
    
    pyProcess.stdout.on('data', (data) => {
      event.reply('register-reply', data.toString());
    });
});

ipcMain.on('login', (event, userData) => {
  const pythonScriptPath = path.join(__dirname, '../../py/main.py');
    const pyProcess = spawn('python', [pythonScriptPath, 'login_user', userData.username, userData.password]);

    pyProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });
  
  pyProcess.on('close', (code) => {
      console.log(`Python script exited with code ${code}`);
  });
    
    pyProcess.stdout.on('data', (data) => {
      event.reply('login-reply', data.toString());
    });
});