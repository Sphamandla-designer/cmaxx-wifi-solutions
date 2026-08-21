#!/usr/bin/env node
/**
 * Phase 1 audit: walk the ./mirror produced by tools/mirror-site.sh and emit
 * the page inventory, asset inventory and observed design system into ./audit.
 *
 * This tool only records what the existing site contains. It never edits,
 * normalises or "fixes" anything — spelling mistakes, duplicated copy and
 * inconsistent terminology are reported as-is so the reconstruction can
 * preserve them exactly.
 *
 * Usage: node tools/audit-site.mjs [mirrorDir] [outDir]
 */

import { readFile, readdir, writeFile, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import * as cheerio from 'cheerio';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const MIRROR_DIR = path.resolve(process.argv[2] ?? path.join(ROOT, 'mirror'));
const OUT_DIR = path.resolve(process.argv[3] ?? path.join(ROOT, 'audit'));

/** Recursively list every file under dir. */
async function walk(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (entry.isFile()) out.push(full);
  }
  return out;
}

const collapse = (s) => (s ?? '').replace(/\s+/g, ' ').trim();

/** Classify a page from its mirror path, so the inventory records page type. */
function pageType(relPath) {
  const p = relPath.toLowerCase();
  if (/^(index|home)\.html$/.test(p)) return 'home';
  if (p.includes('contact')) return 'contact';
  if (p.includes('about')) return 'about';
  if (p.includes('case-stud')) return 'case-study';
  if (p.includes('blog') || p.includes('article') || /\/20\d\d\//.test(p)) return 'blog';
  if (p.includes('industr')) return 'industry';
  if (p.includes('area') || p.includes('serve') || p.includes('location')) return 'service-area';
  if (/(privacy|popia|cookie|terms|policy|bbbee|profile|legal)/.test(p)) return 'legal';
  if (p.includes('service') || p.includes('wifi') || p.includes('cctv') ||
      p.includes('cloud') || p.includes('cabling') || p.includes('smart-home')) return 'service';
  return 'other';
}

/** Extract the heading outline in document order. */
function headings($) {
  return $('h1,h2,h3,h4,h5,h6')
    .toArray()
    .map((el) => ({ level: Number(el.tagName.slice(1)), text: collapse($(el).text()) }))
    .filter((h) => h.text);
}

/** Extract top-level section structure: the content map for this page. */
function sections($) {
  return $('section, [class*="section"], main > div, footer')
    .toArray()
    .map((el) => {
      const $el = $(el);
      const heading = collapse($el.find('h1,h2,h3').first().text());
      const text = collapse($el.text());
      return {
        tag: el.tagName,
        classes: collapse($el.attr('class')),
        heading,
        id: $el.attr('id') ?? '',
        textPreview: text.slice(0, 400),
        images: $el.find('img').length,
        links: $el.find('a').length,
      };
    })
    // Drop wrappers that only repeat a child's content and carry no heading.
    .filter((s) => s.heading || s.images || s.links > 2);
}

function ctas($) {
  const seen = new Set();
  const out = [];
  $('a.btn, a[class*="button"], a[class*="btn"], button, input[type=submit], .elementor-button')
    .toArray()
    .forEach((el) => {
      const $el = $(el);
      const label = collapse($el.attr('value') || $el.text());
      const href = $el.attr('href') ?? '';
      const key = `${label}|${href}`;
      if (!label || seen.has(key)) return;
      seen.add(key);
      out.push({ label, href });
    });
  return out;
}

function forms($) {
  return $('form').toArray().map((el) => {
    const $el = $(el);
    return {
      action: $el.attr('action') ?? '',
      method: ($el.attr('method') ?? 'get').toLowerCase(),
      fields: $el.find('input, textarea, select').toArray().map((f) => {
        const $f = $(f);
        const name = $f.attr('name') ?? '';
        return {
          tag: f.tagName,
          type: $f.attr('type') ?? (f.tagName === 'textarea' ? 'textarea' : 'select'),
          name,
          placeholder: $f.attr('placeholder') ?? '',
          required: $f.attr('required') !== undefined,
          label: collapse($el.find(`label[for="${$f.attr('id') ?? '\u0000'}"]`).text()),
        };
      }).filter((f) => f.type !== 'hidden'),
      submitLabel: collapse(
        $el.find('button[type=submit], input[type=submit]').attr('value') ||
        $el.find('button[type=submit]').text()
      ),
    };
  });
}

/** Body copy, paragraph by paragraph, verbatim. */
function bodyCopy($) {
  return $('p, li').toArray()
    .map((el) => collapse($(el).text()))
    .filter((t) => t.length > 2);
}

function auditPage(file, relPath, html) {
  const $ = cheerio.load(html);
  const meta = (sel, attr = 'content') => collapse($(sel).attr(attr));

  return {
    file: relPath,
    slug: '/' + relPath.replace(/index\.html$/, '').replace(/\.html$/, ''),
    type: pageType(relPath),
    title: collapse($('title').text()),
    seo: {
      metaDescription: meta('meta[name="description"]'),
      canonical: meta('link[rel="canonical"]', 'href'),
      robots: meta('meta[name="robots"]'),
      ogTitle: meta('meta[property="og:title"]'),
      ogDescription: meta('meta[property="og:description"]'),
      ogImage: meta('meta[property="og:image"]'),
      structuredData: $('script[type="application/ld+json"]').length,
    },
    nav: $('nav a, header a').toArray().map((el) => ({
      label: collapse($(el).text()),
      href: $(el).attr('href') ?? '',
    })).filter((l) => l.label),
    headings: headings($),
    sections: sections($),
    ctas: ctas($),
    forms: forms($),
    bodyCopy: bodyCopy($),
    images: $('img').toArray().map((el) => {
      const $el = $(el);
      return {
        src: $el.attr('src') ?? $el.attr('data-src') ?? '',
        alt: $el.attr('alt') ?? '',
        width: $el.attr('width') ?? '',
        height: $el.attr('height') ?? '',
        loading: $el.attr('loading') ?? '',
      };
    }).filter((i) => i.src),
    links: $('a[href]').toArray().map((el) => ({
      label: collapse($(el).text()),
      href: $(el).attr('href'),
    })),
    stylesheets: $('link[rel="stylesheet"]').toArray().map((el) => $(el).attr('href')),
    scripts: $('script[src]').toArray().map((el) => $(el).attr('src')),
    footerText: collapse($('footer').text()).slice(0, 2000),
  };
}

/* ---------- design system extraction (from the mirrored CSS) ---------- */

function tally(map, key) {
  if (!key) return;
  map.set(key, (map.get(key) ?? 0) + 1);
}

function sortedTally(map, limit = 60) {
  return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit);
}

function extractDesignSystem(cssFiles) {
  const colors = new Map();
  const fonts = new Map();
  const fontSizes = new Map();
  const fontWeights = new Map();
  const lineHeights = new Map();
  const letterSpacing = new Map();
  const radii = new Map();
  const shadows = new Map();
  const spacing = new Map();
  const widths = new Map();
  const customProps = new Map();

  for (const css of cssFiles) {
    for (const m of css.matchAll(/#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)/g)) {
      tally(colors, m[0].toLowerCase());
    }
    for (const m of css.matchAll(/font-family\s*:\s*([^;}]+)/gi)) tally(fonts, collapse(m[1]));
    for (const m of css.matchAll(/font-size\s*:\s*([^;}]+)/gi)) tally(fontSizes, collapse(m[1]));
    for (const m of css.matchAll(/font-weight\s*:\s*([^;}]+)/gi)) tally(fontWeights, collapse(m[1]));
    for (const m of css.matchAll(/line-height\s*:\s*([^;}]+)/gi)) tally(lineHeights, collapse(m[1]));
    for (const m of css.matchAll(/letter-spacing\s*:\s*([^;}]+)/gi)) tally(letterSpacing, collapse(m[1]));
    for (const m of css.matchAll(/border-radius\s*:\s*([^;}]+)/gi)) tally(radii, collapse(m[1]));
    for (const m of css.matchAll(/box-shadow\s*:\s*([^;}]+)/gi)) tally(shadows, collapse(m[1]));
    for (const m of css.matchAll(/(?:padding|margin|gap)\s*:\s*([^;}]+)/gi)) tally(spacing, collapse(m[1]));
    for (const m of css.matchAll(/max-width\s*:\s*([^;}]+)/gi)) tally(widths, collapse(m[1]));
    for (const m of css.matchAll(/(--[\w-]+)\s*:\s*([^;}]+)/g)) {
      tally(customProps, `${m[1]}: ${collapse(m[2])}`);
    }
  }

  return {
    colors: sortedTally(colors),
    fonts: sortedTally(fonts, 30),
    fontSizes: sortedTally(fontSizes),
    fontWeights: sortedTally(fontWeights, 20),
    lineHeights: sortedTally(lineHeights, 30),
    letterSpacing: sortedTally(letterSpacing, 20),
    radii: sortedTally(radii, 30),
    shadows: sortedTally(shadows, 30),
    spacing: sortedTally(spacing),
    maxWidths: sortedTally(widths, 30),
    customProperties: sortedTally(customProps, 120),
  };
}

/* ---------- reporting ---------- */

function mdTally(title, entries) {
  if (!entries.length) return '';
  const rows = entries.map(([value, count]) => `| \`${value.replace(/\|/g, '\\|')}\` | ${count} |`);
  return `\n### ${title}\n\n| Value | Occurrences |\n| --- | --- |\n${rows.join('\n')}\n`;
}

function renderPageInventory(pages) {
  const byType = new Map();
  for (const p of pages) {
    if (!byType.has(p.type)) byType.set(p.type, []);
    byType.get(p.type).push(p);
  }

  let md = `# CMAXX — Phase 1 Page Inventory\n\n`;
  md += `Generated from the local mirror. ${pages.length} page(s) discovered.\n\n`;
  md += `## Summary\n\n| Type | Pages |\n| --- | --- |\n`;
  for (const [type, list] of [...byType].sort()) md += `| ${type} | ${list.length} |\n`;

  md += `\n## Pages\n\n| Slug | Title | Type | H1 | Sections | Images | Forms | CTAs |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n`;
  for (const p of pages) {
    const h1 = p.headings.find((h) => h.level === 1)?.text ?? '';
    md += `| \`${p.slug}\` | ${p.title} | ${p.type} | ${h1} | ${p.sections.length} | ${p.images.length} | ${p.forms.length} | ${p.ctas.length} |\n`;
  }

  md += `\n## Content map\n\nEach page's structure in document order, for the reconstruction to follow exactly.\n`;
  for (const p of pages) {
    md += `\n### \`${p.slug}\` — ${p.title}\n\n`;
    if (p.seo.metaDescription) md += `- **Meta description:** ${p.seo.metaDescription}\n`;
    if (p.seo.canonical) md += `- **Canonical:** ${p.seo.canonical}\n`;
    md += `\n**Heading outline**\n\n`;
    for (const h of p.headings) md += `${'  '.repeat(h.level - 1)}- H${h.level}: ${h.text}\n`;
    if (p.ctas.length) {
      md += `\n**CTAs (verbatim labels)**\n\n`;
      for (const c of p.ctas) md += `- "${c.label}" → \`${c.href}\`\n`;
    }
    if (p.forms.length) {
      md += `\n**Forms**\n\n`;
      p.forms.forEach((f, i) => {
        md += `- Form ${i + 1} (\`${f.method}\` → \`${f.action}\`), submit: "${f.submitLabel}"\n`;
        for (const field of f.fields) {
          md += `  - ${field.tag}[${field.type}] name=\`${field.name}\`${field.required ? ' *required*' : ''}${field.placeholder ? ` placeholder="${field.placeholder}"` : ''}\n`;
        }
      });
    }
  }
  return md;
}

function renderDesignSystem(ds, cssCount) {
  let md = `# CMAXX — Existing Design System (observed)\n\n`;
  md += `Extracted from ${cssCount} mirrored stylesheet(s). These are the values the `;
  md += `Phase 1 reconstruction must reproduce, not improve.\n`;
  md += `\n## Typography\n`;
  md += mdTally('Font families', ds.fonts);
  md += mdTally('Font sizes', ds.fontSizes);
  md += mdTally('Font weights', ds.fontWeights);
  md += mdTally('Line heights', ds.lineHeights);
  md += mdTally('Letter spacing', ds.letterSpacing);
  md += `\n## Colour\n`;
  md += mdTally('Colours', ds.colors);
  md += `\n## Layout\n`;
  md += mdTally('Max widths / containers', ds.maxWidths);
  md += mdTally('Spacing (padding / margin / gap)', ds.spacing);
  md += `\n## Surfaces\n`;
  md += mdTally('Border radii', ds.radii);
  md += mdTally('Shadows', ds.shadows);
  md += `\n## Custom properties (theme tokens)\n`;
  md += mdTally('CSS custom properties', ds.customProperties);
  return md;
}

function renderAssets(pages, assetFiles) {
  let md = `# CMAXX — Asset Inventory\n\n`;
  const used = new Map();
  for (const p of pages) {
    for (const img of p.images) {
      if (!used.has(img.src)) used.set(img.src, { alt: new Set(), pages: new Set() });
      used.get(img.src).alt.add(img.alt);
      used.get(img.src).pages.add(p.slug);
    }
  }
  md += `## Images referenced in markup (${used.size})\n\n| Asset | Alt text | Used on |\n| --- | --- | --- |\n`;
  for (const [src, info] of used) {
    const alts = [...info.alt].filter(Boolean).join(' / ') || '_(empty alt)_';
    md += `| \`${src}\` | ${alts} | ${[...info.pages].join(', ')} |\n`;
  }
  md += `\n## Binary assets present in the mirror (${assetFiles.length})\n\n`;
  for (const f of assetFiles) md += `- \`${f.rel}\` — ${(f.size / 1024).toFixed(1)} KB\n`;
  return md;
}

/** Observations only — issues to fix in Phase 2, never in Phase 1. */
function renderIssues(pages) {
  const issues = [];
  for (const p of pages) {
    const h1s = p.headings.filter((h) => h.level === 1);
    if (h1s.length === 0) issues.push([p.slug, 'No H1 on the page']);
    if (h1s.length > 1) issues.push([p.slug, `${h1s.length} H1 elements on one page`]);
    if (!p.seo.metaDescription) issues.push([p.slug, 'Missing meta description']);
    if (!p.seo.canonical) issues.push([p.slug, 'Missing canonical URL']);
    if (!p.title) issues.push([p.slug, 'Missing <title>']);
    if (p.title && p.title.length > 60) issues.push([p.slug, `Title is ${p.title.length} chars (over 60)`]);

    const noAlt = p.images.filter((i) => !i.alt.trim());
    if (noAlt.length) issues.push([p.slug, `${noAlt.length} image(s) with empty alt text`]);

    // Heading level skips, e.g. H2 followed directly by H4.
    for (let i = 1; i < p.headings.length; i++) {
      const jump = p.headings[i].level - p.headings[i - 1].level;
      if (jump > 1) {
        issues.push([p.slug, `Heading level skip: H${p.headings[i - 1].level} → H${p.headings[i].level} ("${p.headings[i].text}")`]);
        break;
      }
    }

    for (const f of p.forms) {
      const unlabelled = f.fields.filter((x) => !x.label && !x.placeholder);
      if (unlabelled.length) issues.push([p.slug, `${unlabelled.length} form field(s) with no label or placeholder`]);
    }

    // Ambiguous link text is a known accessibility/UX smell.
    const vague = p.links.filter((l) => /^(click here|read more|here|more|learn more)$/i.test(l.label));
    if (vague.length) issues.push([p.slug, `${vague.length} link(s) with non-descriptive text`]);
  }

  // Duplicate titles across pages.
  const titles = new Map();
  for (const p of pages) {
    if (!p.title) continue;
    if (!titles.has(p.title)) titles.set(p.title, []);
    titles.get(p.title).push(p.slug);
  }
  for (const [title, slugs] of titles) {
    if (slugs.length > 1) issues.push(['(site)', `Duplicate <title> "${title}" on: ${slugs.join(', ')}`]);
  }

  let md = `# CMAXX — Known Inconsistencies in the Existing Site\n\n`;
  md += `> **Phase 2 backlog.** These are recorded, not fixed. The Phase 1\n`;
  md += `> reconstruction preserves the existing site exactly, including these issues.\n\n`;
  if (!issues.length) return md + `_No automated findings._\n`;
  md += `| Page | Observation |\n| --- | --- |\n`;
  for (const [slug, issue] of issues) md += `| \`${slug}\` | ${issue} |\n`;
  return md;
}

/* ---------- main ---------- */

async function main() {
  if (!existsSync(MIRROR_DIR)) {
    console.error(`No mirror found at ${MIRROR_DIR}`);
    console.error(`Run "npm run mirror" first (needs internet access to the live site).`);
    process.exit(1);
  }

  const files = await walk(MIRROR_DIR);
  const htmlFiles = files.filter((f) => /\.html?$/i.test(f));
  const cssPaths = files.filter((f) => /\.css$/i.test(f));

  if (!htmlFiles.length) {
    console.error(`Mirror at ${MIRROR_DIR} contains no HTML files.`);
    process.exit(1);
  }

  const pages = [];
  for (const file of htmlFiles) {
    const rel = path.relative(MIRROR_DIR, file);
    pages.push(auditPage(file, rel, await readFile(file, 'utf8')));
  }
  pages.sort((a, b) => a.slug.localeCompare(b.slug));

  // Inline <style> blocks count toward the design system too.
  const cssSources = await Promise.all(cssPaths.map((f) => readFile(f, 'utf8')));
  for (const file of htmlFiles) {
    const $ = cheerio.load(await readFile(file, 'utf8'));
    $('style').each((_, el) => cssSources.push($(el).text()));
  }
  const designSystem = extractDesignSystem(cssSources);

  const assetFiles = await Promise.all(
    files
      .filter((f) => /\.(png|jpe?g|gif|svg|webp|avif|ico|woff2?|ttf|otf|eot|mp4|webm|pdf)$/i.test(f))
      .map(async (f) => ({ rel: path.relative(MIRROR_DIR, f), size: (await stat(f)).size }))
  );

  await mkdir(OUT_DIR, { recursive: true });
  await writeFile(path.join(OUT_DIR, 'page-inventory.json'), JSON.stringify(pages, null, 2));
  await writeFile(path.join(OUT_DIR, 'page-inventory.md'), renderPageInventory(pages));
  await writeFile(path.join(OUT_DIR, 'design-system.md'), renderDesignSystem(designSystem, cssSources.length));
  await writeFile(path.join(OUT_DIR, 'design-system.json'), JSON.stringify(designSystem, null, 2));
  await writeFile(path.join(OUT_DIR, 'assets.md'), renderAssets(pages, assetFiles));
  await writeFile(path.join(OUT_DIR, 'known-issues.md'), renderIssues(pages));

  console.log(`Pages audited:      ${pages.length}`);
  console.log(`Stylesheets parsed: ${cssSources.length}`);
  console.log(`Assets in mirror:   ${assetFiles.length}`);
  console.log(`\nWrote to ${path.relative(ROOT, OUT_DIR)}/:`);
  for (const f of ['page-inventory.md', 'page-inventory.json', 'design-system.md', 'design-system.json', 'assets.md', 'known-issues.md']) {
    console.log(`  - ${f}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
