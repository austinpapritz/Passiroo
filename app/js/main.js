const { ipcMain } = require('electron');
const { spawn } = require('child_process');
const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 512,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false
    },
    titleBarStyle: 'hidden'
  });
  mainWindow.loadFile('app/views/register.html');
}

ipcMain.on('resize-window', (event, { width, height }) => {
  mainWindow.setContentSize(width, height);
  // Optional: Center the window again after resizing
  mainWindow.center();
});

app.on('ready', createWindow);

ipcMain.on('close-window', () => {
  mainWindow.close();
});

ipcMain.on('minimize-window', () => {
  mainWindow.minimize();
});

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