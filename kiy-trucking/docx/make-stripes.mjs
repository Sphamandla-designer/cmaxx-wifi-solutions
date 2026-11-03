// Renders the red speed-stripe artwork used in the Word letterhead as transparent PNGs.
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import path from 'node:path';

const { chromium } = createRequire(import.meta.url)('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));

// 210mm wide at 300dpi = 2480px; stripe band heights in px at 300dpi
const W = 2480;
const html = (h, body) => `<!doctype html><html><body style="margin:0;background:transparent">
<div style="position:relative;width:${W}px;height:${h}px;overflow:hidden">${body}</div></body></html>`;

const headerStripe = html(130, `
  <div style="position:absolute;inset:0;background:#000;clip-path:polygon(0 0,100% 0,100% 0,0 40%)"></div>
  <div style="position:absolute;inset:0;background:#b5010d;clip-path:polygon(0 52%,100% 0,100% 22%,0 82%)"></div>
  <div style="position:absolute;inset:0;background:#e3121f;clip-path:polygon(0 92%,62% 44%,62% 54%,0 100%)"></div>`);

const footerStripe = html(130, `
  <div style="position:absolute;inset:0;background:#b5010d;clip-path:polygon(0 42%,100% 0,100% 30%,0 78%)"></div>
  <div style="position:absolute;inset:0;background:#000;clip-path:polygon(0 84%,100% 40%,100% 100%,0 100%)"></div>`);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: 130 }, deviceScaleFactor: 1 });
for (const [name, src] of [['header-stripe.png', headerStripe], ['footer-stripe.png', footerStripe]]) {
  await page.setContent(src);
  await page.screenshot({ path: path.join(dir, name), omitBackground: true, clip: { x: 0, y: 0, width: W, height: 130 } });
}
await browser.close();
console.log('stripes rendered');
