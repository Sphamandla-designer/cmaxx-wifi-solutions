#!/usr/bin/env node
/**
 * Export one page from the design canvas as a standalone HTML file.
 *
 *   node tools/export-page.mjs /cloud-microsoft-365/teams-sharepoint/
 *   node tools/export-page.mjs <slug> [outFile]
 *
 * The canvas keeps every page as a <section data-page> inside one document and
 * uses a small DSL the canvas runtime understands. This converts that DSL to
 * plain HTML and inlines the design system and its fonts, so the result opens
 * anywhere with no network access and no runtime:
 *
 *   sc-raw-<tag>      -> <tag>            (tables)
 *   sc-camel-view-box -> viewBox          (SVG)
 *   style-hover="..." -> a class plus a real :hover rule
 *   <sc-if>           -> unwrapped        (the sticky CTA always renders)
 *   <image-slot>      -> a dashed placeholder carrying its prompt text
 *
 * Titles and meta descriptions come from src/*-seo.md; pass them here as the
 * page's own <title>/<meta> since the canvas can only carry one of each.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, basename } from 'node:path';
import { gunzipSync } from 'node:zlib';

const TEMPLATE = 'src/site.dc.html';
const BUNDLE = 'CMAXX Website (standalone).html';

// Per-page metadata, mirroring the cluster SEO specs in src/.
const META = {
  '/cloud-microsoft-365/microsoft-365-setup-migration/': ['Microsoft 365 Setup & Migration Gauteng | CMAXX', 'Plan and migrate business email, users, files and Microsoft 365 services with structured support from CMAXX across Gauteng.'],
  '/cloud-microsoft-365/microsoft-365-support/': ['Microsoft 365 Support Gauteng | CMAXX', 'Ongoing Microsoft 365 administration for users, licences, email, MFA, Teams, SharePoint and business support across Gauteng.'],
  '/cloud-microsoft-365/teams-sharepoint/': ['Microsoft Teams & SharePoint Services Gauteng | CMAXX', 'Teams and SharePoint setup, permissions, document libraries and collaboration support for Gauteng businesses.'],
  '/cloud-microsoft-365/business-email-exchange-online/': ['Business Email & Exchange Online Gauteng | CMAXX', 'Professional company email, Exchange Online setup, mailbox migration, shared mailboxes and Outlook support for Gauteng businesses.'],
  '/cloud-microsoft-365/business-backup-nas/': ['Business Backup & NAS Storage Gauteng | CMAXX', 'NAS storage, local backup, off-site copies, monitoring and recovery solutions for Gauteng businesses.'],
  '/residential-cctv-installation/': ['Residential CCTV Installation Gauteng | CMAXX', 'Professional residential CCTV installation for homes, estates and smallholdings across Gauteng.'],
  '/commercial-cctv-solutions/': ['Commercial CCTV Installation Gauteng | CMAXX', 'Commercial CCTV systems for offices, retail, warehouses, hospitality, schools and multi-site operations across Gauteng.'],
  '/wireless-cctv-smart-cameras/': ['Wireless CCTV & Smart Camera Installation Gauteng | CMAXX', 'Professional Wi-Fi, battery and smart camera installation across Gauteng.'],
  '/solar-cctv-camera-installation/': ['Solar CCTV Camera Installation Gauteng | CMAXX', 'Solar and 4G/LTE CCTV camera installation for gates, farms, plots and remote areas in Gauteng.'],
  '/cctv-maintenance-upgrades/': ['CCTV Maintenance & Repairs Gauteng | CMAXX', 'CCTV repairs, fault finding, health checks and system upgrades across Gauteng.'],
  '/remote-cctv-viewing/': ['Remote CCTV Viewing Setup Gauteng | CMAXX', 'Secure remote CCTV viewing, playback and alert setup for phone, tablet and desktop.'],
  '/structured-cabling/': ['Structured Cabling & Network Infrastructure Gauteng | CMAXX', 'Professional Cat6 and Cat6A structured cabling, data points, PoE cabling, network racks and fibre in Midrand and across Gauteng.'],
};

const slug = process.argv[2];
if (!slug) {
  console.error('usage: node tools/export-page.mjs <slug> [outFile]');
  process.exit(1);
}
const out = process.argv[3] || `dist${slug.replace(/\/$/, '').replace(/^\//, '/').replace(/\//g, '-').replace(/^-/, '/')}.html`
  .replace('dist/', 'dist/');

const tpl = readFileSync(TEMPLATE, 'utf8');

// Fonts: lift the woff2 blobs out of the bundle manifest as data URIs.
const shell = readFileSync(BUNDLE, 'utf8');
const manifest = JSON.parse(shell.match(/<script type="__bundler\/manifest">\n([\s\S]*?)\n  <\/script>/)[1]);
const fonts = Object.entries(manifest)
  .filter(([, e]) => e.mime.startsWith('font/'))
  .map(([uuid, e]) => {
    const raw = Buffer.from(e.data, 'base64');
    const bytes = e.compressed ? gunzipSync(raw) : raw;
    return [uuid, `data:font/woff2;base64,${bytes.toString('base64')}`];
  });

// Stylesheets: the design system, then the page-level rules.
const styles = [...tpl.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(m => m[1]);
let css = styles[0] + '\n' + styles[1];
for (const [uuid, uri] of fonts) css = css.split(`url("${uuid}")`).join(`url("${uri}")`);

// The page section.
const start = tpl.indexOf(`<section data-page="${slug}"`);
if (start === -1) throw new Error(`no page found for slug ${slug}`);
const next = tpl.indexOf('<section data-page="', start + 10);
let body = tpl.slice(start, next === -1 ? tpl.indexOf('</div>\n</x-dc>') : next);

body = body
  .replace(/^<section data-page="[^"]*" data-screen-label="[^"]*" style="display: none;">\s*/, '')
  .replace(/\s*<\/section>\s*$/, '')
  .replace(/<(\/?)sc-raw-([a-z]+)/g, '<$1$2')
  .split('sc-camel-view-box=').join('viewBox=')
  .replace(/<sc-if[^>]*>/g, '')
  .split('</sc-if>').join('');

// style-hover -> a generated class plus a real :hover rule.
const hoverRules = [];
body = body.replace(/\s*style-hover="([^"]*)"/g, (_, decls) => {
  const cls = `hv${hoverRules.length}`;
  hoverRules.push(`.${cls}:hover { ${decls} }`);
  return ` data-hv="${cls}"`;
});
body = body.replace(/<[a-zA-Z][^>]*data-hv="[^"]+"[^>]*>/g, (tag) => {
  const cls = tag.match(/data-hv="([^"]+)"/)[1];
  const stripped = tag.replace(/\s*data-hv="[^"]+"/, '');
  return /\sclass="/.test(stripped)
    ? stripped.replace(/\sclass="/, ` class="${cls} `)
    : stripped.replace(/^<([a-zA-Z][\w-]*)/, `<$1 class="${cls}"`);
});

// image-slot -> a visible placeholder carrying its prompt.
body = body.replace(/<image-slot[^>]*><\/image-slot>/g, (tag) => {
  const prompt = tag.match(/placeholder="([^"]*)"/);
  return '<div class="img-slot"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
    + 'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    + '<rect x="3" y="3" width="18" height="18" rx="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle>'
    + '<path d="m21 15-5-5L5 21"></path></svg><span>'
    + (prompt ? prompt[1] : 'Image') + '</span></div>';
});

for (const leftover of ['sc-raw', 'sc-if', 'style-hover', 'image-slot', '{{']) {
  if (body.includes(leftover)) throw new Error(`unconverted canvas markup remains: ${leftover}`);
}

const [title, description] = META[slug] || ['CMAXX WiFi Solutions', ''];

const extra = `
/* Standalone-page additions: hover states lifted from the canvas, plus the
   image placeholders awaiting real CMAXX photography or diagrams. */
${hoverRules.join('\n')}
.img-slot {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 10px; text-align: center;
  padding: 24px; background: var(--color-surface);
  border: 1px dashed color-mix(in srgb, var(--color-text) 28%, transparent);
  color: var(--color-neutral-600); font-size: 14px;
}
.img-slot span { max-width: 46ch; }
@media print {
  header[style] { display: none !important; }
  details > p { display: block !important; }
  details { break-inside: avoid; }
}
`;

const html = `<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title.replace(/&/g, '&amp;')}</title>
<meta name="description" content="${description}">
<link rel="canonical" href="https://www.cmaxxwifisolutions.co.za${slug}">
<meta name="robots" content="index, follow">
<style>
${css}
${extra}
</style>
</head>
<body>
${body}
</body>
</html>
`;

mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, html);
console.log(`${out}: ${html.length.toLocaleString()} bytes, ${hoverRules.length} hover rules, ${fonts.length} fonts inlined`);
