// Motion core: GSAP + ScrollTrigger + Lenis, switched by media query.
//   - Smooth scroll (Lenis) only with a fine pointer and no reduced-motion preference.
//   - Reduced motion: no Lenis, reveals become short fades, loops stay off.
//   - "Pause motion" stops looping animations (WCAG 2.2.2); scroll reveals still run.

export const MQ = {
  reduce: '(prefers-reduced-motion: reduce)',
  motion: '(prefers-reduced-motion: no-preference)',
  smooth: '(prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine)',
  desktop: '(min-width: 1024px)',
};

const root = document.documentElement;
const PAUSE_KEY = 'am-motion-paused';

function readPaused() {
  try { return localStorage.getItem(PAUSE_KEY) === '1'; } catch { return false; }
}

export function createMotion() {
  const { gsap, ScrollTrigger, Lenis } = window;
  const listeners = new Set();

  const motion = {
    gsap,
    enabled: Boolean(gsap && ScrollTrigger),
    lenis: null,
    mm: null,
    paused: readPaused(),
    setPaused(value) {
      motion.paused = value;
      root.classList.toggle('motion-paused', value);
      try { localStorage.setItem(PAUSE_KEY, value ? '1' : '0'); } catch { /* storage unavailable */ }
      listeners.forEach((fn) => fn(value));
    },
    onPause(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
    scrollTo(target) {
      const el = typeof target === 'string' ? document.querySelector(target) : target;
      if (!el) return;
      // Header clearance comes from CSS scroll-margin-top, which Lenis and
      // scrollIntoView both respect, so no manual offset here.
      if (motion.lenis) {
        motion.lenis.scrollTo(el === document.body ? 0 : el, { duration: 1.2 });
      } else {
        const reduce = matchMedia(MQ.reduce).matches;
        if (el === document.body) window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
        else el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }
      // Move focus for keyboard and screen-reader users without a second jump.
      if (el !== document.body) {
        if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
        el.focus({ preventScroll: true });
      }
    },
  };

  root.classList.toggle('motion-paused', motion.paused);
  initAnchors(motion);

  if (!motion.enabled) {
    // Libraries failed to load: show everything, keep native behaviour.
    root.classList.remove('js-motion');
    return motion;
  }

  gsap.registerPlugin(ScrollTrigger);
  // No automatic refresh on DOMContentLoaded/load: runWhenIdle() refreshes once
  // after setup and again when web fonts are ready, outside the busy load window.
  ScrollTrigger.config({ autoRefreshEvents: 'visibilitychange,resize' });
  gsap.defaults({ ease: 'power3.out', duration: 0.9 });
  motion.mm = gsap.matchMedia();

  if (Lenis) {
    motion.mm.add(MQ.smooth, () => {
      const lenis = new Lenis({ lerp: 0.1, autoRaf: false });
      const raf = (time) => lenis.raf(time * 1000);
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(raf);
      gsap.ticker.lagSmoothing(0);
      motion.lenis = lenis;
      return () => {
        gsap.ticker.remove(raf);
        gsap.ticker.lagSmoothing(500, 33);
        lenis.destroy();
        motion.lenis = null;
      };
    });
  }

  window.__amMotion = true;
  return motion;
}

// Runs each task in its own idle slot (keeps load-time long tasks short), then
// refreshes ScrollTrigger once so every trigger accounts for pins created later.
export function runWhenIdle(tasks, motion) {
  const idle = window.requestIdleCallback
    ? (fn) => requestIdleCallback(fn, { timeout: 1200 })
    : (fn) => setTimeout(fn, 1);
  const align = hashAligner(motion);
  const next = () => {
    const task = tasks.shift();
    if (task) {
      task();
      idle(next);
    } else if (motion.enabled) {
      window.ScrollTrigger.sort();
      window.ScrollTrigger.refresh();
      align();
      // Font swap changes text heights, so re-measure once fonts have loaded.
      document.fonts?.ready.then(() => idle(() => { window.ScrollTrigger.refresh(); align(); }));
    }
  };
  idle(next);
}

// Arriving from another page via a link such as /#contact, the browser jumps to
// the target before pinned sections add their spacing, so it ends up mid-page.
// Re-align to the hash target once layout has settled, unless the visitor has
// started scrolling in the meantime.
function hashAligner(motion) {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id) return () => {};
  let touched = false;
  const stop = () => { touched = true; };
  ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach((type) => addEventListener(type, stop, { once: true, passive: true }));
  return () => {
    const el = document.getElementById(id);
    if (!el || touched) return;
    if (motion.lenis) {
      // Lenis caches the page height; pins just made the page taller.
      motion.lenis.resize();
      motion.lenis.scrollTo(el, { immediate: true, force: true });
    } else {
      el.scrollIntoView({ block: 'start' });
    }
  };
}

function initAnchors(motion) {
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href^="#"]');
    if (!link || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const hash = link.getAttribute('href');
    if (hash === '#') return;
    const target = hash === '#top' ? document.body : document.querySelector(hash);
    if (!target) return;
    e.preventDefault();
    motion.scrollTo(target);
    history.pushState(null, '', hash);
  });
}

// [data-reveal]          fade + rise when scrolled into view
// [data-reveal="mask"]   heading rises through a clipping mask
// [data-reveal-stagger]  children reveal one after another
export function initReveals(motion) {
  if (!motion.enabled) return;
  const { gsap } = motion;

  // Wrap mask headings once, outside matchMedia, so reverts don't re-wrap.
  gsap.utils.toArray('[data-reveal="mask"]').forEach((el) => {
    if (el.querySelector(':scope > .mask')) return;
    const inner = document.createElement('span');
    inner.className = 'mask__inner';
    inner.append(...el.childNodes);
    const mask = document.createElement('span');
    mask.className = 'mask';
    mask.append(inner);
    el.append(mask);
  });

  motion.mm.add({ full: MQ.motion, reduce: MQ.reduce }, (ctx) => {
    const { reduce } = ctx.conditions;
    const trigger = (el) => ({ trigger: el, start: 'top 88%', once: true });

    gsap.utils.toArray('[data-reveal]').forEach((el) => {
      if (reduce) {
        gsap.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.4, ease: 'power1.out', scrollTrigger: trigger(el) });
      } else if (el.dataset.reveal === 'mask') {
        gsap.set(el, { opacity: 1 });
        gsap.fromTo(el.querySelector('.mask__inner'), { yPercent: 105 }, { yPercent: 0, duration: 1, scrollTrigger: trigger(el) });
      } else {
        gsap.fromTo(el, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.9, scrollTrigger: trigger(el) });
      }
    });

    gsap.utils.toArray('[data-reveal-stagger]').forEach((group) => {
      const items = group.children;
      if (reduce) {
        gsap.fromTo(items, { opacity: 0 }, { opacity: 1, duration: 0.4, ease: 'power1.out', scrollTrigger: trigger(group) });
      } else {
        gsap.fromTo(items, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, stagger: 0.12, scrollTrigger: trigger(group) });
      }
    });
  });
}
