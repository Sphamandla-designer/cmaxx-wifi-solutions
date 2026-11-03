// Renders letterhead.html to PDF (A4) and PNG previews. Run: node render.mjs
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import path from 'node:path';

const { chromium } = createRequire(import.meta.url)('playwright');

const dir = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
await page.goto('file://' + path.join(dir, 'letterhead.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.emulateMedia({ media: 'print' });
await page.pdf({
  path: path.join(dir, 'KIY-Trucking-Letterhead.pdf'),
  format: 'A4',
  printBackground: true,
  preferCSSPageSize: true,
});
const pages = await page.$$('.page');
await pages[0].screenshot({ path: path.join(dir, 'letterhead-page1.png') });
await pages[1].screenshot({ path: path.join(dir, 'letterhead-page2.png') });
await browser.close();
console.log('rendered PDF + PNG previews');
