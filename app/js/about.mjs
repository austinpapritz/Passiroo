const API = window['electronAPI'];

// Handle tab clicks to load respective views.
document.getElementById('plusPage').addEventListener('click', () => {
  API.loadPlusView();
});

document.getElementById('searchPage').addEventListener('click', () => {
  API.loadSearchView();
});