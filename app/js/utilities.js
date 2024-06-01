const setupWindowControls = () => {
  const { ipcRenderer } = require("electron");

  document.getElementById("close-button").addEventListener("click", () => {
    ipcRenderer.send("close-window");
  });

  document.getElementById("minimize-button").addEventListener("click", () => {
    ipcRenderer.send("minimize-window");
  });
}

module.exports = {
  setupWindowControls
};