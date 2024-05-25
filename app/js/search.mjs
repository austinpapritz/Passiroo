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
      if (user_id) {
        let response = await API.fetchPasswords(user_id);

        if (typeof response.data === 'string') {
          response = JSON.parse(response.data);
        }

        if (response) {
          populateSiteList(response);
          window.passwordObjs = response;
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
  const passwordLabel = document.getElementById('passwordLabel');
  const accountNameDropdown = document.getElementById('accountNameDropdown');
  siteUL.innerHTML = '';

  for (const site in passwordObjs) {
    const li = document.createElement('li');
    li.textContent = site;
    li.classList.add('site-li');
    li.addEventListener('click', () => {
      const allSites = document.querySelectorAll('.site-li');
      allSites.forEach(site => site.classList.remove('selected'));
      li.classList.add('selected');
      accountNameDropdown.innerHTML = '';
      passwordLabel.innerHTML = ''; 
      populateAccountDropdown(passwordObjs[site]);
    });
    siteUL.appendChild(li);
  }
}

function populateAccountDropdown(accounts) {
  const accountNameDropdown = document.getElementById('accountNameDropdown');

  accounts.forEach(account => {
    const option = document.createElement('option');
    option.value = account.password;
    option.textContent = account.account_name;
    option.addEventListener('click', () => {
      populatePasswordLabel(account.password);
    });
    accountNameDropdown.appendChild(option);
  });

  if (accounts.length > 0) {
    accountNameDropdown.selectedIndex = 0;
    populatePasswordLabel(accounts[0].password);
  }

  accountNameDropdown.addEventListener('change', (event) => {
    const selectedPassword = event.target.value;
    populatePasswordLabel(selectedPassword);
  });
}

function populatePasswordLabel(password) {
  const passwordLabel = document.getElementById('passwordLabel');
  passwordLabel.textContent = password;
}

function filterSearch() {
  const input = document.getElementById('siteSearch');
  const filter = input.value.toLowerCase();
  const ul = document.getElementById('site-ul');
  const li = ul.getElementsByTagName('li');

  for (let i = 0; i < li.length; i++) {
    const a = li[i].textContent || li[i].innerText;
    if (a.toLowerCase().indexOf(filter) > -1) {
      li[i].style.display = '';
    } else {
      li[i].style.display = 'none';
    }
  }
}