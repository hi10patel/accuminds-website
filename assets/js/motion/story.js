// Hero story: "TANGLED → CLARITY" scroll sequence.
//
// The scroll timeline (giant words, captions, final headline) runs on the page
// with GSAP alone. The 3D wire ball comes from assets/js/story.bundle.js
// (three.js), which loads on the visitor's first interaction (mouse move,
// scroll or touch), so its start-up never competes with the first paint.
// Until then, and whenever WebGL 2 is missing, a poster image of the ball sits
// exactly where the 3D ball renders. Reduced motion: static layout (CSS default)
// with the logo image and the final headline; nothing here runs.
import { MQ } from './core.js';

const BUNDLE = new URL('../story.bundle.js', import.meta.url).href;

// Must match scene.js / the poster render (see tools/story-poster.html).
const BALL = { x: -0.35, y: 0.05, half: 1.12 };
const FOV = 32;
function cameraDistance(aspect) {
  return Math.max(9.2, 2.45 / (Math.tan((FOV * Math.PI) / 360) * aspect));
}

export function initStory(motion) {
  const root = document.documentElement;
  const track = document.querySelector('.story-track');
  if (!track || !motion.enabled || !root.classList.contains('story-live')) return;
  const { gsap } = motion;
  const stage = track.querySelector('.story');
  const canvas = stage.querySelector('.story-canvas');
  const poster = stage.querySelector('.story-poster');
  const state = { t: 0, rise: 0 };
  initPauseToggle(stage.querySelector('.motion-toggle'), motion);

  // ---- Poster: place the ball image where the 3D ball will be
  const placePoster = () => {
    const w = stage.clientWidth, h = stage.clientHeight;
    const unit = (h / 2) / (cameraDistance(w / h) * Math.tan((FOV * Math.PI) / 360));
    const size = BALL.half * 2 * unit;
    poster.style.width = `${size}px`;
    poster.style.left = `${w / 2 + (BALL.x - BALL.half) * unit}px`;
    poster.style.top = `${h / 2 - (BALL.y + BALL.half) * unit}px`;
  };
  new ResizeObserver(placePoster).observe(stage);
  placePoster();

  // ---- Scroll timeline
  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: { trigger: track, start: 'top top', end: 'bottom bottom', scrub: 0.9, invalidateOnRefresh: true },
  });
  tl.to(state, { t: 1, duration: 1 }, 0)
    .to(state, { rise: 1, duration: 0.3, ease: 'power2.inOut' }, 0.7)
    .to(poster, { opacity: 0, duration: 0.06 }, 0.04) // poster only ever stands in for the t = 0 frame
    .to('.word--tangled', { opacity: 0, letterSpacing: '0.12em', filter: 'blur(10px)', duration: 0.22, ease: 'power1.in' }, 0.18)
    .fromTo('.word--clarity', { opacity: 0, letterSpacing: '0.18em', filter: 'blur(12px)' },
      { opacity: 1, letterSpacing: '-0.04em', filter: 'blur(0px)', duration: 0.3, ease: 'power2.out' }, 0.62)
    .fromTo('.cap--1', { opacity: 1, y: 0 }, { opacity: 0, y: -20, duration: 0.12 }, 0.14)
    .fromTo('.cap--2', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.1 }, 0.3)
    .to('.cap--2', { opacity: 0, y: -20, duration: 0.1 }, 0.55)
    .to('.story-hint', { opacity: 0, duration: 0.05 }, 0.02)
    // CLARITY lifts with the spiral to make room for the final headline
    .to('.word--clarity', { y: () => -window.innerHeight * 0.16, duration: 0.28, ease: 'power2.inOut' }, 0.72)
    .fromTo('.story-final', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.14, ease: 'power2.out' }, 0.84)
    .fromTo('.story-progress span', { scaleX: 0 }, { scaleX: 1, duration: 1 }, 0);

  // ---- Load-in: letters rise, ball poster settles
  gsap.from('.word--tangled .ch', { yPercent: 110, duration: 1, stagger: 0.04, ease: 'power3.out', delay: 0.1 });
  gsap.from(poster, { scale: 0.92, opacity: 0, duration: 1.2, ease: 'power3.out' });
  gsap.from('.cap--1, .story-hint', { opacity: 0, y: 16, duration: 0.9, delay: 0.6, ease: 'power2.out' });

  // ---- 3D on demand
  if (!webgl2() || navigator.connection?.saveData) return;
  const small = !matchMedia(`${MQ.desktop} and (hover: hover) and (pointer: fine)`).matches;
  let started = false;
  const start = async () => {
    if (started) return;
    started = true;
    try {
      const { startScene } = await import(BUNDLE);
      await startScene({ canvas, stage, state, small, isPaused: () => motion.paused });
      gsap.to(canvas, { opacity: 1, duration: 0.6, ease: 'power1.out' });
      // The live ball takes over: retire the poster for good (visibility, so the
      // scrubbed opacity tween can never bring it back over the canvas).
      gsap.to(poster, {
        autoAlpha: 0, duration: 0.6, delay: 0.15, ease: 'power1.out',
        onComplete: () => { poster.hidden = true; },
      });
      root.classList.add('story-3d');
    } catch (err) {
      console.warn('3D hero unavailable, keeping the poster.', err);
    }
  };

  // First interaction starts the 3D: a mouse move on desktop, scroll or touch on
  // phones. The poster shows the identical first frame until then, so loading
  // three.js never competes with the page's own start-up.
  const events = ['pointermove', 'scroll', 'wheel', 'touchstart', 'pointerdown', 'keydown'];
  const once = () => { events.forEach((e) => removeEventListener(e, once)); start(); };
  events.forEach((e) => addEventListener(e, once, { passive: true }));
}

function webgl2() {
  try { return Boolean(window.WebGL2RenderingContext && document.createElement('canvas').getContext('webgl2')); } catch { return false; }
}

// "Pause motion" (WCAG 2.2.2): stops the ball's idle drift; scrolling still drives the story.
function initPauseToggle(button, motion) {
  if (!button) return;
  const label = button.querySelector('.motion-toggle__label');
  const render = (paused) => { label.textContent = paused ? 'Play motion' : 'Pause motion'; };
  render(motion.paused);
  motion.onPause(render);
  button.addEventListener('click', () => motion.setPaused(!motion.paused));
}
