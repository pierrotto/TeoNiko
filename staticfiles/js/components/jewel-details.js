(() => {
    const main = document.getElementById('main-photo');
    const thumbs = document.querySelectorAll('.thumbs .thumb');

    function activate(t) {
        if (!main) return;
        main.src = t.dataset.src || t.src;
        thumbs.forEach(x => x.classList.remove('is-active'));
        t.classList.add('is-active');
    }

    thumbs.forEach(t => {
        t.addEventListener('click', () => activate(t));
        t.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                activate(t);
            }
        });
    });

    if (main) {
        const scale = 1.60;

        function setOrigin(ev) {
            const r = main.getBoundingClientRect();
            const x = ((ev.clientX - r.left) / r.width) * 100;
            const y = ((ev.clientY - r.top) / r.height) * 100;
            main.style.transformOrigin = `${x}% ${y}%`;
        }

        function zoomIn() {
            main.style.transform = `scale(${scale})`;
        }

        function zoomOut() {
            main.style.transform = 'scale(1)';
        }

        main.addEventListener('mousemove', setOrigin);
        main.addEventListener('mouseenter', zoomIn);
        main.addEventListener('mouseleave', zoomOut);
        main.setAttribute('tabindex', '0');
        main.addEventListener('focus', zoomIn);
        main.addEventListener('blur', zoomOut);
    }

    const tabs = Array.from(document.querySelectorAll('.tabs .tab'));
    const panels = Array.from(document.querySelectorAll('.tabs .panel'));

    function activateTab(i) {
        tabs.forEach((t, idx) => {
            const on = idx === i;
            t.setAttribute('aria-selected', on ? 'true' : 'false');
            panels[idx].classList.toggle('is-active', on);
            panels[idx].hidden = !on;
        });
    }

    tabs.forEach((t, i) => {
        t.addEventListener('click', () => activateTab(i));
        t.addEventListener('keydown', e => {
            if (e.key === 'ArrowRight') activateTab((i + 1) % tabs.length);
            if (e.key === 'ArrowLeft') activateTab((i - 1 + tabs.length) % tabs.length);
        });
    });
})();