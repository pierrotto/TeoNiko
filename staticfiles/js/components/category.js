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

    document.addEventListener('click', async (e) => {
        const link = e.target.closest('.js-qv');
        if (!link) return;
        e.preventDefault();

        openModal();

        try {
            const res = await fetch(link.dataset.qvUrl, {headers: {'X-Requested-With': 'XMLHttpRequest'}});
            const html = await res.text();
            body.innerHTML = html;
            if (window.initRatings) window.initRatings(body);

            wireThumbs();
            wireQVMagnify();
            dialog.focus();
        } catch (err) {
            body.innerHTML = '<div style="padding:24px;color:#b00">Failed to load.</div>';
        }
    });

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

    document.addEventListener('change', (e) => {
        const sel = e.target.closest('select[name="order"]');
        if (!sel) return;
        const url = new URL(window.location.href);
        url.searchParams.set('order', sel.value);
        url.searchParams.delete('page');
        window.location.assign(url.toString());
    });

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

(function () {
    const SEL_CARD = '.product-grid--list .product-card';

    const px = n => (isNaN(n) ? 0 : parseFloat(n));

    function fitOneCard(card) {
        const extra = card.querySelector('.product-extra');
        if (!extra) return;

        const csExtra = getComputedStyle(extra);
        const cardH = card.getBoundingClientRect().height;
        const padTB = px(csExtra.paddingTop) + px(csExtra.paddingBottom);
        const available = Math.max(0, cardH - padTB);   // no overflow

        extra.style.maxHeight = available + 'px';

        let remaining = available;

        const desc = extra.querySelector('.snip-text');
        if (desc) {
            const lh = px(getComputedStyle(desc).lineHeight) || 20;
            const maxLines = Math.max(0, Math.floor(remaining / lh));
            desc.style.setProperty('--desc-lines', String(maxLines));
            desc.style.webkitLineClamp = String(maxLines);

            remaining = Math.max(0, remaining - Math.min(maxLines * lh, desc.scrollHeight) - 8);
        }

        const specs = extra.querySelector('.snip-specs');
        if (specs) {
            const items = Array.from(specs.children);
            items.forEach(li => li.style.display = ''); // reset

            const probeH = items[0] ? items[0].getBoundingClientRect().height : 18;
            const canShow = Math.max(0, Math.floor(remaining / probeH));
            items.forEach((li, i) => {
                li.style.display = i < canShow ? '' : 'none';
            });
        }
    }

    function fitAll() {
        document.querySelectorAll(SEL_CARD).forEach(fitOneCard);
    }

    document.addEventListener('DOMContentLoaded', fitAll);
    window.addEventListener('load', fitAll);

    let t;
    window.addEventListener('resize', () => {
        clearTimeout(t);
        t = setTimeout(fitAll, 120);
    });
})();


