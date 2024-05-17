const { ipcMain } = require('electron');
const { spawn } = require('child_process');
const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 640,
    transparent: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
    },
    // Uncomment if you want to hide the title bar:
    titleBarStyle: 'hidden'
  });
  mainWindow.loadFile('app/views/register.html');
  // Uncomment to open the DevTools:
  // mainWindow.webContents.openDevTools();
}

ipcMain.on('resize-window', (event, { width, height }) => {
  if (mainWindow) { // Check if mainWindow is available
    mainWindow.setContentSize(width, height);
    mainWindow.center(); // Center the window after resizing
  } else {
    console.error("Error: mainWindow is not defined.");
  }
});

app.on('ready', createWindow);

ipcMain.on('register', (event, userData) => {
  const pythonScriptPath = path.join(__dirname, '../../py/main.py');
  const pyProcess = spawn('python', [pythonScriptPath, 'register_user', userData.username, userData.password]);

  pyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
  
  pyProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
    if (code === 0) {
      event.reply('register-success', 'User registered successfully');
    } else {
      event.reply('register-failure', 'Failed to register user');
    }
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
    if (code === 0) {
      event.reply('login-success', 'User logged in successfully');
    } else {
      event.reply('login-failure', 'Failed to log in');
    }
  });
});