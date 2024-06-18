const {contextBridge, ipcRenderer} = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  sendRegister: (data) => ipcRenderer.send("register", data),
  onRegisterSuccess: (callback) => ipcRenderer.on("register-success", callback),
  onRegisterFailure: (callback) => ipcRenderer.on("register-failure", callback),

  sendLogin: (data) => ipcRenderer.send("login", data),
  onLoginSuccess: (callback) => ipcRenderer.on("login-success", callback),
  onLoginFailure: (callback) => ipcRenderer.on("login-failure", callback),

  addSiteAccountAndPassword: (data) => ipcRenderer.send("add-site-account-and-password", data),
  onAddSiteAccountAndPasswordSuccess: (callback) => ipcRenderer.on("add-site-account-and-password-success", callback),
  onAddSiteAccountAndPasswordFailure: (callback) => ipcRenderer.on("add-site-account-and-password-failure", callback),

  editPassword: async (password_id, site_name, account_name, password) => await ipcRenderer.invoke("edit-password", { password_id, site_name, account_name, password }),

  deletePassword: async (password_id) => await ipcRenderer.invoke("delete-password", password_id),

  loadPlusView: () => ipcRenderer.send("loadPlusView"),
  loadSearchView: () => ipcRenderer.send("loadSearchView"),
  loadAboutView: () => ipcRenderer.send("loadAboutView"),
  
  generateRandomPassword: (data) => ipcRenderer.send("generateRandomPassword", data),
  onGenerateRandomPasswordSuccess: (callback) => ipcRenderer.on("generate-random-password-success", callback),
  onGenerateRandomPasswordFailure: (callback) => ipcRenderer.on("generate-random-password-failure", callback),

  fetchUserId: () => ipcRenderer.invoke("fetch-user-id"),
  fetchSavedSitesAccountsAndPasswords: (user_id) => ipcRenderer.invoke("fetch-saved-sites-accounts-and-passwords", user_id)
})

