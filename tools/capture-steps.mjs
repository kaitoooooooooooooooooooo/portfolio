// Capture d'écrans qui demandent un clic (écran de détail, panneau de filtres…), en pilotant
// Chrome sans fenêtre par son protocole de débogage. Aucune dépendance (Node 22+).
//   node tools/capture-steps.mjs <url> <nom> "<étapes>"
// Étapes séparées par « ; » : wait:ms · click:x,y (pixels CSS) · shot · reload
//   goto:url (changer de page) · js:fichier.js (script de tools/ exécuté dans la page)
// Exemple : node tools/capture-steps.mjs http://127.0.0.1:5199/ rivano "wait:9000;click:130,560;wait:2500;shot"
// Chaque « shot » écrit previews-src/raw/<nom>-s1.png, -s2.png…
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const [url, name, steps = 'wait:8000;shot'] = process.argv.slice(2);
if (!url || !name) { console.error('usage : node tools/capture-steps.mjs <url> <nom> "<étapes>"'); process.exit(1); }
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const raw = join(root, 'previews-src', 'raw');
mkdirSync(raw, { recursive: true });
const chrome = ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'].find(existsSync);
const port = 9333;
const W = 500, H = 1000, SCALE = 2; // 500 px : largeur minimale d'une fenêtre Chrome

const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${join(root, 'previews-src', 'chrome-cdp')}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
  `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page'); } catch { /* pas encore prêt */ }
}
if (!target) { console.error('Chrome ne répond pas'); proc.kill(); process.exit(1); }

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let seq = 0;
const pending = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((res) => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: SCALE, mobile: true });
await send('Emulation.setTouchEmulationEnabled', { enabled: true });
await send('Page.navigate', { url });

let shots = 0;
for (const step of steps.split(';').map((s) => s.trim()).filter(Boolean)) {
  const cut = step.indexOf(':');
  const op = cut < 0 ? step : step.slice(0, cut), arg = cut < 0 ? '' : step.slice(cut + 1);
  if (op === 'wait') await sleep(Number(arg));
  else if (op === 'reload') await send('Page.reload');
  else if (op === 'goto') await send('Page.navigate', { url: arg });
  else if (op === 'js') {
    const r = await send('Runtime.evaluate', { expression: readFileSync(join(root, 'tools', arg), 'utf8'), awaitPromise: true });
    if (r.result?.exceptionDetails) console.error(`${arg} : ${r.result.exceptionDetails.exception?.description ?? 'erreur'}`);
  }
  else if (op === 'click') {
    const [x, y] = arg.split(',').map(Number);
    for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 });
  } else if (op === 'shot') {
    const r = await send('Page.captureScreenshot', { format: 'png' });
    const out = join(raw, `${name}-s${++shots}.png`);
    writeFileSync(out, Buffer.from(r.result.data, 'base64'));
    console.log(`${name}-s${shots} : ${Math.round(r.result.data.length * 0.75 / 1024)} Ko`);
  }
}
ws.close();
proc.kill();
