// Procedural wire bundle for the "chaos to clarity" hero, morphed on the GPU.
//
// Each strand exists twice: as a yarn-like loop wound round a sphere (the
// tangled ball) and as one thread of a cable running along the logo path (an
// S-shaped lead-in that coils into a flat spiral). Both tube meshes are built
// once on the CPU; a vertex shader blends between them with uT (0 = ball,
// 1 = spiral). Strands leave one after another and unwind from their far end
// first, so the motion reads as untangling rather than a cross-fade.
// No model files: everything is generated here.
import { BufferAttribute, BufferGeometry, Color, MeshPhysicalMaterial, Sphere, Vector3 } from 'three';

const TAU = Math.PI * 2;

// Deterministic PRNG so the ball looks identical on every visit.
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
const norm = (v) => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const nextTask = () => new Promise((r) => setTimeout(r, 0));

// The clarity path, drawn the way the AccuMinds logo reads: the strand starts
// low on the left, rises through an S-curve, enters the spiral at its top
// heading right, then coils clockwise inwards. Arc-length sampled.
function logoPath(samples, { center = [0.95, 0.15], rOut = 1.25, rIn = 0.14, turns = 3.1 } = {}) {
  const a0 = Math.PI / 2; // top of the spiral; clockwise from here heads right
  const start = [center[0] + rOut * Math.cos(a0), center[1] + rOut * Math.sin(a0)];
  const bez = [[-2.75, -0.7], [-1.35, -1.3], [-0.7, start[1]], start]; // dips, then climbs; ends tangent to the spiral
  const lead = 0.3;
  const raw = (s) => {
    if (s < lead) {
      const u = s / lead, v = 1 - u;
      return [0, 1].map((k) => v * v * v * bez[0][k] + 3 * v * v * u * bez[1][k] + 3 * v * u * u * bez[2][k] + u * u * u * bez[3][k]).concat(0);
    }
    const v = (s - lead) / (1 - lead);
    const a = a0 - TAU * turns * v, r = rOut - (rOut - rIn) * Math.pow(v, 0.9);
    return [center[0] + r * Math.cos(a), center[1] + r * Math.sin(a), 0];
  };
  const dense = 3000, pts = [], len = [0];
  for (let i = 0; i <= dense; i++) pts.push(raw(i / dense));
  for (let i = 1; i <= dense; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const out = [];
  for (let j = 0, k = 0; j < samples; j++) {
    const target = (len[dense] * j) / (samples - 1);
    while (k < dense - 1 && len[k + 1] < target) k++;
    const f = (target - len[k]) / (len[k + 1] - len[k] || 1);
    out.push([0, 1, 2].map((c) => pts[k][c] + (pts[k + 1][c] - pts[k][c]) * f));
  }
  return out;
}

// Writes one tube (K-sided rings along a centreline) into pos/nor at `base`.
// Parallel-transport frames keep the tube from twisting; radius tapers at both ends.
function writeTube(line, radius, K, pos, nor, base, seedNormal) {
  const M = line.length;
  let n = seedNormal;
  for (let j = 0; j < M; j++) {
    const a = line[Math.max(0, j - 1)], b = line[Math.min(M - 1, j + 1)];
    const t = norm([b[0] - a[0], b[1] - a[1], b[2] - a[2]]);
    const d = n[0] * t[0] + n[1] * t[1] + n[2] * t[2];
    n = norm([n[0] - t[0] * d, n[1] - t[1] * d, n[2] - t[2] * d]);
    const bn = cross(t, n);
    const u = j / (M - 1);
    const r = radius * smooth(0, 0.035, u) * smooth(1, 0.965, u);
    for (let k = 0; k < K; k++) {
      const c = Math.cos((TAU * k) / K), s = Math.sin((TAU * k) / K);
      const nx = c * n[0] + s * bn[0], ny = c * n[1] + s * bn[1], nz = c * n[2] + s * bn[2];
      const v = (base + j * K + k) * 3;
      pos[v] = line[j][0] + nx * r; pos[v + 1] = line[j][1] + ny * r; pos[v + 2] = line[j][2] + nz * r;
      nor[v] = nx; nor[v + 1] = ny; nor[v + 2] = nz;
    }
  }
}

// Builds geometry + material. Async: yields between strands so no single task is long.
export async function createWires({ strands = 16, points = 230, radial = 10, radius = 0.028, seed = 7 } = {}) {
  const S = strands, M = points, K = radial;
  const rand = mulberry32(seed);
  const ballR = 1.08, ballC = [-0.35, 0.05, 0];
  const V = S * M * K;
  const posA = new Float32Array(V * 3), norA = new Float32Array(V * 3);
  const posB = new Float32Array(V * 3), norB = new Float32Array(V * 3);
  const info = new Float32Array(V * 3); // delay, u along strand, gold flag
  const path = logoPath(M);
  const cableR = radius * 1.25 * Math.sqrt(S); // neighbouring spiral turns never touch

  for (let s = 0; s < S; s++) {
    // --- ball centreline: 2–3 loops round the sphere about a slowly drifting axis
    const a0 = norm([rand() * 2 - 1, rand() * 2 - 1, rand() * 2 - 1]);
    const a1 = norm(cross(a0, norm([rand() - 0.5, rand() - 0.5, rand() - 0.5]))), a2 = cross(a0, a1);
    const loops = 2 + rand() * 1.2, phase = rand() * TAU;
    const g1 = 0.6 + rand() * 0.9, g2 = 0.5 + rand() * 0.9, q1 = rand() * TAU, q2 = rand() * TAU;
    const drift = 0.55 + rand() * 0.35, wob = 1 + rand() * 2, wobP = rand() * TAU, rScale = 0.86 + rand() * 0.12;
    const up = norm([rand() - 0.5, 1, rand() - 0.5]);
    const ball = [];
    for (let j = 0; j < M; j++) {
      const u = j / (M - 1);
      const axis = norm([0, 1, 2].map((c) => a0[c] + drift * (Math.sin(TAU * g1 * u + q1) * a1[c] + Math.cos(TAU * g2 * u + q2) * a2[c])));
      let e1 = cross(axis, up);
      if (Math.hypot(...e1) < 1e-3) e1 = cross(axis, [1, 0, 0]);
      e1 = norm(e1);
      const e2 = cross(axis, e1), th = TAU * loops * u + phase;
      // ends dive into the ball's interior so the tapered tips hide behind other wires
      const tuck = 0.62 + 0.38 * smooth(0, 0.1, u) * smooth(1, 0.9, u);
      const r = ballR * rScale * tuck * (0.93 + 0.07 * Math.sin(TAU * wob * u + wobP));
      ball.push([0, 1, 2].map((c) => ballC[c] + r * (Math.cos(th) * e1[c] + Math.sin(th) * e2[c])));
    }
    // --- spiral centreline: this strand's place in the cable cross-section (sunflower layout)
    const rr = cableR * Math.sqrt((s + 0.5) / S), ang = s * 2.39996;
    const ox = rr * Math.cos(ang), oz = rr * Math.sin(ang);
    const spiral = path.map((p, j) => {
      const q = path[Math.min(M - 1, j + 1)], o = path[Math.max(0, j - 1)];
      const t = norm([q[0] - o[0], q[1] - o[1], 0]);
      return [p[0] - t[1] * ox, p[1] + t[0] * ox, oz];
    });

    // Seed both tubes' frames with the same normal so their rings line up as well as possible.
    const t0 = norm([ball[1][0] - ball[0][0], ball[1][1] - ball[0][1], ball[1][2] - ball[0][2]]);
    const seedN = Math.abs(t0[2]) < 0.9 ? norm(cross(t0, [0, 0, 1])) : norm(cross(t0, [1, 0, 0]));
    const base = s * M * K;
    writeTube(ball, radius, K, posA, norA, base, seedN);
    writeTube(spiral, radius * 1.25, K, posB, norB, base, seedN);

    const delay = (s / S) * 0.32 + rand() * 0.04, gold = s % 5 === 1 ? 1 : 0;
    for (let j = 0; j < M; j++) {
      for (let k = 0; k < K; k++) {
        const v = (base + j * K + k) * 3;
        info[v] = delay; info[v + 1] = j / (M - 1); info[v + 2] = gold;
      }
    }
    if (s % 3 === 2) await nextTask();
  }

  const idx = new Uint32Array(S * (M - 1) * K * 6);
  for (let s = 0, w = 0; s < S; s++) {
    for (let j = 0; j < M - 1; j++) {
      for (let k = 0; k < K; k++) {
        const a = (s * M + j) * K + k, b = (s * M + j) * K + ((k + 1) % K);
        idx[w++] = a; idx[w++] = a + K; idx[w++] = b;
        idx[w++] = b; idx[w++] = a + K; idx[w++] = b + K;
      }
    }
  }

  const geometry = new BufferGeometry();
  geometry.setIndex(new BufferAttribute(idx, 1));
  geometry.setAttribute('position', new BufferAttribute(posA, 3)); // ball state
  geometry.setAttribute('normal', new BufferAttribute(norA, 3));
  geometry.setAttribute('aSpiral', new BufferAttribute(posB, 3));  // spiral state
  geometry.setAttribute('aSpiralNormal', new BufferAttribute(norB, 3));
  geometry.setAttribute('aInfo', new BufferAttribute(info, 3));
  geometry.boundingSphere = new Sphere(new Vector3(0, 0, 0.3), 4.2); // covers both states + lift

  const uniforms = {
    uT: { value: 0 },
    uSilver: { value: new Color('#d9dde4') },
    uGold: { value: new Color('#e0a83a') },
  };
  const material = new MeshPhysicalMaterial({ metalness: 1, roughness: 0.24, clearcoat: 0.35, clearcoatRoughness: 0.3 });
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, uniforms);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>
        uniform float uT;
        attribute vec3 aSpiral;
        attribute vec3 aSpiralNormal;
        attribute vec3 aInfo;
        varying float vGold;
        float amMix() {
          float l = clamp((uT - aInfo.x - (1.0 - aInfo.y) * 0.26) / 0.38, 0.0, 1.0);
          return l < 0.5 ? 4.0 * l * l * l : 1.0 - pow(-2.0 * l + 2.0, 3.0) / 2.0;
        }`)
      .replace('#include <beginnormal_vertex>', `float amE = amMix();
        vec3 objectNormal = normalize(mix(normal, aSpiralNormal, amE));
        #ifdef USE_TANGENT
          vec3 objectTangent = vec3(tangent.xyz);
        #endif`)
      .replace('#include <begin_vertex>', `vec3 transformed = mix(position, aSpiral, amE);
        transformed.z += sin(3.14159265 * amE) * 0.55; // strands swing towards the viewer mid-flight
        vGold = aInfo.z > 0.5 ? 1.0 : smoothstep(0.15, 0.85, amE);`);
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', `#include <common>
        uniform vec3 uSilver;
        uniform vec3 uGold;
        varying float vGold;`)
      .replace('#include <color_fragment>', `#include <color_fragment>
        diffuseColor.rgb *= mix(uSilver, uGold, vGold);`);
  };

  return { geometry, material, uniforms };
}
