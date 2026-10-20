import { chromium } from 'playwright';
import path from 'node:path';
const dir = path.resolve(process.argv[2]); const out = path.resolve(process.argv[3]);
const browser = await chromium.launch();
for (const name of ['smart-home','managed-wifi']) {
  const page = await browser.newPage({ viewport:{width:1080,height:1350}, deviceScaleFactor:2 });
  await page.goto('file://'+path.join(dir,name+'.html'), { waitUntil:'networkidle' });
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(out,`cmaxx-${name}-post.png`), type:'png' });
  console.log('rendered', name);
}
await browser.close();
