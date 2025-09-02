(function () {
    const sel = document.getElementById('category-select');
    if (!sel) return;

    sel.addEventListener('change', function () {
        const base = this.value;
        if (!base) return;

        // Are we currently on a category page?
        const onCategoryPage = "{{ request.resolver_match.url_name }}" === "category-by-name";

        if (!onCategoryPage) {
            // Landing page: go straight to the category.
            // (Do NOT carry any min/max so the new page uses category extremes.)
            window.location.assign(base);
            return;
        }

        // Category page: preserve other filters but reset price + pagination.
        const form = document.getElementById('filters');
        const params = new URLSearchParams(form ? new FormData(form) : undefined);

        // Reset price to the new category’s natural bounds
        params.delete('min');
        params.delete('max');

        // Reset pagination when switching category
        params.delete('page');

        const qs = params.toString();
        window.location.assign(qs ? `${base}?${qs}` : base);
    });
})();