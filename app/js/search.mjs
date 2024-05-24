const API = window['electronAPI'];

const fetchUserId = async () => {
  try {
    const response = await API.fetchUserId();
    return response.user_id;
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
      console.log('user_id on load', user_id)
      if (user_id) {
        let response = await API.fetchPasswords(user_id);

        if (typeof response.data === 'string') {
          response = JSON.parse(response.data);
        }

        if (response) {
          populateSiteList(response);
        } else {
          console.error('Failed to fetch passwords:', response.message);
        }
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
