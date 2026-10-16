// Automation showcase: messy workbook → reconciled dashboard.
// Plays once when scrolled into view (~5s), Replay restarts it.
//   Desktop: problems flag, cells clean up, duplicate row collapses, ticks
//            land, then the dashboard builds (KPIs count up, bars grow).
//   Small screens: flags, then a straight cross-fade into the dashboard.
//   Reduced motion / no JS: static before + after side by side (markup default).
//   "Pause motion" on arrival: jump to the finished dashboard.
import { MQ } from './core.js';

const ROW_H = 36; // must match the generated scene

export function initShowcase(motion) {
  const root = document.querySelector('.showcase');
  if (!root || !motion.enabled) return;
  const { gsap } = motion;

  const before = root.querySelector('.showcase-panel--before');
  const after = root.querySelector('.showcase-panel--after');
  const replay = root.querySelector('.showcase-replay');
  const tabs = root.querySelectorAll('.showcase-tab');
  const q = (panel, sel) => [...panel.querySelectorAll(sel)];

  const setTab = (name) => tabs.forEach((t) => t.classList.toggle('is-active', t.dataset.tab === name));
  const kpis = q(after, '.kpi-value');
  const formatKpi = (el, v) => {
    el.textContent = el.dataset.format === 'of5'
      ? `${Math.round(v)} of 5`
      : `AED ${v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  motion.mm.add({ full: `${MQ.motion} and (min-width: 768px)`, small: `${MQ.motion} and (max-width: 767px)` }, (ctx) => {
    const { full } = ctx.conditions;
    root.classList.add('is-animated');

    const flags = q(before, '.flag');
    const fills = q(before, '.problem-fill, .dup-fill');
    const messy = q(before, '.messy');
    const clean = q(before, '.clean');
    const ticks = q(before, '.tick');
    const dup = before.querySelector('.dup-row');
    const below = q(before, '.row-below');
    const tiles = q(after, '.tile');
    const mBars = q(after, '.m-bar');
    const sBars = q(after, '.s-bar');
    const chip = after.querySelector('.chip');

    const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
    tl.call(setTab, ['before'], 0)
      .set(after, { autoAlpha: 0 }, 0)
      .set(before, { autoAlpha: 1, scale: 1 }, 0)
      .fromTo(flags, { opacity: 0, scale: 0.4, transformOrigin: '100% 0%' },
        { opacity: 1, scale: 1, duration: 0.5, stagger: 0.1 }, 0.3);

    if (full) {
      tl.addLabel('clean', '+=0.5')
        .to(messy, { opacity: 0, x: (i, el) => Number(el.dataset.dx || 0), duration: 0.6, stagger: 0.03 }, 'clean')
        .fromTo(clean, { opacity: 0 }, { opacity: 1, duration: 0.6, stagger: 0.03 }, 'clean+=0.2')
        .to([...flags, ...fills], { opacity: 0, duration: 0.5 }, 'clean+=0.2')
        .to(dup, { opacity: 0, duration: 0.5 }, 'clean+=0.3')
        .to(below, { y: -ROW_H, duration: 0.7, ease: 'power3.out' }, 'clean+=0.6')
        .fromTo(ticks, { opacity: 0, scale: 0.5, transformOrigin: '50% 50%' },
          { opacity: 1, scale: 1, duration: 0.45, stagger: 0.07 }, 'clean+=0.9')
        .addLabel('dash', '+=0.7');
    } else {
      tl.addLabel('dash', '+=0.9');
    }

    // Workbook leaves before the dashboard arrives, so the two never ghost over each other.
    tl.to(before, { autoAlpha: 0, scale: 0.98, duration: 0.45, ease: 'power1.in' }, 'dash')
      .fromTo(after, { autoAlpha: 0, scale: 1.02 }, { autoAlpha: 1, scale: 1, duration: 0.7 }, 'dash+=0.4')
      .call(setTab, ['after'], 'dash+=0.4')
      .fromTo(tiles, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.6, stagger: 0.1 }, 'dash+=0.6')
      .fromTo(chip, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 'dash+=0.7');

    kpis.forEach((el, i) => {
      const counter = { v: 0 };
      tl.to(counter, {
        v: Number(el.dataset.value), duration: 1, ease: 'power2.out',
        onUpdate: () => formatKpi(el, counter.v),
      }, `dash+=${0.7 + i * 0.1}`);
    });

    tl.fromTo(mBars, { scaleY: 0, transformOrigin: '50% 100%' }, { scaleY: 1, duration: 0.7, stagger: 0.08 }, 'dash+=0.9')
      .fromTo(sBars, { scaleX: 0, transformOrigin: '0% 50%' }, { scaleX: 1, duration: 0.7, stagger: 0.08 }, 'dash+=1');

    setTab('before');
    tl.progress(0);

    const st = window.ScrollTrigger.create({
      trigger: root,
      start: 'top 65%',
      once: true,
      onEnter: () => (motion.paused ? tl.progress(1) : tl.play(0)),
    });

    const onReplay = () => tl.restart();
    replay.addEventListener('click', onReplay);

    return () => {
      replay.removeEventListener('click', onReplay);
      st.kill();
      root.classList.remove('is-animated');
      tabs.forEach((t) => t.classList.remove('is-active'));
      kpis.forEach((el) => formatKpi(el, Number(el.dataset.value)));
    };
  });
}
