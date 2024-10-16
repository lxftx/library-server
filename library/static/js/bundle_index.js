/******/ (() => { // webpackBootstrap
/*!***************************!*\
  !*** ./src/js/scripts.js ***!
  \***************************/
document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('.logo__window-item'),
        inner = document.querySelector('.logo__window-inner'),
        wrapper = document.querySelector('.logo__window-wrapper'),
        window_slider = document.querySelector('.logo__window'),
        width = window.getComputedStyle(window_slider).width;
    let offer = 0,
        slide = 0;

    wrapper.style.overflow = 'hidden';
    inner.style.display = 'flex';
    inner.style.width = sliders.length * 100 + '%';
    inner.style.transition = '0.5s all';


    const elem_dot_ul = document.createElement('ol');
    elem_dot_ul.classList.add('slider-dot');

    for (let i=0; i < sliders.length; i++) {
        let dot = document.createElement('li');
        dot.setAttribute('data-slide-to', i + 1);
        dot.classList.add('dot');
        if (i==slide) dot.style.backgroundColor = 'black';
        elem_dot_ul.append(dot);
    };

    window_slider.append(elem_dot_ul);

    const dots = elem_dot_ul.querySelectorAll('li');

    dots.forEach(item => {
        item.addEventListener('click', (event) => {
            slide = +event.target.getAttribute('data-slide-to');
            indexSlide(slide);
        });
    });

    function indexSlide(index) {
        // Функция подсчета и перехода на другую картину
        if (index > sliders.length) slide = 1;
        if (index < 1) slide = sliders.length;
        offer = +width.slice(0, width.length - 2) * (slide - 1);
        
        inner.style.transform = `translateX(-${offer}px)`;
        resetStyleDot(slide);
    }

    function resetStyleDot(index) {
        // Функция сброса стилей у кнопок активностей и наделение определеной кнопки стиля
        dots.forEach(item => item.style.backgroundColor = '');
        dots[index-1].style.backgroundColor = 'black';
    }

    setInterval(() => {
        slide += 1;
        indexSlide(slide);
    }, 5000);


})
/******/ })()
;
//# sourceMappingURL=bundle.js.map