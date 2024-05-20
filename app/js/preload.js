// This file makes it so that only necessary Node.js functions are exposed
const {contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  resizeWindow: (width, height) => ipcRenderer.send('resize-window', { width, height }),
  loadPlusView: () => ipcRenderer.send('loadPlusView'),

  sendRegister: (data) => ipcRenderer.send('register', data),
  onRegisterSuccess: (callback) => ipcRenderer.on('register-success', callback),
  onRegisterFailure: (callback) => ipcRenderer.on('register-failure', callback),

  sendLogin: (data) => ipcRenderer.send('login', data),
  onLoginSuccess: (callback) => ipcRenderer.on('login-success', callback),
  onLoginFailure: (callback) => ipcRenderer.on('login-failure', callback),

  addPassword: (data) => ipcRenderer.send('addPassword', data),
  onAddPasswordSuccess: (callback) => ipcRenderer.on('add-password-success', callback),
  onAddPasswordFailure: (callback) => ipcRenderer.on('add-password-failure', callback),
  
  generateRandomPassword: (data) => ipcRenderer.send('generateRandomPassword', data),
  onGenerateRandomPasswordSuccess: (callback) => ipcRenderer.on('generate-random-password-success', callback),
  onGenerateRandomPasswordFailure: (callback) => ipcRenderer.on('generate-random-password-failure', callback)
})

