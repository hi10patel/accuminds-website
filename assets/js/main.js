// Entry point. GSAP, ScrollTrigger and Lenis are loaded as deferred classic
// scripts before this module (see index.html), so they are on `window` here.
import { createMotion } from './motion/core.js';
import { initHero } from './motion/hero.js';
import { initServiceIcons } from './motion/icons.js';
import { initProcess } from './motion/process.js';
import { initShowcase } from './motion/showcase.js';
import { initNav } from './ui/nav.js';
import { initMagnetic } from './ui/magnetic.js';

const motion = createMotion();
initHero(motion);
initServiceIcons(motion);
initProcess(motion);
initShowcase(motion);
initNav(motion);
initMagnetic(motion);

document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = String(new Date().getFullYear());
});
