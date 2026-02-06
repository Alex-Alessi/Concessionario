document.addEventListener('DOMContentLoaded', () => {

    const modernTrack = document.getElementById('modernCarouselTrack');
    if (!modernTrack) return; // sicurezza

    const modernItems = document.querySelectorAll('.modern-carousel-item');
    const modernPrevBtn = document.getElementById('modernPrevBtn');
    const modernNextBtn = document.getElementById('modernNextBtn');
    const modernIndicatorsContainer = document.getElementById('modernIndicators');
    const modernCurrentCounter = document.querySelector('.modern-carousel-counter .current');

    let modernCurrentIndex = 0;
    const modernTotalItems = modernItems.length;

    // indicatori
    for (let i = 0; i < modernTotalItems; i++) {
        const indicator = document.createElement('div');
        indicator.classList.add('modern-indicator');
        if (i === 0) indicator.classList.add('active');
        indicator.addEventListener('click', () => goToSlide(i));
        modernIndicatorsContainer.appendChild(indicator);
    }

    const modernIndicators = document.querySelectorAll('.modern-indicator');

    function updateCarousel() {
        const itemWidth = 400;
        const gap = 30;
        const offset = modernCurrentIndex * (itemWidth + gap);

        modernTrack.style.transform = `translateX(-${offset}px)`;

        modernItems.forEach((item, i) =>
            item.classList.toggle('active', i === modernCurrentIndex)
        );

        modernIndicators.forEach((ind, i) =>
            ind.classList.toggle('active', i === modernCurrentIndex)
        );

        modernCurrentCounter.textContent =
            (modernCurrentIndex + 1).toString().padStart(2, '0');
    }

    function goToSlide(i) {
        modernCurrentIndex = i;
        updateCarousel();
    }

    function next() {
        modernCurrentIndex = (modernCurrentIndex + 1) % modernTotalItems;
        updateCarousel();
    }

    function prev() {
        modernCurrentIndex =
            (modernCurrentIndex - 1 + modernTotalItems) % modernTotalItems;
        updateCarousel();
    }

    modernNextBtn?.addEventListener('click', next);
    modernPrevBtn?.addEventListener('click', prev);


    
});
