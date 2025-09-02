document.addEventListener('DOMContentLoaded', () => {
    // ===== Quick View (unchanged logic, but NOT inside the forEach) =====
    const modal = document.getElementById('qv-modal');
    const body = document.getElementById('qv-body');
    const dialog = modal.querySelector('.qv-dialog');

    function openModal(html) {
        body.innerHTML = html || '<div style="padding:24px">Loading…</div>';
        modal.classList.add('is-open');
        document.body.classList.add('qv-lock');
        dialog.focus();
    }

    function closeModal() {
        modal.classList.remove('is-open');
        document.body.classList.remove('qv-lock');
        body.innerHTML = '';
    }

    // Open QV
    document.addEventListener('click', async (e) => {
        const link = e.target.closest('.js-qv');
        if (!link) return;
        e.preventDefault();

        openModal();

        try {
            const res = await fetch(link.dataset.qvUrl, {headers: {'X-Requested-With': 'XMLHttpRequest'}});
            const html = await res.text();
            body.innerHTML = html;

            wireThumbs();
            wireQVMagnify();
            dialog.focus();
        } catch (err) {
            body.innerHTML = '<div style="padding:24px;color:#b00">Failed to load.</div>';
        }
    });

    // Close QV
    modal.addEventListener('click', (e) => {
        if (e.target.matches('[data-qv-close], .qv-overlay')) closeModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });

    function wireThumbs() {
        const main = modal.querySelector('#qv-main');
        const thumbs = modal.querySelectorAll('.qv-thumb');
        if (!main || !thumbs.length) return;

        function activate(t) {
            main.src = t.dataset.src || t.src;
            thumbs.forEach(x => x.classList.remove('is-active'));
            t.classList.add('is-active');
        }

        thumbs.forEach(t => {
            t.addEventListener('click', () => activate(t));
            t.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    activate(t);
                }
            });
            t.setAttribute('role', 'button');
            t.setAttribute('tabindex', '0');
        });
    }

    function wireQVMagnify() {
        const main = modal.querySelector('#qv-main');
        if (!main) return;
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

    // ===== Cursor-follow zoom on category cards =====
    document.querySelectorAll('.content .product-thumb').forEach(thumb => {
        const img = thumb.querySelector('img');
        if (!img) return;

        function setOrigin(e) {
            const r = thumb.getBoundingClientRect();
            const x = ((e.clientX - r.left) / r.width) * 100;
            const y = ((e.clientY - r.top) / r.height) * 100;
            img.style.transformOrigin = `${x}% ${y}%`;
        }

        thumb.addEventListener('mousemove', setOrigin);
        thumb.addEventListener('mouseenter', setOrigin);
        thumb.addEventListener('mouseleave', () => {
            img.style.transformOrigin = '50% 50%';
        });
    });
});

