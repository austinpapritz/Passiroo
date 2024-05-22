const API = window['electronAPI'];

const fetchUserId = async () => {
  try {
    const user_id = await API.fetchUserId();
    return user_id;
  } catch (error) {
    console.error('Failed to fetch user_id:', error);
    throw error;
  }
};

const aboutPage = document.getElementById('aboutPage');
const plusPage = document.getElementById('plusPage');

// Handle tab clicks to load respective views.
aboutPage.addEventListener('click', () => {
  API.loadAboutView();
});

plusPage.addEventListener('click', () => {
  API.loadPlusView();
});

document.addEventListener('DOMContentLoaded', async () => {
  if (API) {
    try {
      const user_id = await fetchUserId();
      if (user_id) {
        const passwordObjs = await API.fetchPasswords({ user_id });
        populateSiteList(passwordObjs);
      }
    } catch (error) {
      console.error('Failed to fetch passwords:', error);
    }
  } else {
    console.error('electronAPI is not available');
  }
});

function populateSiteList(passwordObjs) {
  const siteUL = document.getElementById('site-ul');
  siteUL.innerHTML = ''; // Clear existing items
  for (const site in passwordObjs) {
    console.log('site', site);
    const li = document.createElement('li');
    li.textContent = site;
    li.classList.add('site-li');
    li.addEventListener('click', () => populateAccountDropdown(passwordObjs[site]));
    siteUL.appendChild(li);
  }
}

function populateAccountDropdown(accounts) {
  const accountNameDropdown = document.getElementById('accountNameDropdown');
  accountNameDropdown.innerHTML = '<option value="">choose account</option>';

  accounts.forEach(account => {
    const option = document.createElement('option');
    option.value = account.account_name;
    option.textContent = account.account_name;
    accountNameDropdown.appendChild(option);
  });
}
