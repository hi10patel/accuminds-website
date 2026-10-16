// Procedural wire bundle: a tangled ball of metal strands that unravels into
// the AccuMinds gold spiral. No model files: every strand is generated here.
//
//   ball state     each strand is a yarn-like loop wound around a sphere
//   spiral state   all strands run side by side as one cable along the logo
//                  path: an S-shaped lead-in that coils into a flat spiral
//   morph(t)       t = 0 ball … 1 spiral. Strands leave the ball one after
//                  another, and each one unwinds from its far end first, so
//                  the motion reads as untangling rather than a cross-fade.
import { BufferAttribute, BufferGeometry, Color } from 'three';

const TAU = Math.PI * 2;

// Small deterministic PRNG so the ball looks the same on every visit.
function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const smooth = (a, b, x) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
const easeInOutCubic = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

function normalize(v) {
  const l = Math.hypot(v[0], v[1], v[2]) || 1;
  return [v[0] / l, v[1] / l, v[2] / l];
}
function cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}

// ---------- The clarity path (lead-in S-curve + inward spiral), arc-length sampled ----------
function logoPath(samples, { center = [0.95, 0.15], rOut = 1.25, rIn = 0.14, turns = 3.1 } = {}) {
  const a0 = -Math.PI / 2; // spiral starts at its lowest point, heading right
  const start = [center[0] + rOut * Math.cos(a0), center[1] + rOut * Math.sin(a0)];
  const bez = [[-2.75, 0.35], [-1.55, 1.05], [-0.55, start[1]], start]; // ends tangent to the spiral
  const leadShare = 0.3;
  const raw = (s) => {
    if (s < leadShare) {
      const u = s / leadShare, v = 1 - u;
      const p = [0, 1].map((k) => v * v * v * bez[0][k] + 3 * v * v * u * bez[1][k] + 3 * v * u * u * bez[2][k] + u * u * u * bez[3][k]);
      return [p[0], p[1], 0];
    }
    const v = (s - leadShare) / (1 - leadShare);
    const a = a0 + TAU * turns * v;
    const r = rOut - (rOut - rIn) * Math.pow(v, 0.9);
    return [center[0] + r * Math.cos(a), center[1] + r * Math.sin(a), 0];
  };
  // Re-sample by arc length so strand points are evenly spaced along the cable.
  const dense = 4000;
  const pts = [], len = [0];
  for (let i = 0; i <= dense; i++) pts.push(raw(i / dense));
  for (let i = 1; i <= dense; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const total = len[dense];
  const out = [];
  let k = 0;
  for (let j = 0; j < samples; j++) {
    const target = (total * j) / (samples - 1);
    while (k < dense - 1 && len[k + 1] < target) k++;
    const f = (target - len[k]) / (len[k + 1] - len[k] || 1);
    out.push([0, 1, 2].map((c) => pts[k][c] + (pts[k + 1][c] - pts[k][c]) * f));
  }
  return out;
}

export class WireBundle {
  constructor({ strands = 16, points = 220, radial = 10, radius = 0.028, ballRadius = 1.08, ballCenter = [-0.35, 0.05, 0], seed = 7 } = {}) {
    Object.assign(this, { strands, points, radial, radius });
    const rand = mulberry32(seed);
    const S = strands, M = points, K = radial;

    this.ball = new Float32Array(S * M * 3);
    this.spiral = new Float32Array(S * M * 3);
    this.delay = new Float32Array(S);
    this.gold = new Uint8Array(S);
    this.cur = new Float32Array(S * M * 3);
    this.mix = new Float32Array(S * M); // 0 = ball, 1 = spiral (per point)

    // --- Ball: each strand winds 2–3 times round the sphere about a slowly drifting axis
    for (let s = 0; s < S; s++) {
      const a0 = normalize([rand() * 2 - 1, rand() * 2 - 1, rand() * 2 - 1]);
      const ref = normalize(cross(a0, normalize([rand() - 0.5, rand() - 0.5, rand() - 0.5])));
      const a1 = ref, a2 = cross(a0, a1);
      const loops = 2 + rand() * 1.2, phase = rand() * TAU;
      const g1 = 0.6 + rand() * 0.9, g2 = 0.5 + rand() * 0.9, q1 = rand() * TAU, q2 = rand() * TAU;
      const drift = 0.55 + rand() * 0.35;
      const wob = 1 + rand() * 2, wobP = rand() * TAU, rScale = 0.86 + rand() * 0.12;
      const up = normalize([rand() - 0.5, 1, rand() - 0.5]);
      for (let j = 0; j < M; j++) {
        const u = j / (M - 1);
        const axis = normalize([0, 1, 2].map((c) => a0[c] + drift * (Math.sin(TAU * g1 * u + q1) * a1[c] + Math.cos(TAU * g2 * u + q2) * a2[c])));
        let e1 = cross(axis, up);
        if (Math.hypot(...e1) < 1e-3) e1 = cross(axis, [1, 0, 0]);
        e1 = normalize(e1);
        const e2 = cross(axis, e1);
        const th = TAU * loops * u + phase;
        const r = ballRadius * rScale * (0.93 + 0.07 * Math.sin(TAU * wob * u + wobP));
        const i = (s * M + j) * 3;
        for (let c = 0; c < 3; c++) this.ball[i + c] = ballCenter[c] + r * (Math.cos(th) * e1[c] + Math.sin(th) * e2[c]);
      }
      this.delay[s] = (s / S) * 0.32 + rand() * 0.04;
      this.gold[s] = s % 5 === 1 ? 1 : 0; // a few gold threads run through the ball, as in the logo
    }

    // --- Spiral: strands packed into one cable (sunflower layout in the cable's cross-section)
    const path = logoPath(M);
    // Tight enough that neighbouring spiral turns never touch (turn gap ≈ 0.36).
    const cableR = radius * 1.25 * Math.sqrt(S);
    for (let s = 0; s < S; s++) {
      const rr = cableR * Math.sqrt((s + 0.5) / S), ang = s * 2.39996;
      const ox = rr * Math.cos(ang), oz = rr * Math.sin(ang);
      for (let j = 0; j < M; j++) {
        const p = path[j], q = path[Math.min(M - 1, j + 1)], o = path[Math.max(0, j - 1)];
        const t = normalize([q[0] - o[0], q[1] - o[1], 0]);
        const n = [-t[1], t[0], 0];
        const i = (s * M + j) * 3;
        this.spiral[i] = p[0] + n[0] * ox;
        this.spiral[i + 1] = p[1] + n[1] * ox;
        this.spiral[i + 2] = oz;
      }
    }

    // --- Mesh buffers: K-sided tube per strand, tapered to points at both ends (no caps)
    const V = S * M * K;
    this.geometry = new BufferGeometry();
    this.pos = new Float32Array(V * 3);
    this.nor = new Float32Array(V * 3);
    this.col = new Float32Array(V * 3);
    const idx = new Uint32Array(S * (M - 1) * K * 6);
    let w = 0;
    for (let s = 0; s < S; s++) {
      for (let j = 0; j < M - 1; j++) {
        for (let k = 0; k < K; k++) {
          const a = (s * M + j) * K + k, b = (s * M + j) * K + ((k + 1) % K);
          const c = a + K, d = b + K;
          idx[w++] = a; idx[w++] = c; idx[w++] = b;
          idx[w++] = b; idx[w++] = c; idx[w++] = d;
        }
      }
    }
    this.geometry.setIndex(new BufferAttribute(idx, 1));
    this.geometry.setAttribute('position', new BufferAttribute(this.pos, 3));
    this.geometry.setAttribute('normal', new BufferAttribute(this.nor, 3));
    this.geometry.setAttribute('color', new BufferAttribute(this.col, 3));
    this.silver = new Color('#d9dde4');
    this.goldColor = new Color('#e0a83a');
    this.ring = Array.from({ length: K }, (_, k) => [Math.cos((TAU * k) / K), Math.sin((TAU * k) / K)]);
    this.lastT = -1;
    this.morph(0);
  }

  morph(t) {
    if (Math.abs(t - this.lastT) < 1e-4) return false;
    this.lastT = t;
    const { strands: S, points: M, radial: K, ball, spiral, cur, mix, delay } = this;
    for (let s = 0; s < S; s++) {
      for (let j = 0; j < M; j++) {
        const u = j / (M - 1);
        // far end leaves first; every point has arrived by t = 1
        const local = Math.min(1, Math.max(0, (t - delay[s] - (1 - u) * 0.26) / 0.38));
        const e = easeInOutCubic(local);
        const i = (s * M + j) * 3;
        const lift = Math.sin(Math.PI * e) * 0.55; // strands swing towards the viewer mid-flight
        cur[i] = ball[i] + (spiral[i] - ball[i]) * e;
        cur[i + 1] = ball[i + 1] + (spiral[i + 1] - ball[i + 1]) * e;
        cur[i + 2] = ball[i + 2] + (spiral[i + 2] - ball[i + 2]) * e + lift;
        mix[s * M + j] = e;
      }
    }
    this.#buildTubes();
    return true;
  }

  #buildTubes() {
    const { strands: S, points: M, radial: K, cur, mix, pos, nor, col, ring, radius, gold, silver, goldColor } = this;
    let n = [0, 0, 1];
    for (let s = 0; s < S; s++) {
      for (let j = 0; j < M; j++) {
        const i = (s * M + j) * 3;
        const ia = (s * M + Math.max(0, j - 1)) * 3, ib = (s * M + Math.min(M - 1, j + 1)) * 3;
        const t = normalize([cur[ib] - cur[ia], cur[ib + 1] - cur[ia + 1], cur[ib + 2] - cur[ia + 2]]);
        // parallel transport keeps the tube from twisting
        if (j === 0) {
          n = Math.abs(t[2]) < 0.9 ? normalize(cross(t, [0, 0, 1])) : normalize(cross(t, [1, 0, 0]));
        } else {
          const d = n[0] * t[0] + n[1] * t[1] + n[2] * t[2];
          n = normalize([n[0] - t[0] * d, n[1] - t[1] * d, n[2] - t[2] * d]);
        }
        const b = cross(t, n);
        const u = j / (M - 1);
        const m = mix[s * M + j];
        const r = radius * smooth(0, 0.035, u) * smooth(1, 0.965, u) * (1 + 0.25 * m);
        const g = gold[s] ? 1 : smooth(0.15, 0.85, m);
        const cr = silver.r + (goldColor.r - silver.r) * g;
        const cg = silver.g + (goldColor.g - silver.g) * g;
        const cb = silver.b + (goldColor.b - silver.b) * g;
        for (let k = 0; k < K; k++) {
          const [cx, sy] = ring[k];
          const nx = cx * n[0] + sy * b[0], ny = cx * n[1] + sy * b[1], nz = cx * n[2] + sy * b[2];
          const v = ((s * M + j) * K + k) * 3;
          pos[v] = cur[i] + nx * r; pos[v + 1] = cur[i + 1] + ny * r; pos[v + 2] = cur[i + 2] + nz * r;
          nor[v] = nx; nor[v + 1] = ny; nor[v + 2] = nz;
          col[v] = cr; col[v + 1] = cg; col[v + 2] = cb;
        }
      }
    }
    const g = this.geometry;
    g.attributes.position.needsUpdate = true;
    g.attributes.normal.needsUpdate = true;
    g.attributes.color.needsUpdate = true;
    g.computeBoundingSphere();
  }
}
