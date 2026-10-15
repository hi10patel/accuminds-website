// "How we work": the gold line draws as you scroll and each step lights up
// when the line reaches it.
//   Desktop (≥1024 wide, ≥640 tall): section pins for 1.5 viewports, scrubbed.
//   Smaller screens: no pin; the vertical line scrubs through the section.
//   Reduced motion / no JS: the finished state in the markup (all steps lit).

const PIN = '(prefers-reduced-motion: no-preference) and (min-width: 1024px) and (min-height: 640px)';
const FLOW = '(prefers-reduced-motion: no-preference) and (max-width: 1023px), '
  + '(prefers-reduced-motion: no-preference) and (max-height: 639px)';

export function initProcess(motion) {
  const section = document.getElementById('process');
  const wrap = section?.querySelector('.process');
  if (!wrap) return;
  const line = wrap.querySelector('.process-line');
  const nums = [...wrap.querySelectorAll('.process-num')];
  const bodies = [...wrap.querySelectorAll('.process-body')];

  // Vertical rail runs from the first circle's centre to the last one's.
  const measure = () => {
    const first = nums[0];
    const last = nums[nums.length - 1];
    wrap.style.setProperty('--track-top', `${first.offsetTop + first.offsetHeight / 2}px`);
    wrap.style.setProperty('--track-len', `${last.offsetTop - first.offsetTop}px`);
  };
  measure();
  new ResizeObserver(measure).observe(wrap);

  if (!motion.enabled) return;
  const { gsap } = motion;
  const css = getComputedStyle(document.documentElement);
  const token = (name) => css.getPropertyValue(name).trim();
  const ACTIVE = { backgroundColor: token('--gold'), borderColor: token('--gold'), color: token('--navy') };
  const IDLE = { backgroundColor: token('--surface'), borderColor: token('--ink-300'), color: token('--ink-600') };

  motion.mm.add({ pin: PIN, flow: FLOW }, (ctx) => {
    const { pin } = ctx.conditions;
    const axis = pin ? 'scaleX' : 'scaleY';
    if (pin) section.classList.add('is-pinned');

    // Step 1 is lit from the start; the rest wait for the line.
    gsap.set(line, { [axis]: 0 });
    gsap.set(nums.slice(1), IDLE);
    gsap.set(bodies.slice(1), { opacity: 0.25, y: 12 });

    const tl = gsap.timeline({
      defaults: { ease: 'power2.out' },
      scrollTrigger: pin
        ? {
          trigger: section, start: 'top top', end: '+=150%',
          pin: true, scrub: 0.6, anticipatePin: 1,
          // Refresh before the earlier-created reveal triggers further down,
          // so their positions include this pin's extra scroll distance.
          refreshPriority: 1,
        }
        : { trigger: wrap, start: 'top 75%', end: 'bottom 55%', scrub: 0.5 },
    });

    // Timeline units: line runs 0.3 → 3.3; step i lights as the line reaches it.
    tl.to(line, { [axis]: 1, duration: 3, ease: 'none' }, 0.3);
    for (let i = 1; i < nums.length; i++) {
      const at = 0.3 + i - 0.15;
      tl.to(nums[i], { ...ACTIVE, duration: 0.35 }, at)
        .to(bodies[i], { opacity: 1, y: 0, duration: 0.45 }, at);
    }
    tl.to({}, { duration: 0.4 }); // short hold before the pin releases

    return () => section.classList.remove('is-pinned');
  });
}
