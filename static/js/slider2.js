const slidero = document.querySelector('.slider2');
const prevButtono = document.querySelector('.prev-button2');
const nextButtono = document.querySelector('.next-button2');
const slideso = Array.from(slidero.querySelectorAll('img'));
const slideCounto = slideso.length;
let slideIndexo = 0;

prevButtono.addEventListener('click', () => {
  slideIndexo = (slideIndexo - 1 + slideCounto) % slideCounto;
  slideo();
});

nextButtono.addEventListener('click', () => {
  slideIndexo = (slideIndexo + 1) % slideCounto;
  slideo();
});

const slideo = () => {
  const imageWidth = slidero.clientWidth;
  const slideOffset = -slideIndexo * imageWidth;
  slidero.style.transform = `translateX(${slideOffset}px)`;
}

window.addEventListener('load', () => {
  slideo();
});