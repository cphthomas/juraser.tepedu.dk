// Theme Toggle — default light (white), animated sun/moon
(function () {
    'use strict';

    const THEME_STORAGE_KEY = 'tepedu-theme';
    const THEME_LIGHT = 'light';
    const THEME_DARK = 'dark';

    function getCurrentTheme() {
        try {
            return localStorage.getItem(THEME_STORAGE_KEY) || THEME_LIGHT;
        } catch (e) {
            return THEME_LIGHT;
        }
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(THEME_STORAGE_KEY, theme);
        } catch (e) { /* ignore */ }
    }

    function updateThemeIcon(theme, animate) {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        const wrapper = themeToggle.querySelector('.theme-icon-wrapper');
        const sunIcon = themeToggle.querySelector('.theme-icon-sun');
        const moonIcon = themeToggle.querySelector('.theme-icon-moon');
        if (!sunIcon || !moonIcon) return;

        if (animate && wrapper) {
            wrapper.classList.remove('is-switching');
            // Force reflow so animation can restart
            void wrapper.offsetWidth;
            wrapper.classList.add('is-switching');
            themeToggle.classList.add('theme-pop');
            setTimeout(() => {
                wrapper.classList.remove('is-switching');
                themeToggle.classList.remove('theme-pop');
            }, 650);
        }

        if (theme === THEME_DARK) {
            sunIcon.classList.remove('active');
            moonIcon.classList.add('active');
            themeToggle.setAttribute('aria-label', 'Skift til lyst tema');
            themeToggle.setAttribute('title', 'Lyst tema');
        } else {
            sunIcon.classList.add('active');
            moonIcon.classList.remove('active');
            themeToggle.setAttribute('aria-label', 'Skift til mørkt tema');
            themeToggle.setAttribute('title', 'Mørkt tema');
        }
    }

    function toggleTheme() {
        const newTheme = getCurrentTheme() === THEME_LIGHT ? THEME_DARK : THEME_LIGHT;
        setTheme(newTheme);
        updateThemeIcon(newTheme, true);
    }

    function initTheme() {
        // Always resolve to light unless user previously chose dark
        const currentTheme = getCurrentTheme() === THEME_DARK ? THEME_DARK : THEME_LIGHT;
        setTheme(currentTheme);
        updateThemeIcon(currentTheme, false);

        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle && !themeToggle.dataset.themeBound) {
            themeToggle.dataset.themeBound = '1';
            themeToggle.addEventListener('click', function (e) {
                e.preventDefault();
                toggleTheme();
            });
        }
    }

    // Apply ASAP to avoid flash — default white/light
    try {
        const t = localStorage.getItem(THEME_STORAGE_KEY);
        document.documentElement.setAttribute('data-theme', t === THEME_DARK ? THEME_DARK : THEME_LIGHT);
    } catch (e) {
        document.documentElement.setAttribute('data-theme', THEME_LIGHT);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    window.toggleTheme = toggleTheme;
    window.getCurrentTheme = getCurrentTheme;
})();
