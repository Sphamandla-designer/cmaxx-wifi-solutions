#!/usr/bin/env node
/**
 * Inlines assets/styles.css into the page and writes a single self-contained
 * file to dist/structured-cabling.html — one file to hand over, paste into an
 * Elementor HTML widget, or open in a browser.
 *
 *   node tools/build-standalone.mjs
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const SRC = 'site/structured-cabling/index.html';
const CSS = 'site/structured-cabling/assets/styles.css';
const OUT = 'dist/structured-cabling.html';

const css = readFileSync(CSS, 'utf8');
const html = readFileSync(SRC, 'utf8');

const linkTag = '<link rel="stylesheet" href="assets/styles.css">';
if (!html.includes(linkTag)) {
  throw new Error(`Expected stylesheet link not found in ${SRC}`);
}

const out = html.replace(linkTag, `<style>\n${css.trim()}\n</style>`);

mkdirSync('dist', { recursive: true });
writeFileSync(OUT, out);
console.log(`${OUT} written (${out.length} bytes, CSS inlined, no external stylesheet)`);
