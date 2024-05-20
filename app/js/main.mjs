import { ipcMain, app, BrowserWindow } from 'electron';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Define __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


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
    }
    // Uncomment if you want to hide the title bar:
    // titleBarStyle: 'hidden'
  });
  mainWindow.loadFile('app/views/login-register.html');
  // Uncomment to open the DevTools:
  // mainWindow.webContents.openDevTools();
}

ipcMain.on('loadPlusView', () => {
  if (mainWindow) {
    mainWindow.loadFile('app/views/plus.html');
  } else {
    console.error('Main window is not available.');
  }
});

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
  const pyProcess = spawn('python', [pythonScriptPath, 'register_user', userData.email, userData.password]);

  pyProcess.stdout.on('data', (data) => {
    const response = JSON.parse(data.toString());
    if (response.status === 'success') {
      event.reply('register-success', 'User registered successfully');
    } else {
      event.reply('register-failure', response.message);
    }
  });

  pyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
});

ipcMain.on('login', (event, userData) => {
  const pythonScriptPath = path.join(__dirname, '../../py/main.py');
  const pyProcess = spawn('python', [pythonScriptPath, 'login_user', userData.email, userData.password]);

  pyProcess.stdout.on('data', (data) => {
    const response = JSON.parse(data.toString());
    if (response.status === 'success') {
      event.reply('login-success', 'User logged in successfully');
    } else {
      event.reply('login-failure', response.message);
    }
  });

  pyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
});