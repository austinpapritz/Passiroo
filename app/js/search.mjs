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


// Populating site name search / dropdown list.
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

// Edit password
document.addEventListener("DOMContentLoaded", () => {
  const pencilSvg = document.getElementById("pencilSvg");
  const checkmarkSvg = document.querySelector(".pencil-svg.hidden");
  const trashSvg = document.getElementById("trashSvg");
  const xmarkSvg = document.querySelector(".trash-svg.hidden");
  const accountNameInput = document.querySelector(".middle input[placeholder='account name']");
  const passwordInput = document.querySelector(".middle input[placeholder='password']");
  const confirmPasswordInput = document.querySelector(".middle input[placeholder='confirm password']");
  const passwordLabel = document.getElementById("passwordLabel");

  pencilSvg.addEventListener("click", () => {
      // Toggle hidden class on input fields and labels
      toggleHidden([accountNameInput, passwordInput, confirmPasswordInput, passwordLabel]);
      // Toggle visibility of SVGs
      toggleHidden([pencilSvg, checkmarkSvg, trashSvg, xmarkSvg]);
  });

  checkmarkSvg.addEventListener("click", () => {
      // Handle the logic for confirming the edit
      confirmEdit();
      // Toggle back the hidden class on input fields and labels
      toggleHidden([accountNameInput, passwordInput, confirmPasswordInput, passwordLabel]);
      // Toggle back visibility of SVGs
      toggleHidden([pencilSvg, checkmarkSvg, trashSvg, xmarkSvg]);
  });

  xmarkSvg.addEventListener("click", () => {
      // Handle the logic for cancelling the edit
      cancelEdit();
      // Toggle back the hidden class on input fields and labels
      toggleHidden([accountNameInput, passwordInput, confirmPasswordInput, passwordLabel]);
      // Toggle back visibility of SVGs
      toggleHidden([pencilSvg, checkmarkSvg, trashSvg, xmarkSvg]);
  });

  function toggleHidden(elements) {
      elements.forEach(element => {
          element.classList.toggle("hidden");
      });
  }

  function confirmEdit() {
      // Logic to save the edited values
      // This can include sending the updated values to the backend
      console.log("Edit confirmed");
  }

  function cancelEdit() {
      // Logic to revert any changes made during the edit
      console.log("Edit cancelled");
  }
});