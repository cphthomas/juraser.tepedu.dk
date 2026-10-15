document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.book-quiz').forEach(root => {
        const items = [...root.querySelectorAll('.question')].map(node => ({
            question: node.getAttribute('data-question') || '',
            answer: Number(node.getAttribute('data-answer')),
            explanation: node.getAttribute('data-explanation') || '',
            options: [...node.querySelectorAll('.option')].map(option => option.getAttribute('data-option') || option.textContent)
        }));
        if (!items.length) return;

        const stage = document.createElement('div');
        stage.className = 'quiz-stage';
        root.appendChild(stage);

        let index = 0;
        let score = 0;
        let locked = false;

        function render() {
            const item = items[index];
            stage.innerHTML = '';
            const progress = document.createElement('div');
            progress.className = 'quiz-progress';
            items.forEach((_, i) => {
                const mark = document.createElement('span');
                if (i <= index) mark.className = 'on';
                progress.appendChild(mark);
            });
            stage.appendChild(progress);

            const question = document.createElement('p');
            question.className = 'quiz-question';
            question.textContent = (index + 1) + '. ' + item.question;
            stage.appendChild(question);

            const options = document.createElement('div');
            options.className = 'quiz-options';
            item.options.forEach((label, optionIndex) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.textContent = label;
                button.addEventListener('click', () => choose(optionIndex, button, options, item));
                options.appendChild(button);
            });
            stage.appendChild(options);
        }

        function choose(optionIndex, button, options, item) {
            if (locked) return;
            locked = true;
            [...options.children].forEach((child, i) => {
                child.disabled = true;
                if (i === item.answer) child.classList.add('right');
            });
            if (optionIndex === item.answer) score += 1;
            else button.classList.add('wrong');

            const explain = document.createElement('div');
            explain.className = 'quiz-explain';
            explain.textContent = item.explanation;
            stage.appendChild(explain);

            const nav = document.createElement('div');
            nav.className = 'quiz-nav';
            const count = document.createElement('span');
            count.className = 'quiz-score';
            count.textContent = score + ' rigtige';
            const next = document.createElement('button');
            next.type = 'button';
            next.textContent = index === items.length - 1 ? 'Se resultat' : 'Næste';
            next.addEventListener('click', () => {
                if (index === items.length - 1) {
                    stage.innerHTML = '<p class="quiz-question">Du fik ' + score + ' ud af ' + items.length + '.</p>';
                    const again = document.createElement('button');
                    again.type = 'button';
                    again.textContent = 'Prøv igen';
                    again.addEventListener('click', () => {
                        index = 0;
                        score = 0;
                        locked = false;
                        render();
                    });
                    const navAgain = document.createElement('div');
                    navAgain.className = 'quiz-nav';
                    navAgain.appendChild(again);
                    stage.appendChild(navAgain);
                    return;
                }
                index += 1;
                locked = false;
                render();
            });
            nav.appendChild(count);
            nav.appendChild(next);
            stage.appendChild(nav);
        }

        render();
    });
});
