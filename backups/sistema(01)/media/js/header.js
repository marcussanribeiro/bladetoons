document.addEventListener('DOMContentLoaded', function () {

  // =========================
  // USER MENU (dropdown perfil)
  // =========================
  const userBtn = document.getElementById('userMenuBtn');
  const userMenu = document.getElementById('userDropdown');

  if (userBtn && userMenu) {

    userBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      userMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', function (e) {
      if (!userBtn.contains(e.target) && !userMenu.contains(e.target)) {
        userMenu.classList.add('hidden');
      }
    });

  }

  // =========================
  // SEARCH TOGGLE
  // =========================
  const searchBtn = document.getElementById('searchBtn');
  const searchBox = document.getElementById('searchBox');
  const searchInput = document.getElementById('searchInput');
  const mainMenu = document.getElementById('mainMenu');

  let searchOpen = false;

  if (searchBtn && searchBox && mainMenu) {

    searchBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      searchOpen = !searchOpen;

      if (searchOpen) {
        searchBox.classList.remove('w-0');
        searchBox.classList.add('w-[300px]');

        if (mainMenu) {
          mainMenu.style.opacity = '0';
          mainMenu.style.pointerEvents = 'none';
        }

        if (searchInput) searchInput.focus();

      } else {
        searchBox.classList.add('w-0');
        searchBox.classList.remove('w-[300px]');

        if (mainMenu) {
          mainMenu.style.opacity = '1';
          mainMenu.style.pointerEvents = 'auto';
        }
      }
    });

    document.addEventListener('click', function (e) {
      if (
        searchOpen &&
        !searchBox.contains(e.target) &&
        e.target !== searchBtn
      ) {
        searchBox.classList.add('w-0');
        searchBox.classList.remove('w-[300px]');

        if (mainMenu) {
          mainMenu.style.opacity = '1';
          mainMenu.style.pointerEvents = 'auto';
        }

        searchOpen = false;
      }
    });

  }

  // =========================
  // LOGIN AJAX
  // =========================
  const loginForm = document.getElementById('loginForm');
  const loginError = document.getElementById('loginError');

  if (loginForm) {

    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const formData = new FormData(loginForm);

      fetch("/api/login/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]')?.value || ""
        }
      })
      .then(response => response.json())
      .then(data => {

        if (data.success) {
          window.location.href = "/dashboard/";
        } else {
          if (loginError) {
            loginError.innerText = data.error || "Erro ao logar";
            loginError.classList.remove("hidden");
          }
        }

      })
      .catch(() => {
        if (loginError) {
          loginError.innerText = "Erro no servidor";
          loginError.classList.remove("hidden");
        }
      });

    });

  }

});