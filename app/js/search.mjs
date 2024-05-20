const API = window['electronAPI'];
const aboutPage = document.getElementById('aboutPage');
const plusPage = document.getElementById('plusPage');

// Handle tab clicks to load respective views.
aboutPage.addEventListener('click', () => {
  API.loadAboutView();
});

plusPage.addEventListener('click', () => {
  API.loadPlusView();
});