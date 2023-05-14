AOS.init({
   once: false, 
   easing: 'ease-out-back',   // Choose a different easing function
   duration: 1200,            // Change the duration of the animations
   delay: 100,                // Change the initial delay of the animations
});

// Initialize Headroom.js
const header = document.querySelector('header');
const headroom = new Headroom(header, {
   tolerance: 5
});
headroom.init();

// Initialize Parallax.js
const parallaxContainer = document.querySelector('.parallax-container');
const parallaxInstance = new Parallax(parallaxContainer);