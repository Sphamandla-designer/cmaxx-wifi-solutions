#!/usr/bin/env node
/**
 * Builds ONE fully self-contained file: dist/structured-cabling-complete.html
 *
 * Inlines the stylesheet, base64-embeds every photo, and embeds the Outfit
 * webfont so the page has ZERO external requests — it renders identically
 * offline, from a USB stick, or pasted into any CMS.
 *
 *   node tools/build-embedded.mjs
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';

const SRC = 'site/structured-cabling/index.html';
const CSS = 'site/structured-cabling/assets/styles.css';
const IMG = 'site/structured-cabling/assets/img';
const OUT = 'dist/structured-cabling-complete.html';

const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
const FONT_CSS = 'https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap';

/* ---- 1. Fetch the font CSS and embed each face as a data: URI ---------- */

async function buildFontCss() {
  const res = await fetch(FONT_CSS, { headers: { 'User-Agent': UA } });
  if (!res.ok) throw new Error(`font CSS ${res.status}`);
  let css = await res.text();

  // Keep the latin subset only — the page has no latin-ext content, and
  // dropping it roughly halves the embedded font payload.
  const faces = css.split('@font-face').slice(1)
    .map(b => '@font-face' + b.slice(0, b.indexOf('}') + 1))
    .filter(b => /U\+0000-00FF/.test(b));

  let total = 0;
  const out = [];
  for (const face of faces) {
    const url = face.match(/url\((https:\/\/[^)]+)\)/)?.[1];
    if (!url) continue;
    const buf = Buffer.from(await (await fetch(url, { headers: { 'User-Agent': UA } })).arrayBuffer());
    total += buf.length;
    out.push(face
      .replace(/url\(https:\/\/[^)]+\)/, `url(data:font/woff2;base64,${buf.toString('base64')})`)
      .replace(/\s*unicode-range:[^;]+;/, ''));
  }
  console.log(`  fonts: ${out.length} faces embedded, ${(total / 1024).toFixed(0)} KB raw`);
  return out.join('\n');
}

/* ---- 2. Assemble ------------------------------------------------------ */

const fontCss = await buildFontCss();
const css = readFileSync(CSS, 'utf8');
let html = readFileSync(SRC, 'utf8');

// Drop the external font <link>s and preconnects — the faces are embedded now.
html = html
  .replace(/<link rel="preconnect"[^>]*>\s*/g, '')
  .replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>\s*/g, '')
  .replace('<link rel="stylesheet" href="assets/styles.css">',
           `<style>\n${fontCss}\n\n${css.trim()}\n</style>`);

// Base64 every local image.
let imgBytes = 0, imgCount = 0;
html = html.replace(/src="assets\/img\/([^"]+)"/g, (_, file) => {
  const path = `${IMG}/${file}`;
  if (!existsSync(path)) throw new Error(`missing image: ${path}`);
  const buf = readFileSync(path);
  imgBytes += buf.length; imgCount += 1;
  const mime = file.endsWith('.png') ? 'image/png' : file.endsWith('.webp') ? 'image/webp' : 'image/jpeg';
  return `src="data:${mime};base64,${buf.toString('base64')}"`;
});
console.log(`  images: ${imgCount} embedded, ${(imgBytes / 1024).toFixed(0)} KB raw`);

/* ---- 3. Verify nothing external is left ------------------------------- */

const external = [...html.matchAll(/(?:src|href)="(https?:\/\/[^"]+)"/g)]
  .map(m => m[1])
  .filter(u => !/^https:\/\/(wa\.me|www\.cmaxxwifisolutions\.co\.za)/.test(u));
if (external.length) throw new Error(`external assets remain:\n  ${external.join('\n  ')}`);

mkdirSync('dist', { recursive: true });
writeFileSync(OUT, html);
console.log(`${OUT} written (${(html.length / 1024).toFixed(0)} KB, zero external asset requests)`);
