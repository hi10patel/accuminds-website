// Numbers: count up once when the stats scroll into view (1.2s, power2.out).
//   data-count="240"   real value: counted up, or shown as-is without motion
//   data-count="TODO"  placeholder: left as the literal "TODO" text
//   /?todo&demo        preview only: TODO stats count to their data-demo value
import { MQ } from './core.js';

const format = (n) => Math.round(n).toLocaleString('en-US');

export function initStats(motion) {
  const nums = [...document.querySelectorAll('.stat-num')];
  if (!nums.length) return;

  const demo = document.documentElement.classList.contains('show-todo')
    && /[?&]demo(=|&|$)/.test(location.search);

  const targets = nums.flatMap((el) => {
    let raw = el.dataset.count?.trim() ?? '';
    if (!/^\d+(\.\d+)?$/.test(raw) && demo && el.dataset.demo) {
      raw = el.dataset.demo;
      el.setAttribute('data-demo-shown', '');
    }
    if (!/^\d+(\.\d+)?$/.test(raw)) return [];
    const value = Number(raw);
    el.textContent = format(value); // final value: no-JS fallback is the markup, this covers demo
    return [{ el, value }];
  });

  if (!motion.enabled || !targets.length) return;
  const { gsap } = motion;

  motion.mm.add(MQ.motion, () => {
    targets.forEach(({ el, value }, i) => {
      const counter = { v: 0 };
      el.textContent = '0';
      gsap.to(counter, {
        v: value,
        duration: 1.2,
        delay: i * 0.1,
        ease: 'power2.out',
        onUpdate: () => { el.textContent = format(counter.v); },
        scrollTrigger: { trigger: el.closest('.stats') ?? el, start: 'top 85%', once: true },
      });
    });
    return () => targets.forEach(({ el, value }) => { el.textContent = format(value); });
  });
}
