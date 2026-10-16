// logo-animation.jsx — Accuminds logo reveal animation
// Uses the actual logo PNG (untouched), unveiled via an animated CSS clip-path:
//   • Ball materializes through a vibrating/shaking entry (chaos → settled)
//   • A left-to-right sweep reveals the gold strand and coils outward to spiral
// Architecture: HTML <img> inside a clipped wrapper. SVG <image> doesn't render
// reliably in sandboxed previews, so we use CSS clip-path: path(...) for the
// reveal — equivalent visual result, works everywhere.

const { useTime, Easing, clamp } = window;

const LOGO_SRC = "assets/logo-mark-3d-transparent.png";

function LogoAnimation() {
  const t = useTime();

  // Timestamp label for review comments
  React.useEffect(() => {
    const root = document.querySelector('[data-screen-label]');
    if (root) root.setAttribute('data-screen-label', `t=${t.toFixed(1)}s`);
  }, [Math.floor(t * 2)]);

  // ── Image layout on the 1280×720 stage ────────────────────────────────
  // Native PNG is 1380×560 → display at 1200×487, centered (40 px gutter).
  const IMG = { w: 1200, h: 487, x: 40, y: 116 };

  // ── Anatomy of the logo in IMG-LOCAL coords (origin = img top-left) ───
  const BALL = { cx: 255, cy: 280, rMax: 225 };
  const SWEEP_START_X = 295;   // x where the strand-and-spiral sweep begins

  // ── Phase timing (loop = 9s) ─────────────────────────────────────────
  const ballGrowEnd  = 0.7;
  const jitterPeak   = 0.9;
  const jitterEnd    = 2.0;
  const sweepStart   = 2.5;
  const sweepEnd     = 5.8;

  // Ball reveal disc
  const ballR = BALL.rMax * Easing.easeOutCubic(clamp(t / ballGrowEnd, 0, 1));

  // Jitter amplitude — gentle shake while chaos, decays to 0 by jitterEnd
  let jAmp = 0;
  if (t < jitterPeak)      jAmp = 7;
  else if (t < jitterEnd)  jAmp = 7 * (1 - Easing.easeInOutCubic((t - jitterPeak) / (jitterEnd - jitterPeak)));

  // Multi-harmonic pseudo-noise for natural chaotic shake (slower frequencies = calmer)
  const jx = jAmp * (Math.sin(t * 31) * 0.55 + Math.sin(t * 53) * 0.45);
  const jy = jAmp * (Math.cos(t * 27) * 0.55 + Math.cos(t * 47) * 0.45);

  // Strand + spiral sweep — paints the right side of the logo into view
  const sweepRaw = clamp((t - sweepStart) / (sweepEnd - sweepStart), 0, 1);
  const sweepEased = Easing.easeInOutCubic(sweepRaw);
  const sweepX = SWEEP_START_X + (IMG.w - SWEEP_START_X) * sweepEased;

  // Build a union clip-path: ball circle ∪ growing sweep rectangle.
  // BOTH subpaths must wind in the same direction (CW here) so the nonzero
  // fill-rule treats their overlap as filled — otherwise opposite windings
  // cancel out and a gap appears between the ball and the strand.
  const ballPath =
    `M ${(BALL.cx - ballR).toFixed(2)},${BALL.cy} ` +
    `a ${ballR},${ballR} 0 1,1 ${(2 * ballR).toFixed(2)},0 ` +
    `a ${ballR},${ballR} 0 1,1 ${(-2 * ballR).toFixed(2)},0 Z`;
  const sweepPath = sweepEased > 0
    ? `M ${SWEEP_START_X},0 L ${sweepX.toFixed(2)},0 L ${sweepX.toFixed(2)},${IMG.h} L ${SWEEP_START_X},${IMG.h} Z`
    : '';
  const clipPath = `path('${ballPath}${sweepPath ? ' ' + sweepPath : ''}')`;

  // Ghost copies opacity (subtle motion-blur during chaos)
  const ghostOp = clamp((jitterEnd - t) / 1.3, 0, 1) * 0.28;

  // Subtle camera drift / breathing zoom — keeps frame alive
  const camScale = 1 + 0.018 * Math.sin(t * 0.42);
  const camTx = Math.sin(t * 0.27) * 6;
  const camTy = Math.cos(t * 0.21) * 4;

  // Shared <img> style — different transforms per copy
  const imgBase = {
    position: 'absolute', left: 0, top: 0,
    width: IMG.w, height: IMG.h, display: 'block',
    willChange: 'transform, opacity',
    pointerEvents: 'none',
    userSelect: 'none',
  };

  return (
    <div style={{
      position: 'absolute', inset: 0,
      transformOrigin: '50% 50%',
      transform: `scale(${camScale}) translate(${camTx}px, ${camTy}px)`,
    }}>
      <div style={{
        position: 'absolute',
        left: IMG.x, top: IMG.y,
        width: IMG.w, height: IMG.h,
        clipPath: clipPath,
        WebkitClipPath: clipPath,
      }}>
        {/* Ghost copies during chaos — multiple offset shadows of the same logo */}
        {ghostOp > 0.02 && (
          <React.Fragment>
            <img src={LOGO_SRC} draggable={false} style={{
              ...imgBase,
              transform: `translate(${(jx * 1.55 + 7).toFixed(2)}px, ${(jy * 1.55 - 5).toFixed(2)}px)`,
              opacity: ghostOp * 0.55,
            }} />
            <img src={LOGO_SRC} draggable={false} style={{
              ...imgBase,
              transform: `translate(${(-jx * 1.25 - 6).toFixed(2)}px, ${(-jy * 1.25 + 7).toFixed(2)}px)`,
              opacity: ghostOp * 0.45,
            }} />
            <img src={LOGO_SRC} draggable={false} style={{
              ...imgBase,
              transform: `translate(${(jx * 0.8 + 11).toFixed(2)}px, ${(jy * 0.8 + 9).toFixed(2)}px)`,
              opacity: ghostOp * 0.35,
            }} />
          </React.Fragment>
        )}

        {/* Main logo — jittered during chaos, settles afterwards */}
        <img src={LOGO_SRC} draggable={false} style={{
          ...imgBase,
          transform: `translate(${jx.toFixed(2)}px, ${jy.toFixed(2)}px)`,
        }} />
      </div>
    </div>
  );
}

window.LogoAnimation = LogoAnimation;
