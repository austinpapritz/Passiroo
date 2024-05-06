// This file makes it so that only necessary Node.js functions are exposed
const { contextBridge, ipcRenderer } = require('electron');
const utilities = require('./utilities.js');

contextBridge.exposeInMainWorld('electronAPI', {
  sendRegister: (data) => ipcRenderer.send('register', data),
  onRegisterReply: (callback) => ipcRenderer.on('register-reply', callback),
  setupWindowControls: utilities.setupWindowControls,
  resizeWindow: (width, height) => {
    ipcRenderer.send('resize-window', { width, height });
  }
});
