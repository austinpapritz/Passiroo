// This file makes it so that only necessary Node.js functions are exposed
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  resizeWindow: (width, height) => ipcRenderer.send('resize-window', { width, height }),
  sendRegister: (data) => ipcRenderer.send('register', data),
  onRegisterReply: (callback) => ipcRenderer.on('register-reply', callback),
  sendLogin: (data) => ipcRenderer.send('login', data),
  onLoginReply: (callback) => ipcRenderer.on('login-reply', callback)
});
