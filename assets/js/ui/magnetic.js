// Magnetic CTAs: [data-magnetic] elements lean gently toward the pointer.
// Fine pointers only, never with reduced motion. Max offset 8px, 0.6s ease-out.

const STRENGTH = 0.3;
const MAX = 8;

export function initMagnetic(motion) {
  if (!motion.enabled) return;
  const { gsap } = motion;

  motion.mm.add('(prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine)', () => {
    const clamp = gsap.utils.clamp(-MAX, MAX);

    const cleanups = gsap.utils.toArray('[data-magnetic]').map((el) => {
      const xTo = gsap.quickTo(el, 'x', { duration: 0.6, ease: 'power3.out' });
      const yTo = gsap.quickTo(el, 'y', { duration: 0.6, ease: 'power3.out' });

      const move = (e) => {
        const r = el.getBoundingClientRect();
        xTo(clamp((e.clientX - (r.left + r.width / 2)) * STRENGTH));
        yTo(clamp((e.clientY - (r.top + r.height / 2)) * STRENGTH));
      };
      const leave = () => {
        xTo(0);
        yTo(0);
      };

      el.addEventListener('pointermove', move);
      el.addEventListener('pointerleave', leave);
      return () => {
        el.removeEventListener('pointermove', move);
        el.removeEventListener('pointerleave', leave);
        gsap.set(el, { x: 0, y: 0 });
      };
    });

    return () => cleanups.forEach((fn) => fn());
  });
}
