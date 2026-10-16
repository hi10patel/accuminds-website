// Hero background: slow-drifting gold/teal line network on a canvas.
//   Desktop: ~24–48 nodes scaled to hero area, pointer parallax by node depth.
//   Mobile / coarse pointer: 16 nodes, 30 fps cap, no parallax.
//   Reduced motion or "Pause motion": a single static frame.
//   Off screen or tab hidden: no frames are drawn at all.
//   The drift starts after page load (the first frame is drawn immediately), so
//   it doesn't compete with the hero intro and page start-up for the main thread.
//   Lines fade towards the headline area (drawn here rather than with a CSS mask,
//   which would be recomposited on every frame).

const COLORS = {
  gold: '201, 151, 43',   // --gold
  teal: '45, 179, 166',   // --teal-300 (teal tuned for navy backgrounds)
};

export function initNetwork(canvas, motion) {
  if (!canvas?.getContext) return;
  const ctx = canvas.getContext('2d');
  const host = canvas.parentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const small = matchMedia('(max-width: 767px), (pointer: coarse)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');

  let w = 0;
  let h = 0;
  let dpr = 1;
  let nodes = [];
  let raf = 0;
  let last = 0;
  let running = false;
  let inView = true;
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };

  function build() {
    w = host.clientWidth;
    h = host.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    const count = small.matches ? 16 : Math.round(Math.min(48, Math.max(24, (w * h) / 26000)));
    nodes = Array.from({ length: count }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 16, // px per second: slow drift
      vy: (Math.random() - 0.5) * 16,
      z: 0.35 + Math.random() * 0.65, // depth: nearer nodes move more with the pointer
      c: i % 3 === 0 ? COLORS.teal : COLORS.gold,
    }));
  }

  // 0.25 inside an ellipse centred behind the headline, rising to 1 at the edges.
  function quiet(x, y) {
    const dx = (x - w * 0.5) / (w * 0.55);
    const dy = (y - h * 0.66) / (h * 0.45);
    const t = Math.min(1, Math.sqrt(dx * dx + dy * dy) / 1.6);
    return 0.25 + 0.75 * t * t * (3 - 2 * t);
  }

  function draw(dt) {
    const maxD = small.matches ? 120 : 170;
    const margin = 20;
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    const pts = nodes.map((n) => {
      n.x += n.vx * dt;
      n.y += n.vy * dt;
      if (n.x < -margin) n.x = w + margin;
      else if (n.x > w + margin) n.x = -margin;
      if (n.y < -margin) n.y = h + margin;
      else if (n.y > h + margin) n.y = -margin;
      return { x: n.x + pointer.x * 14 * n.z, y: n.y + pointer.y * 10 * n.z, n };
    });

    ctx.lineWidth = 1;
    for (let i = 0; i < pts.length; i++) {
      for (let j = i + 1; j < pts.length; j++) {
        const dx = pts[i].x - pts[j].x;
        const dy = pts[i].y - pts[j].y;
        const d2 = dx * dx + dy * dy;
        if (d2 > maxD * maxD) continue;
        const a = (1 - Math.sqrt(d2) / maxD) * 0.3 * Math.min(pts[i].n.z, pts[j].n.z)
          * quiet((pts[i].x + pts[j].x) / 2, (pts[i].y + pts[j].y) / 2);
        ctx.strokeStyle = `rgba(${pts[i].n.c}, ${a.toFixed(3)})`;
        ctx.beginPath();
        ctx.moveTo(pts[i].x, pts[i].y);
        ctx.lineTo(pts[j].x, pts[j].y);
        ctx.stroke();
      }
    }
    for (const p of pts) {
      ctx.fillStyle = `rgba(${p.n.c}, ${((0.35 + 0.35 * p.n.z) * quiet(p.x, p.y)).toFixed(3)})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1 + 1.2 * p.n.z, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function frame(t) {
    raf = requestAnimationFrame(frame);
    if (small.matches && t - last < 1000 / 30) return; // 30 fps on mobile
    const dt = Math.min((t - last) / 1000, 0.05);
    last = t;
    draw(dt);
  }

  function start() {
    if (running) return;
    running = true;
    last = performance.now();
    raf = requestAnimationFrame(frame);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(raf);
  }
  let loaded = document.readyState === 'complete';
  function sync() {
    if (reduce.matches || motion.paused || !inView || !loaded) stop();
    else start();
  }

  build();
  draw(0);
  canvas.classList.add('is-ready');
  if (!loaded) {
    window.addEventListener('load', () => setTimeout(() => { loaded = true; sync(); }, 600), { once: true });
  }
  sync();

  let resizeQueued = false;
  new ResizeObserver(() => {
    if (resizeQueued) return;
    resizeQueued = true;
    requestAnimationFrame(() => {
      resizeQueued = false;
      if (host.clientWidth === w && host.clientHeight === h) return;
      build();
      draw(0);
    });
  }).observe(host);

  new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    sync();
  }).observe(host);

  motion.onPause(sync);
  reduce.addEventListener('change', sync);

  host.addEventListener('pointermove', (e) => {
    if (!finePointer.matches || small.matches) return;
    const r = host.getBoundingClientRect();
    pointer.tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
    pointer.ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
  });
  host.addEventListener('pointerleave', () => {
    pointer.tx = 0;
    pointer.ty = 0;
  });
}
