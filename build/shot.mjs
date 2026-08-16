/**
 * Screenshot helper - renders an HTML file to PNG via CDP.
 * Used to visually verify glyph coverage and print layout.
 *
 *   env -u NODE_OPTIONS node build/shot.mjs <input.html> <output.png> [widthPx]
 */
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const CHROME = ['/usr/local/bin/chrome',
                '/opt/playwright/chromium-1232/chrome-linux64/chrome']
                .find(p => existsSync(p));
const PORT = 9224;
const sleep = ms => new Promise(r => setTimeout(r, ms));

const [input, output, widthArg] = process.argv.slice(2);
if (!input || !output) { console.error('usage: shot.mjs in.html out.png [width]'); process.exit(1); }
const width = Number(widthArg || 900);

const chrome = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu',
  '--disable-dev-shm-usage', '--hide-scrollbars', `--window-size=${width},1400`,
  `--remote-debugging-port=${PORT}`, '--user-data-dir=/tmp/apfc-shot', 'about:blank'],
  { stdio: ['ignore', 'ignore', 'pipe'] });
chrome.stderr.on('data', () => {});

let wsUrl = null;
for (let i = 0; i < 60 && !wsUrl; i++) {
  try { wsUrl = (await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json()).webSocketDebuggerUrl; }
  catch { await sleep(250); }
}
const ws = new WebSocket(wsUrl);
await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });

let id = 0; const pending = new Map(); const waiters = [];
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id);
    m.error ? p.reject(new Error(JSON.stringify(m.error))) : p.resolve(m.result); }
  else if (m.method) {
    for (let i = waiters.length - 1; i >= 0; i--)
      if (waiters[i].method === m.method) { waiters.splice(i, 1)[0].resolve(m.params); }
  }
});
const send = (method, params = {}, sessionId) => {
  const n = ++id; const p = { id: n, method, params }; if (sessionId) p.sessionId = sessionId;
  ws.send(JSON.stringify(p));
  return new Promise((resolve, reject) => pending.set(n, { resolve, reject }));
};
const once = m => new Promise(r => waiters.push({ method: m, resolve: r }));

const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
await send('Page.enable', {}, sessionId);
const loaded = once('Page.loadEventFired');
await send('Page.navigate', { url: 'file://' + resolve(input) }, sessionId);
await loaded;
await sleep(500);

const full = process.argv[5] === 'full';
if (process.argv[6]) {
  await send('Runtime.evaluate',
    { expression: `window.scrollTo(0, ${Number(process.argv[6])})` }, sessionId);
  await sleep(200);
}
const { data } = await send('Page.captureScreenshot',
  { format: 'png', captureBeyondViewport: full }, sessionId);
await mkdir(dirname(resolve(output)), { recursive: true });
await writeFile(resolve(output), Buffer.from(data, 'base64'));
console.log(`wrote ${output} (${(Buffer.from(data, 'base64').length / 1024).toFixed(0)} KB)`);

ws.close(); chrome.kill(); await sleep(150); process.exit(0);
