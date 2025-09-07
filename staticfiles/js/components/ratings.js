(function () {
    function getCsrf() {
        const m = document.cookie.match(/(?:^|;)\s*csrftoken=([^;]+)/);
        return m ? decodeURIComponent(m[1]) : "";
    }

    function textForCount(container) {
        const avg = Number(container.dataset.avg || 0).toFixed(1);
        const count = Number(container.dataset.count || 0);
        const showCount = (container.dataset.showCount || "1") === "1"; // NEW: gate

        return showCount ? `(${avg}/5${count ? " · " + count : ""})` : `(${avg}/5)`;
    }

    function paint(container, value) {
        const v = Number(value) || 0;
        const upto = Math.round(v);

        container.querySelectorAll(".star").forEach((btn, i) => {
            const icon = btn.querySelector("i");
            const filled = i < upto;
            btn.classList.toggle("filled", filled);
            icon.classList.toggle("fas", filled);
            icon.classList.toggle("far", !filled);
        });

        const el = container.querySelector(".rating-count");
        if (el) el.textContent = textForCount(container);
    }

    async function handleClick(container, btn) {
        const url = container.dataset.rateUrl;
        if (!url) return;
        const value = Number(btn.dataset.value || "0");
        if (!value) return;

        container.dataset.my = String(value);
        paint(container, value);

        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCsrf(),
                },
                body: JSON.stringify({ rating: value }),
            });
            if (!res.ok) throw new Error("Bad response");
            const data = await res.json();
            if (!data.ok) throw new Error(data.error || "fail");

            container.dataset.avg = data.avg;
            container.dataset.count = data.count;

            paint(container, value);
        } catch (err) {
            // revert to previous state (my → or 0)
            console.warn("Rating failed:", err);
            const fallback = Number(container.dataset.my || 0);
            paint(container, fallback);
        }
    }

    function setup(container) {
        if (container.dataset.wired) return;
        container.dataset.wired = "1";

        const initial = Number(container.dataset.my || 0);
        paint(container, initial);

        const stars = container.querySelectorAll(".star");
        stars.forEach((btn, i) => {
            btn.addEventListener("mouseenter", () => paint(container, i + 1));
            btn.addEventListener("mouseleave", () => paint(container, Number(container.dataset.my || 0)));
        });

        container.addEventListener("click", (e) => {
            const btn = e.target.closest(".star");
            if (btn) handleClick(container, btn);
        });
    }

    window.initRatings = function (root) {
        (root || document).querySelectorAll(".rating-stars[data-rate-url]").forEach(setup);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => window.initRatings(document));
    } else {
        window.initRatings(document);
    }
})();
