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

    function slugify(value) {
        return value.toLowerCase()
            .replace(/æ/g, 'ae').replace(/ø/g, 'oe').replace(/å/g, 'aa')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '');
    }

    function linkTermsInChapters() {
        const page = (window.location.pathname || '').toLowerCase();
        if (!/kapitel[12]\.html$/.test(page) && !page.endsWith('/kapitel1.html') && !page.endsWith('/kapitel2.html')) {
            if (!page.includes('kapitel1') && !page.includes('kapitel2')) return;
        }
        const article = document.querySelector('article');
        if (!article) return;
        const entries = Object.entries(glossaryData)
            .map(([slug, data]) => ({ slug, term: data.term || findTermLabel(slug, data) }))
            .filter(entry => entry.term && entry.term.length >= 4)
            .sort((a, b) => b.term.length - a.term.length);
        if (!entries.length) return;

        const nodes = [];
        const walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT, {
            acceptNode(node) {
                const parent = node.parentElement;
                if (!parent) return NodeFilter.FILTER_REJECT;
                if (parent.closest('.legal-term, a, script, style, h1, .chapter-banner')) {
                    return NodeFilter.FILTER_REJECT;
                }
                if (!parent.closest('p, li, td')) return NodeFilter.FILTER_REJECT;
                if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
            }
        });
        while (walker.nextNode()) nodes.push(walker.currentNode);

        nodes.forEach(node => {
            let text = node.nodeValue;
            const hits = [];
            entries.forEach(entry => {
                const re = new RegExp('(?<![A-Za-zÆØÅæøå])' + escapeRegExp(entry.term) + '(?![A-Za-zÆØÅæøå])', 'i');
                const match = re.exec(text);
                if (match) hits.push({ index: match.index, length: match[0].length, slug: entry.slug, label: match[0] });
            });
            if (!hits.length) return;
            hits.sort((a, b) => a.index - b.index || b.length - a.length);
            const chosen = [];
            hits.forEach(hit => {
                const overlaps = chosen.some(prev => hit.index < prev.index + prev.length && hit.index + hit.length > prev.index);
                if (!overlaps) chosen.push(hit);
            });
            const fragment = document.createDocumentFragment();
            let cursor = 0;
            chosen.forEach(hit => {
                if (hit.index > cursor) fragment.appendChild(document.createTextNode(text.slice(cursor, hit.index)));
                const span = document.createElement('span');
                span.className = 'legal-term';
                span.setAttribute('data-slug', hit.slug);
                span.textContent = hit.label;
                fragment.appendChild(span);
                cursor = hit.index + hit.length;
            });
            if (cursor < text.length) fragment.appendChild(document.createTextNode(text.slice(cursor)));
            node.parentNode.replaceChild(fragment, node);
        });
    }

    function findTermLabel(slug, data) {
        const row = document.querySelector('[id="term-' + slug + '"]');
        if (row) return row.textContent.replace(/\s+/g, ' ').trim();
        return (data && data.term) || '';
    }

    function escapeRegExp(value) {
        return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // First, fetch all definitions from kapitel23.html if we are not on that page
    // Or just fetch them once to have a central registry
    const glossaryUrl = 'kapitel3.html';
    
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
                doc.querySelectorAll('table.glossary-table tbody tr').forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length < 2) return;
                    const term = cells[0].textContent.replace(/\s+/g, ' ').trim();
                    if (!term) return;
                    const slug = slugify(term);
                    glossaryData[slug] = {
                        term: term,
                        definition: cells[1].textContent.replace(/\s+/g, ' ').trim(),
                        example: cells[2] ? cells[2].textContent.replace(/\s+/g, ' ').trim() : ''
                    };
                });

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
                
                linkTermsInChapters();
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
                    <div class="footer" style="cursor: pointer;" onclick="window.location.href='kapitel3.html#term-${slug}'">
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

        termElement.addEventListener('click', (event) => {
            event.preventDefault();
            termElement.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
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
