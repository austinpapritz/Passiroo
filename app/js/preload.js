// This file makes it so only necessary Node.js functions are exposed
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendRegister: (data) => ipcRenderer.send('register', data),
  onRegisterReply: (callback) => ipcRenderer.on('register-reply', callback)
});
