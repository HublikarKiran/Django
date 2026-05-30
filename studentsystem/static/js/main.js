var menuButton = document.querySelector('[data-menu-button]');
var menu = document.querySelector('[data-menu]');

if (menuButton && menu) {
    menuButton.addEventListener('click', function () {
        menu.classList.toggle('open');
    });
}
