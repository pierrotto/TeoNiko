window.addEventListener('load', function () {
    const track = document.getElementById('carouselTrack');
    const allItems = Array.from(track.querySelectorAll('.carousel-item'));
    const clones = allItems.filter(item => item.classList.contains('clone'));
    const realItems = allItems.length - clones.length;

    const itemWidth = allItems[0].offsetWidth + 20; // includes margin/gap
    let position = clones.length / 2;
    let isAnimating = false;

    // Initial positioning
    track.style.transition = 'none';
    track.style.transform = `translateX(-${position * itemWidth}px)`;

    function scrollCarousel(direction) {
        if (isAnimating) return;
        isAnimating = true;

        position += direction;
        track.style.transition = 'transform 0.4s ease';
        track.style.transform = `translateX(-${position * itemWidth}px)`;

        track.addEventListener('transitionend', function handler() {
            track.removeEventListener('transitionend', handler);

            // Loop forward
            if (position >= realItems + clones.length / 2) {
                position = clones.length / 2;
                track.style.transition = 'none';
                track.style.transform = `translateX(-${position * itemWidth}px)`;
                void track.offsetWidth;
                track.style.transition = 'transform 0.4s ease';
            }

            // Loop backward
            if (position < clones.length / 2) {
                position = realItems + clones.length / 2 - 1;
                track.style.transition = 'none';
                track.style.transform = `translateX(-${position * itemWidth}px)`;
                void track.offsetWidth;
                track.style.transition = 'transform 0.4s ease';
            }

            isAnimating = false;
        });
    }

    window.scrollCarousel = scrollCarousel;
});