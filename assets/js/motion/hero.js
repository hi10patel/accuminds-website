// Hero intro: 3D mark reveal, staggered headline, supporting copy.
// Runs once on load (not tied to breakpoints, so rotating a phone never replays it).
//   Desktop: ball grows in through a circular clip, then a sweep unrolls the
//            strand and spiral (geometry from design/logo-animation; the
//            prototype's shake phase is intentionally dropped).
//   Mobile:  simple left-to-right wipe.
//   Reduced motion: everything visible, copy fades in briefly.
import { MQ } from './core.js';
import { initNetwork } from './network.js';

// Ball and sweep geometry as fractions of the 1380×560 image box.
const BALL = { cx: 0.2125, cy: 0.575, r: 0.1875 }; // r is a fraction of width
const SWEEP_X0 = 0.2458;

export function initHero(motion) {
  const hero = document.querySelector('.hero');
  if (!hero) return;

  initNetwork(hero.querySelector('.hero-network'), motion);
  initPauseToggle(hero.querySelector('.motion-toggle'), motion);
  if (!motion.enabled) return;

  const { gsap } = motion;
  const title = hero.querySelector('.hero-title');
  const words = splitWords(title);
  const clip = hero.querySelector('.hero-mark__clip');
  const fades = hero.querySelectorAll('[data-hero-fade]');
  const [eyebrow, lead, ...rest] = fades;

  if (matchMedia(MQ.reduce).matches) {
    gsap.set(title, { visibility: 'visible' });
    gsap.fromTo([title, ...fades], { opacity: 0 }, { opacity: 1, duration: 0.4, ease: 'power1.out' });
    return;
  }

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  gsap.set(words, { yPercent: 110 });
  gsap.set(title, { visibility: 'visible' });

  if (matchMedia('(min-width: 768px)').matches) {
    tl.add(markReveal(clip, gsap), 0);
  } else {
    tl.fromTo(clip,
      { clipPath: 'inset(0% 100% 0% 0%)' },
      {
        clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power2.out',
        // Explicit 'none' (not clearProps), or the CSS start state would hide it again.
        onComplete: () => { clip.style.clipPath = 'none'; },
      }, 0);
  }

  tl.fromTo(eyebrow, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.6 }, 0.25)
    .to(words, { yPercent: 0, duration: 0.9, stagger: 0.06 }, 0.35)
    .fromTo(lead, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8 }, 0.9)
    .fromTo(rest, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.7, stagger: 0.08 }, 1.05);
}

// Wrap each word in a mask so it can rise into place. Spaces stay as text
// nodes, so screen readers and copy/paste see the original sentence.
function splitWords(title) {
  const words = [];
  title.querySelectorAll('.line').forEach((line) => {
    const parts = line.textContent.trim().split(/\s+/);
    line.textContent = '';
    parts.forEach((text, i) => {
      const outer = document.createElement('span');
      const inner = document.createElement('span');
      outer.className = 'word';
      inner.className = 'word__inner';
      inner.textContent = text;
      outer.append(inner);
      line.append(outer);
      if (i < parts.length - 1) line.append(' ');
      words.push(inner);
    });
  });
  return words;
}

// Clip-path reveal: circle(r) for the ball, then the union of the full ball
// and a widening rectangle for the strand + spiral.
function markReveal(el, gsap) {
  const state = { r: 0, sweep: SWEEP_X0 };

  const circle = () => {
    const w = el.offsetWidth;
    const h = el.offsetHeight;
    return `circle(${(state.r * w).toFixed(1)}px at ${(BALL.cx * w).toFixed(1)}px ${(BALL.cy * h).toFixed(1)}px)`;
  };

  const union = () => {
    const w = el.offsetWidth;
    const h = el.offsetHeight;
    const cx = BALL.cx * w;
    const cy = BALL.cy * h;
    const r = state.r * w;
    const x0 = SWEEP_X0 * w;
    const sx = state.sweep * w;
    const pts = [];
    const arc = (from, to, steps) => {
      for (let i = 0; i <= steps; i++) {
        const a = from + ((to - from) * i) / steps;
        pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
      }
    };

    // Right edge: rectangle top, then the ball's right side if it still pokes out.
    pts.push([x0, 0], [sx, 0]);
    if (sx < cx + r) {
      const dy = Math.sqrt(r * r - (sx - cx) ** 2);
      arc(Math.atan2(-dy, sx - cx), Math.atan2(dy, sx - cx), 16);
    }
    pts.push([sx, h], [x0, h]);
    // Left edge: the ball's left side, from where it meets x0 at the bottom round to the top.
    const dy0 = Math.sqrt(r * r - (x0 - cx) ** 2);
    arc(Math.atan2(dy0, x0 - cx), Math.atan2(-dy0, x0 - cx) + Math.PI * 2, 40);

    return `polygon(${pts.map(([x, y]) => `${x.toFixed(1)}px ${y.toFixed(1)}px`).join(',')})`;
  };

  return gsap.timeline()
    .to(state, {
      r: BALL.r, duration: 0.8, ease: 'power3.out',
      onUpdate: () => { el.style.clipPath = circle(); },
    })
    .to(state, {
      sweep: 1, duration: 1.2, ease: 'power2.out',
      onUpdate: () => { el.style.clipPath = union(); },
      onComplete: () => { el.style.clipPath = 'none'; },
    }, '-=0.1');
}

function initPauseToggle(button, motion) {
  if (!button) return;
  const label = button.querySelector('.motion-toggle__label');
  const render = (paused) => {
    label.textContent = paused ? 'Play motion' : 'Pause motion';
  };
  render(motion.paused);
  motion.onPause(render);
  button.addEventListener('click', () => motion.setPaused(!motion.paused));
}
