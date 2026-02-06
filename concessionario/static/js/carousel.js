// carousel.js
var size = 200;
var margin = 20;
var count = document.querySelectorAll('.carousel__box').length;
var visible = 3; // Visible carousel slides
var last = count - visible;
var offset = 0;
var carousel = (size * visible) + (margin * visible) + (size / 3);
var container = (size * count) + (margin * count);
var barely = size / visible;

var $container = $('.carousel__inner');
var $slides = $('.carousel__box');
var $left = $('.carousel__control--left');
var $right = $('.carousel__control--right');
var $previous = null;
var $next = null;

const carouselEl = document.querySelector('.carousel');
const innerEl = document.querySelector('.carousel__inner');


$left.on('click', function() {
  if ( offset === 0 ) return;
  move(offset - 1);
});

$right.on('click', function() {
  move(offset + 1);
});

$slides.each(function(index, slide) {
  $(slide).data('index', index);
});

$slides.on('mouseenter', _.debounce(function() {
  var $slide = $(this);
  var index = $slide.data('index');
  $previous = previous(index);
  $next = next(index);

  $previous.addClass('carousel__box--previous');
  $next.addClass('carousel__box--next');
  $slide.addClass('carousel__box--enter')
}, 350));

$slides.on('mouseout', _.debounce(function() {
  var $slide = $(this);

  $slide
    .addClass('carousel__box--leave')
    .removeClass('carousel__box--enter')
    .delay(400)
    .queue(function() {
      $(this).removeClass('carousel__box--leave')
        .dequeue();
    });

  $previous.addClass('carousel__box--previous-leave')
    .removeClass('carousel__box--previous')
    .delay(300)
    .queue(function() {
      $(this).removeClass('carousel__box--previous-leave')
        .dequeue();
    });

  $next.addClass('carousel__box--next-leave')
    .removeClass('carousel__box--next')
    .delay(300)
    .queue(function() {
      $(this).removeClass('carousel__box--next-leave')
        .dequeue();
    });
}, 300));

function previous(hovered) {
  var index = hovered - offset;
  var start = offset + visible === count ? offset - 1 : offset;
  return $slides.slice(start, offset + index);
}

function next(hovered) {
  var index = hovered - offset;
  if ( index === visible ) {
    return $slides.slice();
  } else {
    return $slides.slice(offset + index + 1, offset + visible + 1);
  }
}

function move(newOffset) {
  const step = size + margin;
  const translateX = step * newOffset;
  const max = innerEl.scrollWidth - carouselEl.clientWidth;

  if (translateX >= max) {
    offset = Math.floor(max / step);
    $container.css('transform', `translateX(-${max}px)`);
    return;
  }

  offset = newOffset;
  $container.css('transform', `translateX(-${translateX}px)`);
}
