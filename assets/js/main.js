// Entry point. GSAP, ScrollTrigger and Lenis are loaded as deferred classic
// scripts before this module (see index.html), so they are on `window` here.
//
// Above the fold (hero, header) starts immediately; everything below the fold
// is set up in separate idle tasks so the page stays responsive while loading.
import { createMotion, initReveals, runWhenIdle } from './motion/core.js';
import { initHero } from './motion/hero.js';
import { initServiceIcons } from './motion/icons.js';
import { initProcess } from './motion/process.js';
import { initShowcase } from './motion/showcase.js';
import { initStats } from './motion/stats.js';
import { initNav } from './ui/nav.js';
import { initMagnetic } from './ui/magnetic.js';
import { initContact } from './ui/contact.js';

const motion = createMotion();
initHero(motion);
initNav(motion);

runWhenIdle([
  () => initReveals(motion),
  () => initServiceIcons(motion),
  () => initProcess(motion),
  () => initShowcase(motion),
  () => initStats(motion),
  () => initMagnetic(motion),
  () => initContact(motion),
], motion);

document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = String(new Date().getFullYear());
});
