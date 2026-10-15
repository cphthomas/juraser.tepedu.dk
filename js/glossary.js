/**
 * Glossary Tooltip Functionality
 * Handles showing a discrete popup with definitions of legal terms.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'glossary-tooltip';
    document.body.appendChild(tooltip);

    let hideTimeout;

    const glossaryData = {};

    // First, fetch all definitions from kapitel23.html if we are not on that page
    // Or just fetch them once to have a central registry
    const glossaryUrl = window.location.pathname.includes('kapitel23.html') ? 'kapitel23.html' : 'kapitel23.html';
    
    // Check if we are running on file:// protocol (local development)
    const isLocalFile = window.location.protocol === 'file:';
    
    if (isLocalFile) {
        console.warn('Kører lokalt via file:// - Fetch af kapitel23.html kan være blokeret af CORS. Bruger data-attributter som fallback.');
        initTooltips();
    } else {
        fetch(glossaryUrl)
            .then(response => {
                if (!response.ok) throw new Error('Netværksfejl ved hentning af ordliste');
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const items = doc.querySelectorAll('.glossary-term-item');
                
                items.forEach(item => {
                    const titleEl = item.querySelector('.term-title');
                    const defEl = item.querySelector('.term-definition');
                    const exEl = item.querySelector('.term-example small');
                    
                    if (titleEl && titleEl.id) {
                        const slug = titleEl.id.replace('term-', '').toLowerCase();
                        const defText = defEl ? defEl.textContent.trim() : '';
                        const exText = exEl ? exEl.innerHTML.replace(/<strong>Eksempel:<\/strong>\s*/i, '').trim() : '';
                        
                        glossaryData[slug] = {
                            definition: defText,
                            example: exText
                        };
                    }
                });
                
                // Now that we have the data, initialize tooltips
                initTooltips();
            })
            .catch(err => {
                console.error('Kunne ikke hente ordliste-data:', err);
                initTooltips(); // Fallback to data attributes
            });
    }

    function initTooltips() {
        const terms = document.querySelectorAll('.legal-term');

        terms.forEach(termElement => {
            termElement.addEventListener('mouseenter', (e) => {
                clearTimeout(hideTimeout);

                const term = termElement.textContent.trim();
                const slug = termElement.getAttribute('data-slug') ? termElement.getAttribute('data-slug').toLowerCase() : null;
                
                // Priority: 1. Loaded glossaryData, 2. data-attributes
                let definition = termElement.getAttribute('data-definition');
                let example = termElement.getAttribute('data-example');
                
                if (slug && glossaryData[slug]) {
                    // Only override if glossaryData has content
                    if (glossaryData[slug].definition) {
                        definition = glossaryData[slug].definition;
                    }
                    if (glossaryData[slug].example) {
                        example = glossaryData[slug].example;
                    }
                }

                tooltip.innerHTML = `
                    <div class="header">
                        <i class="bi bi-info-circle-fill"></i>
                        <h4>${term}</h4>
                    </div>
                    <div class="definition">${definition || 'Ingen definition tilgængelig.'}</div>
                    ${example ? `<div class="example"><strong>Eksempel:</strong> ${example}</div>` : ''}
                    <div class="footer" style="cursor: pointer;" onclick="window.open('kapitel23.html#term-${slug}', '_blank')">
                        <span>LÆS MERE I ORDLISTEN</span>
                        <i class="bi bi-arrow-right"></i>
                    </div>
                `;

            // Allow transitions to calculate height
            tooltip.style.visibility = 'hidden';
            tooltip.classList.add('show');

            const rect = termElement.getBoundingClientRect();
            const tooltipHeight = tooltip.offsetHeight;
            const tooltipWidth = tooltip.offsetWidth;

            let top = rect.top - tooltipHeight - 15;
            let left = rect.left + (rect.width / 2) - (tooltipWidth / 2);

            // Adjust if out of bounds (top)
            if (top < 0) {
                top = rect.bottom + 15;
            }

            // Adjust if out of bounds (left)
            if (left < 10) left = 10;
            if (left + tooltipWidth > window.innerWidth - 10) {
                left = window.innerWidth - tooltipWidth - 10;
            }

            tooltip.style.top = `${top + window.scrollY}px`;
            tooltip.style.left = `${left + window.scrollX}px`;
            tooltip.style.visibility = 'visible';
        });

        termElement.addEventListener('mouseleave', () => {
            hideTimeout = setTimeout(() => {
                tooltip.classList.remove('show');
            }, 300);
        });
    });
    }

    // Keep tooltip open when hovering over it
    tooltip.addEventListener('mouseenter', () => {
        clearTimeout(hideTimeout);
    });

    tooltip.addEventListener('mouseleave', () => {
        tooltip.classList.remove('show');
    });
});
