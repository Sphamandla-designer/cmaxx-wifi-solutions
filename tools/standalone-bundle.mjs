#!/usr/bin/env node
/**
 * Round-trips the design-canvas template in and out of the packed
 * "CMAXX Website (standalone).html" bundle.
 *
 *   node tools/standalone-bundle.mjs unpack   standalone -> src/site.dc.html
 *   node tools/standalone-bundle.mjs pack     src/site.dc.html -> standalone
 *
 * Only the <script type="__bundler/template"> payload is touched. The
 * manifest (fonts, runtime JS) and every other bundler block are left byte
 * for byte as they were, so packing an unmodified template is a no-op.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const STANDALONE = 'CMAXX Website (standalone).html';
const TEMPLATE = 'src/site.dc.html';
const BLOCK = /(<script type="__bundler\/template">\n)([\s\S]*?)(\n  <\/script>)/;

// The bundler's JSON writer escapes the slash of a closing tag, which is what
// keeps a literal </script> inside the template from ending the host script
// element. Only that slash is escaped — matching the shipped bundle byte for
// byte, so packing an untouched template leaves the file unchanged.
const encode = (s) => JSON.stringify(s).replaceAll('<\u002F', '<\\u002F');

const read = (p) => readFileSync(p, 'utf8');
const write = (p, s) => { mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, s); };

const shell = read(STANDALONE);
const match = shell.match(BLOCK);
if (!match) throw new Error(`no __bundler/template block found in ${STANDALONE}`);

const command = process.argv[2];

if (command === 'unpack') {
  write(TEMPLATE, JSON.parse(match[2]));
  console.log(`unpacked ${TEMPLATE}`);
} else if (command === 'pack') {
  const encoded = encode(read(TEMPLATE));
  write(STANDALONE, shell.replace(BLOCK, (_, open, __, close) => open + encoded + close));
  console.log(`packed ${TEMPLATE} into ${STANDALONE}`);
} else {
  console.error('usage: node tools/standalone-bundle.mjs <unpack|pack>');
  process.exit(1);
}
