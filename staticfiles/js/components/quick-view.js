(function () {
    function ready(fn) {
        if (document.readyState !== 'loading') fn();
        else document.addEventListener('DOMContentLoaded', fn);
    }

    ready(function () {
        const modal = document.getElementById('qv-modal');
        if (!modal) return;                     // guard
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
                body.innerHTML = await res.text();
                dialog.focus();
            } catch {
                body.innerHTML = '<div style="padding:24px;color:#b00">Failed to load.</div>';
            }
        });

        modal.addEventListener('click', (e) => {
            if (e.target.matches('[data-qv-close], .qv-overlay')) closeModal();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
        });
    });
})();
