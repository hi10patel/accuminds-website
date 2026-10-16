// Service icons: small looping SVG animations, one per pillar.
// Each loop = build → hold on the finished frame ('rest') → quiet reset.
// Loops run only while their card is on screen and motion isn't paused;
// when stopped they park on 'rest', which is also the SVG's default markup,
// so no-JS and reduced-motion visitors see the same finished icons.
import { MQ } from './core.js';

const HOLD = 1.8;   // seconds the finished icon stays before resetting
const EASE = 'power2.out';

// Stroke "draw" via pathLength="1" + stroke-dasharray: 1 (see main.css).
const DRAW_FROM = { strokeDashoffset: 1, opacity: 0 };
const DRAW_TO = { strokeDashoffset: 0, opacity: 1, ease: EASE };

const BUILDERS = {
  // Core Accounting: ledger rows draw in, then the gold double underline.
  ledger(svg, tl) {
    const rows = svg.querySelectorAll('.row');
    const total = svg.querySelectorAll('.total');
    tl.fromTo(rows, DRAW_FROM, { ...DRAW_TO, duration: 0.6, stagger: 0.25 })
      .fromTo(total, DRAW_FROM, { ...DRAW_TO, duration: 0.5, stagger: 0.12 }, '-=0.1')
      .addLabel('rest')
      .to([...rows, ...total], { opacity: 0, duration: 0.5, ease: 'power1.inOut' }, `+=${HOLD}`);
  },

  // FTA Compliance: ring draws, VAT ticks 0% → 5%, a check stamp lands.
  vat(svg, tl, gsap) {
    const ring = svg.querySelector('.ring');
    const num = svg.querySelector('.vat-num');
    const stamp = svg.querySelectorAll('.stamp .draw');
    const count = { v: 5 };
    const show = () => { num.textContent = `${Math.round(count.v)}%`; };
    tl.fromTo(ring, DRAW_FROM, { ...DRAW_TO, duration: 0.8 })
      .fromTo(num, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: EASE }, 0.1)
      .fromTo(count, { v: 0 }, { v: 5, duration: 1, ease: 'power1.out', onUpdate: show }, 0.2)
      .fromTo(stamp, DRAW_FROM, { ...DRAW_TO, duration: 0.45, stagger: 0.15 }, '-=0.05')
      .addLabel('rest')
      .to([ring, num, ...stamp], { opacity: 0, duration: 0.5, ease: 'power1.inOut' }, `+=${HOLD}`);
    gsap.set(count, { v: 5 });
    show();
  },

  // CFO Advisory: bars rise, trend line and arrow draw over them.
  growth(svg, tl, gsap) {
    const bars = svg.querySelectorAll('.bar');
    const trend = svg.querySelectorAll('.trend');
    gsap.set(bars, { transformOrigin: '50% 100%' });
    tl.fromTo(bars, { scaleY: 0, opacity: 1 }, { scaleY: 1, duration: 0.6, stagger: 0.15, ease: EASE })
      .fromTo(trend, DRAW_FROM, { ...DRAW_TO, duration: 0.7, stagger: 0.3 }, '-=0.15')
      .addLabel('rest')
      .to([...bars, ...trend], { opacity: 0, duration: 0.5, ease: 'power1.inOut' }, `+=${HOLD}`);
  },

  // AI Automation: a scan line passes down the document, fields light up, sparkle.
  scan(svg, tl) {
    const beam = svg.querySelector('.beam');
    const fields = svg.querySelectorAll('.field');
    const spark = svg.querySelector('.spark');
    tl.set(fields, { opacity: 0.3 })
      .set(spark, { opacity: 0, scale: 0.6, transformOrigin: '50% 50%' })
      .fromTo(beam, { y: 0, opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'none' })
      .to(beam, { y: 13, duration: 1.2, ease: 'power1.inOut' }, '<')
      .to(fields[0], { opacity: 1, duration: 0.3, ease: EASE }, 0.45)
      .to(fields[1], { opacity: 1, duration: 0.3, ease: EASE }, 0.7)
      .to(fields[2], { opacity: 1, duration: 0.3, ease: EASE }, 0.95)
      .to(beam, { opacity: 0, duration: 0.25, ease: 'none' }, 1.15)
      .to(spark, { opacity: 1, scale: 1, duration: 0.5, ease: EASE }, 1.2)
      .addLabel('rest')
      .to([...fields, spark], { opacity: 0.3, duration: 0.5, ease: 'power1.inOut' }, `+=${HOLD}`);
  },

  // Payroll & WPS: calendar page slides up to the next month, payday is ringed.
  calendar(svg, tl) {
    const page = svg.querySelector('.cal-page');
    const pay = svg.querySelector('.pay');
    tl.to(pay, { opacity: 0, duration: 0.3, ease: 'power1.inOut' })
      .to(page, { y: -6, opacity: 0, duration: 0.45, ease: 'power1.in' })
      .fromTo(page, { y: 6, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: EASE })
      .fromTo(pay, DRAW_FROM, { ...DRAW_TO, duration: 0.6 }, '-=0.05')
      .addLabel('rest')
      .to({}, { duration: HOLD });
  },
};

export function initServiceIcons(motion) {
  if (!motion.enabled) return;
  const { gsap } = motion;
  const { ScrollTrigger } = window;

  motion.mm.add(MQ.motion, () => {
    const stops = [];

    gsap.utils.toArray('[data-icon]').forEach((svg, i) => {
      const build = BUILDERS[svg.dataset.icon];
      if (!build) return;

      // Slightly different repeat delays keep the five loops from syncing up.
      const tl = gsap.timeline({ paused: true, repeat: -1, repeatDelay: 0.3 + i * 0.15 });
      build(svg, tl, gsap);
      // Start blank (the card is still hidden by its reveal) so the first entry
      // builds the icon; if the visitor has paused motion, show it finished.
      tl.seek(motion.paused ? 'rest' : 0, false);

      let inView = false;
      const sync = () => {
        if (inView && !motion.paused) {
          if (tl.paused()) tl.restart();
        } else if (!tl.paused()) {
          tl.pause().seek('rest', false);
        }
      };

      const card = svg.closest('.svc-card') ?? svg;
      ScrollTrigger.create({
        trigger: card,
        start: 'top 85%',
        end: 'bottom 10%',
        onToggle: (self) => {
          inView = self.isActive;
          // First entry waits for the card's own reveal to settle.
          gsap.delayedCall(inView ? 0.4 + i * 0.12 : 0, sync);
        },
      });
      stops.push(motion.onPause(sync));
    });

    return () => stops.forEach((off) => off());
  });
}
