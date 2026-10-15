// Menu configuration for servicejura
const menuItems = [
    { href: 'index.html', text: '0. Forside' },
    { href: 'kapitel1.html', text: '1. Markedsføring og forbrugerret' },
    { href: 'kapitel2.html', text: '2. Købeloven' },
    { href: 'kapitel3.html', text: '3. Ordliste' }
];

// Initialize menu when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    const menuContainer = document.querySelector('.navbar .dropdown-menu');
    if (menuContainer) {
        menuContainer.innerHTML = menuItems.map(item =>
            `<a class="dropdown-item" href="${item.href}">${item.text}</a>`
        ).join('');
        menuContainer.querySelectorAll('.dropdown-item').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href && !href.startsWith('#') && href !== '#') {
                    e.preventDefault();
                    window.location.href = href;
                }
            });
        });
    }

    // Dynamic Navigation Arrows
    const pages = menuItems.map(item => item.href);

    // Get current filename (virker med file://, localhost og produktion)
    const pathname = (window.location.pathname || '/').toLowerCase();
    const filename = pathname.split('/').filter(Boolean).pop() || '';
    let currentPage = 'index.html';
    if (!filename || filename === 'index.html' || pathname.endsWith('/')) {
        currentPage = 'index.html';
    } else if (/kapitel\d+\.html/.test(filename)) {
        currentPage = filename;
    }

    const currentIndex = pages.findIndex(page => page.toLowerCase() === currentPage);

    const prevLink = document.getElementById('prev-page-link');
    const nextLink = document.getElementById('next-page-link');

    if (currentIndex !== -1) {
        const prevIndex = (currentIndex - 1 + pages.length) % pages.length;
        const nextIndex = (currentIndex + 1) % pages.length;

        const prevHref = pages[prevIndex];
        const nextHref = pages[nextIndex];

        if (prevLink) {
            prevLink.href = prevHref;
            prevLink.classList.remove('disabled');
        }
        if (nextLink) {
            nextLink.href = nextHref;
            nextLink.classList.remove('disabled');
        }
    } else {
        if (prevLink) prevLink.href = 'index.html';
        if (nextLink) nextLink.href = 'kapitel1.html';
    }
});
