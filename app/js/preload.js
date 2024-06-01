// This file makes it so that only necessary Node.js functions are exposed
const {contextBridge, ipcRenderer} = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  sendRegister: (data) => ipcRenderer.send("register", data),
  onRegisterSuccess: (callback) => ipcRenderer.on("register-success", callback),
  onRegisterFailure: (callback) => ipcRenderer.on("register-failure", callback),

  sendLogin: (data) => ipcRenderer.send("login", data),
  onLoginSuccess: (callback) => ipcRenderer.on("login-success", callback),
  onLoginFailure: (callback) => ipcRenderer.on("login-failure", callback),

  addPassword: (data) => ipcRenderer.send("addPassword", data),
  onAddPasswordSuccess: (callback) => ipcRenderer.on("add-password-success", callback),
  onAddPasswordFailure: (callback) => ipcRenderer.on("add-password-failure", callback),

  editPassword: async (password_id, site_name, account_name, password) => await ipcRenderer.invoke("edit-password", { password_id, site_name, account_name, password }),

  loadPlusView: () => ipcRenderer.send("loadPlusView"),
  loadAboutView: () => ipcRenderer.send("loadAboutView"),
  loadSearchView: () => ipcRenderer.send("loadSearchView"),
  
  generateRandomPassword: (data) => ipcRenderer.send("generateRandomPassword", data),
  onGenerateRandomPasswordSuccess: (callback) => ipcRenderer.on("generate-random-password-success", callback),
  onGenerateRandomPasswordFailure: (callback) => ipcRenderer.on("generate-random-password-failure", callback),

  fetchUserId: () => ipcRenderer.invoke("fetch-user-id"),
  fetchPasswords: (user_id) => ipcRenderer.invoke("fetch-passwords", user_id)
})

