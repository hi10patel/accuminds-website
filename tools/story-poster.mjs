// Captures tools/story-poster.html with headless Chrome (GPU, transparent
// background) and writes the cropped ball to tools/.out/story-poster.png.
// Then: python tools/optimise_images.py  (converts it to assets/img/story-poster.webp)
//   Needs: npm run serve (port 4173) and Google Chrome.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://localhost:4173/tools/story-poster.html';
const OUT = fileURLToPath(new URL('./.out/story-poster.png', import.meta.url));
mkdirSync(fileURLToPath(new URL('./.out/', import.meta.url)), { recursive: true });

// Crop: ball centre (-0.35, 0.05), half-size 1.12 units, camera z 9.2, FOV 32°,
// 1200px stage at device scale 2 → 2400px canvas.
const SCALE = 2;
const unit = (600 / (9.2 * Math.tan((32 * Math.PI) / 360))) * SCALE;
const cx = 600 * SCALE + -0.35 * unit, cy = 600 * SCALE - 0.05 * unit, half = 1.12 * unit;
const clip = { x: (cx - half) / SCALE, y: (cy - half) / SCALE, width: (2 * half) / SCALE, height: (2 * half) / SCALE, scale: 1 };

const port = 9400 + Math.floor(Math.random() * 300);
const proc = spawn(CHROME, ['--headless=new', '--use-angle=d3d11', '--ignore-gpu-blocklist', `--remote-debugging-port=${port}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), 'poster-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let targets;
for (let i = 0; i < 50; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 1200, deviceScaleFactor: SCALE, mobile: false });
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
await send('Page.navigate', { url: URL_ });
for (let i = 0; i < 60; i++) {
  const r = await send('Runtime.evaluate', { expression: 'window.__storyPosterReady === true', returnByValue: true });
  if (r.result.result.value) break;
  await sleep(250);
}
await sleep(300);
const shot = await send('Page.captureScreenshot', { format: 'png', clip });
writeFileSync(OUT, Buffer.from(shot.result.data, 'base64'));
console.log('wrote', OUT, `${Math.round(clip.width * SCALE)}px square`);
ws.close(); proc.kill();
