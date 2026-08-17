/**
 * APFC RT Manual - PDF build.
 *
 * Renders the HTML in docs/ to print-quality PDFs in pdf/ by driving the
 * bundled Chrome over the DevTools Protocol.
 *
 * There is no PDF toolchain in this sandbox (no pandoc, weasyprint, wkhtmltopdf
 * or LaTeX) and PyPI is blocked, so reportlab/weasyprint cannot be installed.
 * But Chrome for Testing is present, and Node 22 ships a WebSocket client, so
 * CDP Page.printToPDF gives us real PDFs with the actual stylesheet applied -
 * and, unlike `chrome --print-to-pdf`, proper "Page X of Y" numbering.
 *
 * No npm dependencies.
 *
 * Usage:
 *   node build/pdf.mjs                       # every file in docs/
 *   node build/pdf.mjs docs/index.html       # one file
 */

import { spawn } from 'node:child_process';
import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = join(ROOT, 'docs');
const OUT = join(ROOT, 'pdf');
const PORT = 9223;

const CHROME = ['/usr/local/bin/chrome',
                '/opt/playwright/chromium-1232/chrome-linux64/chrome']
                .find(p => existsSync(p));

// ---------------------------------------------------------------- helpers

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function findHtml(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...await findHtml(p));
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out.sort();
}

/** Pull the document title and version out of the built HTML. */
async function meta(file) {
  const html = await readFile(file, 'utf8');
  const strip = s => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const t = html.match(/<title>([\s\S]*?)<\/title>/i);
  const run = html.match(/<div class="running">([\s\S]*?)<\/div>/i);
  const ver = html.match(/<span class="ver">([\s\S]*?)<\/span>/i);
  const version = ver ? strip(ver[1]) : '';
  let running = run ? strip(run[1]) : (t ? strip(t[1]) : '');
  // the in-page running div ends with the version; the header shows it
  // separately on the right, so drop the duplicate here
  if (version && running.endsWith(version)) {
    running = running.slice(0, -version.length).trim();
  }
  return { title: t ? strip(t[1]) : '', running, version };
}

// ---------------------------------------------------------------- CDP

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.waiters = [];
    ws.addEventListener('message', ev => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve: res, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(JSON.stringify(msg.error))) : res(msg.result);
      } else if (msg.method) {
        this.waiters = this.waiters.filter(w => {
          if (w.method === msg.method && (!w.sessionId || w.sessionId === msg.sessionId)) {
            w.resolve(msg.params);
            return false;
          }
          return true;
        });
      }
    });
  }

  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }

  once(method, sessionId, timeout = 30000) {
    return new Promise((resolve, reject) => {
      const w = { method, sessionId, resolve };
      this.waiters.push(w);
      setTimeout(() => {
        this.waiters = this.waiters.filter(x => x !== w);
        reject(new Error(`timeout waiting for ${method}`));
      }, timeout);
    });
  }
}

const HEADER = m => `
<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7pt;
  color:#5c6673;padding:0 14mm;display:flex;justify-content:space-between;
  border-bottom:.5px solid #d7dce4;padding-bottom:2mm;-webkit-print-color-adjust:exact;">
  <span>${m.running}</span><span style="color:#1e3a5f;font-weight:700;">${m.version}</span>
</div>`;

const FOOTER = `
<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7pt;
  color:#5c6673;padding:0 14mm;display:flex;justify-content:space-between;
  border-top:.5px solid #d7dce4;padding-top:1.5mm;-webkit-print-color-adjust:exact;">
  <span>UPSC EPFO APFC &mdash; Recruitment Test Manual</span>
  <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
</div>`;

// ---------------------------------------------------------------- main

async function main() {
  if (!CHROME) {
    console.error('no Chrome binary found');
    process.exit(1);
  }
  if (typeof WebSocket === 'undefined') {
    console.error('this Node build has no global WebSocket; need Node >= 21');
    process.exit(1);
  }

  const args = process.argv.slice(2);
  const targets = args.length
    ? args.map(a => resolve(a))
    : await findHtml(DOCS);

  if (!targets.length) { console.log('nothing to render'); return; }

  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    '--hide-scrollbars', '--force-color-profile=srgb',
    `--remote-debugging-port=${PORT}`, '--user-data-dir=/tmp/apfc-cdp',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  chrome.stderr.on('data', () => {});

  // wait for the debugging endpoint
  let wsUrl = null;
  for (let i = 0; i < 60 && !wsUrl; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      wsUrl = (await r.json()).webSocketDebuggerUrl;
    } catch { await sleep(250); }
  }
  if (!wsUrl) { chrome.kill(); throw new Error('Chrome DevTools endpoint never came up'); }

  const ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });
  const cdp = new CDP(ws);

  let failures = 0;
  for (const file of targets) {
    const rel = relative(DOCS, file);
    const dest = join(OUT, rel.replace(/\.html$/, '.pdf'));
    await mkdir(dirname(dest), { recursive: true });
    const m = await meta(file);

    try {
      const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
      const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });

      await cdp.send('Page.enable', {}, sessionId);
      const loaded = cdp.once('Page.loadEventFired', sessionId);
      await cdp.send('Page.navigate', { url: 'file://' + file }, sessionId);
      await loaded;
      await sleep(400);   // let fonts settle before measuring page breaks

      const { data } = await cdp.send('Page.printToPDF', {
        printBackground: true,
        paperWidth: 8.27, paperHeight: 11.69,          // A4
        marginTop: 0.62, marginBottom: 0.58,
        marginLeft: 0.5, marginRight: 0.5,
        displayHeaderFooter: true,
        headerTemplate: HEADER(m),
        footerTemplate: FOOTER,
        preferCSSPageSize: false,
        transferMode: 'ReturnAsBase64',
      }, sessionId);

      await writeFile(dest, Buffer.from(data, 'base64'));
      await cdp.send('Target.closeTarget', { targetId });

      const kb = (Buffer.from(data, 'base64').length / 1024).toFixed(0);
      console.log(`rendered ${relative(ROOT, dest)}  (${kb} KB)`);
    } catch (err) {
      failures++;
      console.error(`FAILED ${rel}: ${err.message}`);
    }
  }

  ws.close();
  chrome.kill();
  await sleep(200);
  process.exit(failures ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(1); });
