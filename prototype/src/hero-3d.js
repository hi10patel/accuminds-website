// "Chaos → Clarity" 3D hero prototype.
// Scroll scrubs a tangled wire ball into the AccuMinds gold spiral while giant
// type changes from TANGLED to CLARITY; the wire passes between a filled copy
// of the word (behind the canvas) and an outlined copy (in front).
//
// Bundle: npm run build:3d  (esbuild → prototype/hero-3d.bundle.js)
import {
  ACESFilmicToneMapping, DirectionalLight, Group, Mesh, MeshPhysicalMaterial,
  PerspectiveCamera, PMREMGenerator, Scene, SRGBColorSpace, WebGLRenderer,
} from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { WireBundle } from './wires.js';

const root = document.documentElement;
const stageEl = document.querySelector('.story');
const canvas = document.querySelector('.story-canvas');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const small = matchMedia('(max-width: 767px), (pointer: coarse)').matches;

function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return Boolean(window.WebGL2RenderingContext && c.getContext('webgl2'));
  } catch { return false; }
}

if (reduce || !webglAvailable()) {
  // Static: logo image + final copy, no scroll story.
  root.classList.add('story-static');
} else {
  start();
}

function start() {
  root.classList.add('story-live');
  const { gsap, ScrollTrigger, Lenis } = window;
  gsap.registerPlugin(ScrollTrigger);

  // ---------- three.js scene ----------
  const renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 1.75));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  pmrem.dispose();

  const camera = new PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0, 9.2);

  const key = new DirectionalLight('#fff4dc', 2.2);
  key.position.set(3, 4, 6);
  scene.add(key);
  const rim = new DirectionalLight('#9fb8ff', 1.1);
  rim.position.set(-5, -2, -3);
  scene.add(rim);

  const wires = new WireBundle(small
    ? { strands: 11, points: 170, radial: 8, radius: 0.032 }
    : { strands: 16, points: 230, radial: 10, radius: 0.028 });
  const material = new MeshPhysicalMaterial({
    vertexColors: true, metalness: 1, roughness: 0.24, clearcoat: 0.35, clearcoatRoughness: 0.3,
  });
  const group = new Group();
  group.add(new Mesh(wires.geometry, material));
  scene.add(group);

  // ---------- sizing ----------
  function resize() {
    const w = stageEl.clientWidth, h = stageEl.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // Keep the cable (≈ x −2.45 … 2.45 once the lead-in tip trims) in frame on
    // narrow screens: distance = half-width / tan(horizontal half-FOV).
    const halfFovY = (camera.fov * Math.PI) / 360;
    camera.position.z = Math.max(9.2, 2.45 / (Math.tan(halfFovY) * camera.aspect));
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(stageEl);
  resize();

  // ---------- scroll story ----------
  if (Lenis && !small) {
    const lenis = new Lenis({ lerp: 0.09 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  const state = { t: 0, frame: 0 };
  const story = document.querySelector('.story-track');
  gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: { trigger: story, start: 'top top', end: 'bottom bottom', scrub: 0.9 },
  })
    .to(state, { t: 1, duration: 1 }, 0)
    // word swap: TANGLED drifts apart and fades, CLARITY tightens into place
    .to('.word--tangled', { opacity: 0, letterSpacing: '0.12em', filter: 'blur(10px)', duration: 0.22, ease: 'power1.in' }, 0.18)
    .fromTo('.word--clarity', { opacity: 0, letterSpacing: '0.18em', filter: 'blur(12px)' },
      { opacity: 1, letterSpacing: '-0.04em', filter: 'blur(0px)', duration: 0.3, ease: 'power2.out' }, 0.62)
    // captions
    .fromTo('.cap--1', { opacity: 1, y: 0 }, { opacity: 0, y: -20, duration: 0.12 }, 0.14)
    .fromTo('.cap--2', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.1 }, 0.3)
    .to('.cap--2', { opacity: 0, y: -20, duration: 0.1 }, 0.55)
    .fromTo('.story-final', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.14, ease: 'power2.out' }, 0.84)
    .to('.story-hint', { opacity: 0, duration: 0.05 }, 0.02)
    // the clean spiral rises and settles above the final headline
    .to(group.position, { y: 0.55, duration: 0.3, ease: 'power2.inOut' }, 0.7)
    .to(group.scale, { x: 0.86, y: 0.86, z: 0.86, duration: 0.3, ease: 'power2.inOut' }, 0.7)
    .fromTo('.story-progress span', { scaleX: 0 }, { scaleX: 1, duration: 1 }, 0);

  // Intro on load: ball spins up from nothing, headline rises
  // intro: the tangle grows in (animates the inner mesh so it never fights the scroll tween)
  gsap.from(group.children[0].scale, { x: 0.6, y: 0.6, z: 0.6, duration: 1.6, ease: 'power3.out' });
  gsap.from('.word--tangled .ch', { yPercent: 110, duration: 1, stagger: 0.04, ease: 'power3.out', delay: 0.15 });
  gsap.from('.cap--1, .story-hint', { opacity: 0, y: 16, duration: 0.9, delay: 0.7, ease: 'power2.out' });

  // ---------- pointer ----------
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  window.addEventListener('pointermove', (e) => {
    pointer.tx = (e.clientX / innerWidth - 0.5) * 2;
    pointer.ty = (e.clientY / innerHeight - 0.5) * 2;
  }, { passive: true });

  // ---------- render loop (only while the stage is on screen) ----------
  let visible = true;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(stageEl);
  let clock = 0;
  gsap.ticker.add((time, delta) => {
    if (!visible || document.hidden) return;
    clock += delta / 1000;
    wires.morph(state.t);
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;
    const calm = 1 - Math.min(1, state.t * 1.4); // the tangle moves; the spiral settles face-on
    group.rotation.y = Math.sin(clock * 0.35) * 0.55 * calm + pointer.x * 0.22;
    group.rotation.x = Math.cos(clock * 0.27) * 0.25 * calm + pointer.y * 0.12;
    group.rotation.z = Math.sin(clock * 0.2) * 0.12 * calm;
    renderer.render(scene, camera);
  });
}
