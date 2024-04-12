function toggleDarkMode() {
    const body = document.body;
    const darkModeIcon = document.getElementById('dark-mode-icon');

    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        darkModeIcon.classList.remove('fa-moon');
        darkModeIcon.classList.add('fa-sun');
    } else {
        darkModeIcon.classList.remove('fa-sun');
        darkModeIcon.classList.add('fa-moon');
    }
}


function navigateTo(url) {
    window.location.href = url;
}