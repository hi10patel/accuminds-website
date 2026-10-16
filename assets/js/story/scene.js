// three.js scene for the hero story. Bundled by esbuild into
// assets/js/story.bundle.js (npm run build:3d) and loaded on demand by
// assets/js/motion/story.js, so three.js never blocks the first paint.
import {
  ACESFilmicToneMapping, DirectionalLight, Group, Mesh, PerspectiveCamera,
  PMREMGenerator, Scene, SRGBColorSpace, WebGLRenderer,
} from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { createWires } from './wires.js';

// Camera distance that keeps the whole cable (≈ ±2.45 units wide) in frame.
export function cameraDistance(aspect, fov = 32) {
  return Math.max(9.2, 2.45 / (Math.tan((fov * Math.PI) / 360) * aspect));
}

/**
 * @param {object} o
 * @param {HTMLCanvasElement} o.canvas
 * @param {HTMLElement} o.stage        element whose size the canvas fills
 * @param {{t:number, rise:number}} o.state   scroll state (0..1), owned by story.js
 * @param {() => boolean} o.isPaused   "Pause motion" (stops idle drift)
 * @param {boolean} o.small            lighter mesh + lower pixel ratio
 * @param {boolean} [o.poster]         render one frozen frame (for the poster image)
 */
export async function startScene({ canvas, stage, state, isPaused, small, poster = false }) {
  const { gsap } = window;
  const renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance', preserveDrawingBuffer: poster });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 1.75));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  pmrem.dispose();

  const camera = new PerspectiveCamera(32, 1, 0.1, 100);
  const key = new DirectionalLight('#fff4dc', 2.2);
  key.position.set(3, 4, 6);
  const rim = new DirectionalLight('#9fb8ff', 1.1);
  rim.position.set(-5, -2, -3);
  scene.add(key, rim);

  const wires = await createWires(small
    ? { strands: 11, points: 170, radial: 8, radius: 0.032 }
    : { strands: 16, points: 230, radial: 10, radius: 0.028 });
  const mesh = new Mesh(wires.geometry, wires.material);
  const group = new Group();
  group.add(mesh);
  scene.add(group);

  const resize = () => {
    const w = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.set(0, 0, cameraDistance(camera.aspect));
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(stage);
  resize();

  // Compile shaders before the first visible frame (avoids a hitch on reveal).
  if (renderer.compileAsync) await renderer.compileAsync(scene, camera);

  if (poster) {
    // Same pose as the live scene's first frame (clock = 0, pointer centred).
    wires.uniforms.uT.value = 0;
    group.rotation.set(0.25, 0, 0);
    renderer.render(scene, camera);
    window.__storyPosterReady = true;
    return { renderer };
  }

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  window.addEventListener('pointermove', (e) => {
    pointer.tx = (e.clientX / innerWidth - 0.5) * 2;
    pointer.ty = (e.clientY / innerHeight - 0.5) * 2;
  }, { passive: true });

  let visible = true;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(stage);

  let clock = 0;
  let lastT = -1;
  const tick = (time, delta) => {
    if (!visible || document.hidden) return;
    const paused = isPaused();
    if (!paused) clock += delta / 1000;
    // Nothing moved: skip the frame entirely.
    if (paused && state.t === lastT && Math.abs(pointer.tx - pointer.x) < 1e-3) return;
    lastT = state.t;
    wires.uniforms.uT.value = state.t;
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;
    const calm = 1 - Math.min(1, state.t * 1.4); // the tangle drifts; the spiral settles face-on
    group.rotation.set(
      Math.cos(clock * 0.27) * 0.25 * calm + pointer.y * 0.12,
      Math.sin(clock * 0.35) * 0.55 * calm + pointer.x * 0.22,
      Math.sin(clock * 0.2) * 0.12 * calm,
    );
    // the clean spiral rises and settles above the final headline
    group.position.y = 0.7 * state.rise;
    group.scale.setScalar(1 - 0.14 * state.rise);
    renderer.render(scene, camera);
  };
  gsap.ticker.add(tick);
  renderer.render(scene, camera);
  return { renderer, stop: () => gsap.ticker.remove(tick) };
}
