const API = window['electronAPI'];

// Handle tab clicks to load respective views.
document.getElementById('aboutPage').addEventListener('click', () => {
  API.loadAboutView();
});

document.getElementById('plusPage').addEventListener('click', () => {
  API.loadPlusView();
});