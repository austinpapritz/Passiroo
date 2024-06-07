const API = window["electronAPI"];

const fetchUserId = async () => {
  try {
    const response = await API.fetchUserId();
    return response.user_id;
  } catch (error) {
    console.error("Failed to fetch user_id:", error);
    throw error;
  }
};

const aboutPage = document.getElementById("aboutPage");
const plusPage = document.getElementById("plusPage");
const searchPage = document.getElementById("searchPage");

// Handle tab clicks to load respective views.
aboutPage.addEventListener("click", () => {
  API.loadAboutView();
});

plusPage.addEventListener("click", () => {
  API.loadPlusView();
});

searchPage.addEventListener("click", () => {
  API.loadSearchView();
});

// Fetches password object from backend. Example of passwordObj below:
// {
//   "site_name": [
//     {
//       "account_name": "a@b.com",
//       "password": "p4ssw0rd",
//       "password_id": 1
//     },
//     {
//       "account_name": "b@c.com",
//       "password": "hunter_2",
//       "password_id": 2
//     },
//   ]
// }
async function fetchPasswordData() {
  if (API) {
    try {
      const user_id = await fetchUserId();
      if (user_id) {
        let response = await API.fetchPasswords(user_id);

        if (typeof response.data === "string") {
          response = JSON.parse(response.data);
        }

        if (response) {
          populateSiteList(response);
          window.passwordObjs = response;
        } else {
          console.error("Failed to fetch passwords:", response.message);
        }
      }
    } catch (error) {
      console.error("Failed to fetch passwords:", error);
    }
  } else {
    console.error("electronAPI is not available");
  }
}
// Populating site name search / dropdown list.
document.addEventListener("DOMContentLoaded", async () => {
  await fetchPasswordData();
});

function populateSiteList(passwordObjs) {
  const siteUL = document.getElementById("site-ul");
  const passwordLabel = document.getElementById("passwordLabel");
  const accountNameDropdown = document.getElementById("accountNameDropdown");
  siteUL.innerHTML = "";

  for (const site in passwordObjs) {
    const li = document.createElement("li");
    li.textContent = site;
    li.classList.add("site-li");
    li.addEventListener("click", () => {
      const allSites = document.querySelectorAll(".site-li");
      allSites.forEach(site => site.classList.remove("selected"));
      li.classList.add("selected");
      accountNameDropdown.innerHTML = "";
      passwordLabel.innerHTML = ""; 
      populateAccountDropdown(passwordObjs[site]);
    });
    siteUL.appendChild(li);
  }
}

function populateAccountDropdown(accounts) {
  const accountNameDropdown = document.getElementById("accountNameDropdown");

  accounts.forEach(account => {
    const option = document.createElement("option");
    option.value = account.password;
    option.textContent = account.account_name;
    option.addEventListener("click", () => {
      populatePasswordLabel(account.password);
    });
    accountNameDropdown.appendChild(option);
  });

  if (accounts.length > 0) {
    accountNameDropdown.selectedIndex = 0;
    populatePasswordLabel(accounts[0].password);
  }

  accountNameDropdown.addEventListener("change", (event) => {
    const selectedPassword = event.target.value;
    populatePasswordLabel(selectedPassword);
  });
}

function populatePasswordLabel(password) {
  const passwordLabel = document.getElementById("passwordLabel");
  passwordLabel.textContent = password;
}

function filterSearch() {
  const input = document.getElementById("siteSearch");
  const filter = input.value.toLowerCase();
  const ul = document.getElementById("site-ul");
  const li = ul.getElementsByTagName("li");

  for (let i = 0; i < li.length; i++) {
    const a = li[i].textContent || li[i].innerText;
    if (a.toLowerCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

// Edit and delete password.
document.addEventListener("DOMContentLoaded", () => {
  const pencilSvg = document.getElementById("pencilSvg");
  const checkmarkSvg = document.querySelector(".pencil-svg.hidden");
  const trashSvg = document.getElementById("trashSvg");
  const xmarkSvg = document.querySelector(".trash-svg.hidden");
  const accountNameDropdown = document.getElementById("accountNameDropdown");
  const passwordLabel = document.getElementById("passwordLabel");
  const accountNameInput = document.querySelector(".middle input[placeholder='account name']");
  const passwordInput = document.querySelector(".middle input[placeholder='password']");
  const confirmPasswordInput = document.querySelector(".middle input[placeholder='confirm password']");

  let confirmingDelete = false;

  // Pencil and trashcan SVGs turn into checkmark and ex-mark SVGs for confirming/cancelling edit.
  pencilSvg.addEventListener("click", () => {
    // Toggle hidden class on input fields and labels.
    addHidden([pencilSvg, trashSvg]);
    // Toggle visibility of SVGs.
    removeHidden([checkmarkSvg, xmarkSvg, accountNameInput, passwordInput, confirmPasswordInput, passwordLabel]);
  });

  trashSvg.addEventListener("click", () => {

    confirmingDelete = true;
    addRedBorder([accountNameDropdown, passwordLabel]);
    addHidden([pencilSvg, trashSvg]);
    removeHidden([checkmarkSvg, xmarkSvg]);
});

  checkmarkSvg.addEventListener("click", async () => {
    if (confirmingDelete) {
      await deletePassword();
      confirmingDelete = false;
      removeRedBorder([accountNameDropdown, passwordLabel]);
    } else {
      await confirmEdit();
    }
    // Refetch passwords and reload page.
    await fetchPasswordData();
    // API.loadSearchView();
    // Toggle back the hidden class on input fields and labels.
    addHidden([accountNameInput, passwordInput, confirmPasswordInput, checkmarkSvg, xmarkSvg]);
    // Toggle back visibility of SVGs.
    removeHidden([pencilSvg, trashSvg, accountNameDropdown, passwordLabel ]);
  });

  xmarkSvg.addEventListener("click", () => {
    // Handle the logic for cancelling the edit.
    cancelEdit();
    // Toggle back the hidden class on input fields and labels.
    toggleHidden([accountNameInput, passwordInput, confirmPasswordInput, passwordLabel]);
    // Toggle back visibility of SVGs.
    toggleHidden([pencilSvg, checkmarkSvg, trashSvg, xmarkSvg]);
  });

  // If checkmark is clicked, then send new password data to backend for updating.
  async function confirmEdit() {
    try {
      const selectedSite = document.querySelector(".site-li.selected").textContent;
      const selectedAccount = accountNameDropdown.options[accountNameDropdown.selectedIndex].textContent;

      const newAccountName = accountNameInput.value;
      const newPassword = passwordInput.value;
      const confirmPassword = confirmPasswordInput.value;

      if (newPassword !== confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      const account = window.passwordObjs[selectedSite].find(account => account.account_name === selectedAccount);
      const password_id = account.password_id;

      const response = await API.editPassword(password_id, selectedSite, newAccountName, newPassword);

      if (response.status === "success") {
        console.log("Password updated successfully");
      } else {
        console.error("Failed to update password:", response.message);
      }
    } catch (error) {
      console.error("Failed to edit password:", error);
    }
  }

  async function deletePassword() {
    try {
        const selectedSite = document.querySelector(".site-li.selected").textContent;
        const selectedAccount = accountNameDropdown.options[accountNameDropdown.selectedIndex].textContent;
        const account = window.passwordObjs[selectedSite].find(account => account.account_name === selectedAccount);
        const password_id = account.password_id;

        const response = await API.deletePassword(password_id);

        if (response.status === "success") {
            console.log("Password deleted successfully");
        } else {
            console.error("Failed to delete password:", response.message);
        }
    } catch (error) {
        console.error("Failed to delete password:", error);
    }
}

  // If ex-mark is clicked, cancel the edit by reloading page.
  async function cancelEdit() {
    await fetchPasswordData();
    API.loadSearchView();
  }

  function addHidden(elements) {
    elements.forEach(element => {
        element.classList.add("hidden");
    });
  }

  function removeHidden(elements) {
    elements.forEach(element => {
        element.classList.remove("hidden");
    });
  }

  function addRedBorder(elements) {
    elements.forEach(element => {
        element.classList.add("red-border");
    });
  }

  function removeRedBorder(elements) {
      elements.forEach(element => {
          element.classList.remove("red-border");
      });
    }
});

