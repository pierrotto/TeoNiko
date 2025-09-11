(function () {
    if (window.__LIKES_BOUND__) return;
    window.__LIKES_BOUND__ = true;

    function getCsrfToken() {
        const m = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
        if (m) return m.pop();
        const el = document.querySelector('input[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }

    async function toggleLike(btn) {
        const url = btn.dataset.url;
        const csrftoken = getCsrfToken();

        try {
            const res = await fetch(url, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest'},
                redirect: 'follow',
            });

            if (res.redirected) {
                window.location.href = res.url;
                return;
            }
            if (!res.ok) {
                console.warn('[likes] HTTP', res.status);
                return;
            }

            // ⬇️ Parse JSON once and derive liked
            const data = await res.json();
            const liked = !!data.liked;

            btn.classList.toggle('liked', liked);
            btn.setAttribute('aria-pressed', String(liked));
            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fas', liked);
                icon.classList.toggle('far', !liked);
            }

            const wrap = document.querySelector('.icon-circle.right');
            if (wrap) {
                let badge = wrap.querySelector('.js-wish-count');
                const n = Math.max(0, parseInt(data.count, 10) || 0);
                wrap.dataset.count = String(n);

                if (!badge && n > 0) {
                    badge = document.createElement('span');
                    badge.className = 'badge js-wish-count';
                    badge.textContent = String(n);
                    wrap.appendChild(badge);
                } else if (badge) {
                    if (n > 0) {
                        badge.textContent = String(n);
                    } else {
                        badge.remove();
                    }
                }
            }

            if (!liked && btn.dataset.removeRow === '1') {
                const row = btn.closest('.wl-row');
                if (row) row.remove();
            }
        } catch (err) {
            console.error('[likes] error', err);
        }
    }

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.like-btn');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();
        toggleLike(btn);
    }, true);
})();
