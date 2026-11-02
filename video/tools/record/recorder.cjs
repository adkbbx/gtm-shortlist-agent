// Crisp screen recording of the live demo: CDP screencast frames (JPEG q92) at 1920x1080 device pixels, a visible
// cursor drawn from real mouse events, and a marks file with the time of each action. Assemble with ffmpeg afterwards.
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PW_ROOT + '/node_modules/playwright');

const BASE = 'https://gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run';

const CURSOR = `
(() => {
  if (window.__cursorInstalled) return; window.__cursorInstalled = true;
  const add = () => {
    const c = document.createElement('div');
    c.id = '__rec_cursor';
    c.innerHTML = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M4 2.5l15.5 9.2-6.6 1.5 3.9 7.3-3 1.6-3.9-7.4-5 4.6z" fill="#1b1b1b" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    Object.assign(c.style, {position:'fixed', left:'-60px', top:'-60px', zIndex:2147483647, pointerEvents:'none',
      transition:'transform 120ms ease-out', transformOrigin:'4px 3px', filter:'drop-shadow(0 2px 3px rgba(0,0,0,.25))'});
    document.documentElement.appendChild(c);
    addEventListener('mousemove', e => { c.style.left = e.clientX - 4 + 'px'; c.style.top = e.clientY - 3 + 'px'; }, true);
    addEventListener('mousedown', () => { c.style.transform = 'scale(.82)'; }, true);
    addEventListener('mouseup', () => { c.style.transform = 'scale(1)'; }, true);
  };
  if (document.documentElement) add(); else addEventListener('DOMContentLoaded', add);
})();`;

async function start(name, outDir) {
  const dir = path.join(outDir, name);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(path.join(dir, 'frames'), { recursive: true });
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 4 / 3,
    locale: 'en-US', timezoneId: 'America/New_York', colorScheme: 'light' });
  await context.addInitScript(CURSOR);
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  const frames = [];
  const marks = [];
  let t0 = null;
  cdp.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
    const ts = metadata.timestamp;
    if (t0 === null) t0 = ts;
    const file = `f${String(frames.length).padStart(6, '0')}.jpg`;
    fs.writeFileSync(path.join(dir, 'frames', file), Buffer.from(data, 'base64'));
    frames.push({ file, t: ts - t0 });
    cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {});
  });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });
  const rec = {
    page, dir,
    // CDP frame timestamps are epoch seconds, so marks share the frames' clock.
    now: () => (t0 === null ? 0 : Date.now() / 1000 - t0),
    mark(label) { marks.push({ label, t: rec.now() }); console.log(`[${name}] ${rec.now().toFixed(2)}s ${label}`); },
    wait: ms => page.waitForTimeout(ms),
    async moveTo(locator, { steps = 28, dx = 0.5, dy = 0.5 } = {}) {
      const box = await locator.boundingBox();
      await page.mouse.move(box.x + box.width * dx, box.y + box.height * dy, { steps });
    },
    async click(locator, opts) { await rec.moveTo(locator, opts); await rec.wait(180); await page.mouse.down(); await rec.wait(90); await page.mouse.up(); },
    async scrollBy(dy, { steps = 24, pause = 22 } = {}) {
      for (let i = 0; i < steps; i++) { await page.mouse.wheel(0, dy / steps); await rec.wait(pause); }
    },
    async scrollToShow(locator, top = 120) {
      const box = await locator.boundingBox();
      await rec.scrollBy(box.y - top);
      await rec.wait(500);
    },
    async stop() {
      await rec.wait(400);
      await cdp.send('Page.stopScreencast').catch(() => {});
      await browser.close();
      // Concat list: each frame lasts until the next one arrives.
      const lines = [];
      frames.forEach((f, i) => {
        const next = frames[i + 1] ? frames[i + 1].t : f.t + 0.5;
        lines.push(`file 'frames/${f.file}'`, `duration ${Math.max(next - f.t, 0.001).toFixed(4)}`);
      });
      lines.push(`file 'frames/${frames[frames.length - 1].file}'`);
      fs.writeFileSync(path.join(dir, 'list.txt'), lines.join('\n'));
      fs.writeFileSync(path.join(dir, 'marks.json'), JSON.stringify({ marks, frames: frames.length, seconds: frames.at(-1).t }, null, 1));
      console.log(`[${name}] ${frames.length} frames, ${frames.at(-1).t.toFixed(1)}s`);
    },
  };
  return rec;
}

module.exports = { start, BASE };
