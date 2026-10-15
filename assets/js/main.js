// Entry point. GSAP, ScrollTrigger and Lenis are loaded as deferred classic
// scripts before this module (see index.html), so they are on `window` here.
import { createMotion } from './motion/core.js';
import { initNav } from './ui/nav.js';
import { initMagnetic } from './ui/magnetic.js';

const motion = createMotion();
initNav(motion);
initMagnetic(motion);

document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = String(new Date().getFullYear());
});
