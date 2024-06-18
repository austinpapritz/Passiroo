import { spawn } from "child_process";
import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 660,
    transparent: true,
    titleBarStyle: "hidden",
    frame: false, 
    webPreferences: {
      preload: path.join(__dirname, "js/preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
    }
  });
  mainWindow.loadFile("app/views/login-register.html");
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.on("loadPlusView", () => {
  if (mainWindow) {
    mainWindow.loadFile("app/views/plus.html");
  } else {
    console.error("Main window is not available.");
  }
});

ipcMain.on("loadSearchView", () => {
  if (mainWindow) {
    mainWindow.loadFile("app/views/search.html");
  } else {
    console.error("Main window is not available.");
  }
});

ipcMain.on("loadAboutView", () => {
  if (mainWindow) {
    mainWindow.loadFile("app/views/about.html");
  } else {
    console.error("Main window is not available.");
  }
});

ipcMain.on("loadPlusView", () => {
  if (mainWindow) {
    mainWindow.loadFile("app/views/plus.html");
  } else {
    console.error("Main window is not available.");
  }
});

ipcMain.on("register", (event, userData) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "register_and_login_user", userData.email, userData.password]);

  pyProcess.stdout.on("data", (data) => {
    const response = JSON.parse(data.toString());
    if (response.status === "success") {
      event.reply("register-success", "User registered successfully");
    } else {
      event.reply("register-failure", response.message);
    }
  });

  pyProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
  });
});

ipcMain.on("login", (event, userData) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "login_user", userData.email, userData.password]);

  pyProcess.stdout.on("data", (data) => {
    try {
      const response = JSON.parse(data.toString());
      if (response.status === "success") {
        event.reply("login-success", response.message);
      } else {
        event.reply("login-failure", response.message);
      }
    } catch (e) {
      console.error(`Error parsing JSON: ${e.message}`);
      event.reply("login-failure", "Invalid response from server");
    }
  });

  pyProcess.stderr.on("data", (data) => {
    console.error(`Login stderr: ${data}`);
  });

  pyProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
  });
});

ipcMain.on("add-site-account-and-password", (event, userData) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "add_site_account_and_password", userData.user_id, userData.site_name, userData.account_name, userData.password]);

  let data = "";
  let error = "";

  pyProcess.stdout.on("data", (chunk) => {
    data += chunk;
  });

  pyProcess.stderr.on("data", (chunk) => {
    error += chunk;
  });

  pyProcess.on("close", (code) => {
    if (code === 0) {
      event.reply("add-site-account-and-password-success", "Password added successfully");
    } else {
      event.reply("add-site-account-and-password-failure", "Failed to add password");
    }
  });
});

ipcMain.on("generateRandomPassword", (event, data) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "generate_random_password", data.specialCharacters, data.passwordLength]);

  pyProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.stdout.on("data", (data) => {
    const result = JSON.parse(data.toString());
    if (result.status === "success") {
      event.reply("generate-random-password-success", { password: result.password });
    } else {
      event.reply("generate-random-password-failure", result.message);
    }
  });
});

ipcMain.handle("fetch-user-id", async (event) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "fetch_user_id"]);

  let data = "";
  let error = "";

  pyProcess.stdout.on("data", (chunk) => {
    data += chunk;
  });

  pyProcess.stderr.on("data", (chunk) => {
    error += chunk;
  });

  const exitCode = await new Promise((resolve) => {
    pyProcess.on("close", resolve);
  });

  if (exitCode) {
    console.error(`subprocess error exit ${exitCode}, ${error}`);
    throw new Error(`subprocess error exit ${exitCode}, ${error}`);
  }

  try {
    const result = JSON.parse(data);
    return result;
  } catch (e) {
    console.error(`JSON parse error: ${data}`);
    throw new Error(`JSON parse error: ${data}`);
  }
});

ipcMain.handle("fetch-saved-sites-accounts-and-passwords", async (event, user_id) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "fetch_sites_accounts_and_passwords", user_id]);

  let data = "";
  let error = "";

  pyProcess.stdout.on("data", (chunk) => {
      data += chunk;
  });

  pyProcess.stderr.on("data", (chunk) => {
      error += chunk;
  });

  const exitCode = await new Promise((resolve) => {
      pyProcess.on("close", resolve);
  });

  if (exitCode) {
      console.error(`subprocess error exit ${exitCode}, ${error}`);
      throw new Error(`subprocess error exit ${exitCode}, ${error}`);
  }

  try {
      const result = JSON.parse(data);
      return result;
  } catch (e) {
      console.error(`JSON parse error: ${data}`);
      throw new Error(`JSON parse error: ${data}`);
  }
});

ipcMain.on("logout", (event) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "logout_user"]);

  pyProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.on("close", (code) => {
    if (code === 0) {
      event.reply("logout-success");
    } else {
      event.reply("logout-failure");
    }
  });
});

app.on("before-quit", () => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  spawn("python", [pythonScriptPath, "logout_user"]);
});

ipcMain.handle("edit-password", async (event, { password_id, site_name, account_name, password }) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "edit_password", password_id, site_name, account_name, password]);

  let data = "";
  let error = "";

  pyProcess.stdout.on("data", (chunk) => {
    data += chunk;
  });

  pyProcess.stderr.on("data", (chunk) => {
    error += chunk;
  });

  const exitCode = await new Promise((resolve) => {
    pyProcess.on("close", resolve);
  });

  if (exitCode) {
    console.error(`subprocess error exit ${exitCode}, ${error}`);
    return { status: "error", message: `subprocess error exit ${exitCode}, ${error}` };
  }

  try {
    const result = JSON.parse(data);
    return result;
  } catch (e) {
    console.error(`JSON parse error: ${data}`);
    return { status: "error", message: `JSON parse error: ${data}` };
  }
});

ipcMain.handle("delete-password", async (event, password_id) => {
  const pythonScriptPath = path.join(__dirname, "backend/main.py");
  const pyProcess = spawn("python", [pythonScriptPath, "delete_password", password_id]);

  let data = "";
  let error = "";

  pyProcess.stdout.on("data", (chunk) => {
    data += chunk;
  });

  pyProcess.stderr.on("data", (chunk) => {
    error += chunk;
  });

  const exitCode = await new Promise((resolve) => {
    pyProcess.on("close", resolve);
  });

  if (exitCode) {
    console.error(`subprocess error exit ${exitCode}, ${error}`);
    return { status: "error", message: `subprocess error exit ${exitCode}, ${error}` };
  }

  try {
    const result = JSON.parse(data);
    return result;
  } catch (e) {
    console.error(`JSON parse error: ${data}`);
    return { status: "error", message: `JSON parse error: ${data}` };
  }
});
