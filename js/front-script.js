document.addEventListener('DOMContentLoaded', () => {
    // --- TYPEWRITER FUNCTION (still used for hero text, logo) ---
    function typeWriter(element, text, speed = 100, callback) {
        let i = 0;
        element.innerHTML = '';
        let cursor = element.querySelector('.typing-cursor');
        if (!cursor) {
            cursor = document.createElement('span');
            cursor.className = 'typing-cursor';
            element.appendChild(cursor);
        }
        function type() {
            if (i < text.length) {
                cursor.insertAdjacentText('beforebegin', text.charAt(i));
                i++;
                setTimeout(type, speed);
            } else {
                if (cursor && cursor.parentNode) {
                    // cursor.parentNode.removeChild(cursor); 
                }
                if (callback) callback();
            }
        }
        type();
    }

    // --- LOGO TYPING ---
    const logoElement = document.querySelector('.logo[data-type-text]');
    if (logoElement) {
        const textToType = logoElement.dataset.typeText;
        const typeSpeed = parseInt(logoElement.dataset.typeSpeed) || 120;
        setTimeout(() => { typeWriter(logoElement, textToType, typeSpeed); }, 300);
    }

    // --- SMOOTH SCROLL ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || !href.startsWith('#') || href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- HAMBURGER MENU ---
    const hamburger = document.querySelector('.hamburger-menu');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('is-active');
            navLinks.classList.toggle('is-active');
            const isActive = hamburger.classList.contains('is-active');
            hamburger.setAttribute('aria-expanded', isActive);
            if (isActive) {
                navLinks.setAttribute('aria-hidden', 'false');
            } else {
                navLinks.setAttribute('aria-hidden', 'true');
            }
        });
    }

    // --- REMOVED animateCoverLetters function ---

    // --- INTERSECTION OBSERVER FOR SCROLL ANIMATIONS ---
    const observerCallback = (entries, observerInstance) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const targetElement = entry.target; // This is the .animate-on-scroll element (e.g., .book-card)
                const cardAnimationDelay = parseInt(targetElement.dataset.animationDelay) || 0;

                // Delay for the card/section itself to animate in
                setTimeout(() => {
                    targetElement.classList.add('is-visible');

                    // Handle typing text for hero/logo (if it's a child of this animated block)
                    const typeableChildren = targetElement.querySelectorAll('[data-type-text][data-type-once]:not([data-typed="true"])');
                    typeableChildren.forEach((typeableChild, index) => {
                        typeableChild.dataset.typed = "true";
                        const text = typeableChild.dataset.typeText;
                        const speed = parseInt(typeableChild.dataset.typeSpeed) || 100;
                        const typeDelay = (parseInt(targetElement.dataset.typeDelay) || 150) + (index * (speed * text.length * 0.2));
                        setTimeout(() => {
                            typeWriter(typeableChild, text, speed);
                        }, typeDelay);
                    });

                    // Handle block slide-in + typing for cover text overlays
                    const coverTextsToAnimate = targetElement.querySelectorAll('.cover-text-overlay.animate-cover-text:not(.is-visible)');
                    coverTextsToAnimate.forEach(coverText => {
                        setTimeout(() => {
                            coverText.classList.add('is-visible');
                            const text = coverText.dataset.typeText;
                            if (text && !coverText.hasAttribute('data-typed')) {
                                coverText.setAttribute('data-typed', 'true');
                                const speed = parseInt(coverText.dataset.typeSpeed) || 60;
                                typeWriter(coverText, text, speed);
                            }
                        }, 600);
                    });

                }, cardAnimationDelay);

                observerInstance.unobserve(targetElement);
            }
        });
    };

    const observerOptions = { threshold: 0.05 };
    const observer = new IntersectionObserver(observerCallback, observerOptions);
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // Prevent flash of full cover titles before typing
    document.querySelectorAll('.cover-text-overlay[data-type-text]').forEach(el => {
        el.innerHTML = '';
    });

    // --- CARD CLICK TO TEPEDU, EXCLUDING SPECIFIC LINKS ---
    const firstBookCard = document.getElementById('first-book-card');

    if (firstBookCard) {
        firstBookCard.style.cursor = 'pointer'; // Indicate it's clickable
        firstBookCard.addEventListener('click', function (event) {
            // Check if the click target or its parent is the specific DR link
            if (event.target.closest('.dr-link')) {
                // If it is the DR link, let the default <a> tag behavior happen
                return; // Stop this function from doing anything further
            }

            // If the click was on the card itself but NOT on the .dr-link,
            // navigate to the main link for the card.
            // Make sure this click isn't bubbling from an unintended interactive element.
            if (event.target.closest('a') && !event.target.closest('.dr-link')) {
                // Click was on another link within the card that we don't want to override.
                // Or, if there are other specific non-DR links you want to allow, add checks for them.
                return;
            }

            window.open('https://s.tepedu.com/', '_blank'); // Open in new tab
        });
    }

});