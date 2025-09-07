(function () {
    const sel = document.getElementById('category-select');
    if (!sel) return;

    sel.addEventListener('change', function () {
        const base = this.value;
        if (!base) return;

        const onCategoryPage = "{{ request.resolver_match.url_name }}" === "category-by-name";

        if (!onCategoryPage) {
            window.location.assign(base);
            return;
        }

        const form = document.getElementById('filters');
        const params = new URLSearchParams(form ? new FormData(form) : undefined);

        params.delete('min');
        params.delete('max');

        params.delete('page');

        const qs = params.toString();
        window.location.assign(qs ? `${base}?${qs}` : base);
    });
})();

(function () {
    const form = document.getElementById('filters');
    if (!form) return;

    const lo = form.querySelector('#price_min');
    const hi = form.querySelector('#price_max');
    const loOut = document.getElementById('min_value');
    const hiOut = document.getElementById('max_value');
    if (!lo || !hi || !loOut || !hiOut) return;

    const GAP = 10;

    const decimals = Math.max(
        (String(lo.step || '').split('.')[1] || '').length,
        (String(hi.step || '').split('.')[1] || '').length
    );
    const fmt = v => Number(v).toFixed(decimals);

    const num = v => parseFloat(v);
    const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

    function updateOutputs(a, b) {
        loOut.textContent = fmt(a);
        hiOut.textContent = fmt(b);
    }

    function onLoChange() {
        let a = num(lo.value);
        const b = num(hi.value);

        a = clamp(a, num(lo.min || '-Infinity'), num(lo.max || 'Infinity'));
        if (a > b - GAP) a = b - GAP;

        lo.value = a;
        updateOutputs(a, b);
    }

    function onHiChange() {
        const a = num(lo.value);
        let b = num(hi.value);

        b = clamp(b, num(hi.min || '-Infinity'), num(hi.max || 'Infinity'));
        if (b < a + GAP) b = a + GAP;

        hi.value = b;
        updateOutputs(a, b);
    }

    ['input', 'change'].forEach(evt => {
        lo.addEventListener(evt, onLoChange);
        hi.addEventListener(evt, onHiChange);
    });

    onLoChange();
    onHiChange();
})();
