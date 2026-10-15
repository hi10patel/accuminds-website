// Header: scrolled shadow, mobile menu, active-section highlight.

const DESKTOP = '(min-width: 900px)';

export function initNav(motion) {
  const header = document.getElementById('site-header');
  const toggle = header?.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');
  if (!header || !toggle || !nav) return;
  const root = document.documentElement;

  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const isOpen = () => toggle.getAttribute('aria-expanded') === 'true';
  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Close menu' : 'Open menu';
    header.classList.toggle('menu-open', open);
    root.classList.toggle('menu-open', open);
    if (motion.lenis) open ? motion.lenis.stop() : motion.lenis.start();
  }

  toggle.addEventListener('click', () => {
    setOpen(!isOpen());
    if (isOpen()) nav.querySelector('a')?.focus();
  });
  nav.addEventListener('click', (e) => {
    if (e.target.closest('a') && isOpen()) setOpen(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });
  document.addEventListener('click', (e) => {
    if (isOpen() && !header.contains(e.target)) setOpen(false);
  });
  matchMedia(DESKTOP).addEventListener('change', (e) => {
    if (e.matches) setOpen(false);
  });

  // Highlight the nav link for the section in the middle of the viewport.
  const links = new Map();
  nav.querySelectorAll('ul a[href^="#"]').forEach((a) => {
    const section = document.querySelector(a.getAttribute('href'));
    if (section) links.set(section, a);
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const link = links.get(entry.target);
      if (entry.isIntersecting) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  links.forEach((_, section) => observer.observe(section));
}
