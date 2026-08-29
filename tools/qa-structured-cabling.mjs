#!/usr/bin/env node
/**
 * Pre-launch QA gate for /structured-cabling/.
 *
 * Encodes the brief's section 09 checklist and the technical-accuracy
 * guardrails as executable assertions, so the page cannot regress on the
 * items that survived into the live build last time.
 *
 *   node tools/qa-structured-cabling.mjs
 */

import { readFileSync } from 'node:fs';

const FILE = 'site/structured-cabling/index.html';
const html = readFileSync(FILE, 'utf8');
const text = html.replace(/<script[\s\S]*?<\/script>/gi, '')
                 .replace(/<!--[\s\S]*?-->/g, '')
                 .replace(/<[^>]+>/g, ' ')
                 .replace(/&amp;/g, '&')
                 .replace(/\s+/g, ' ');

const results = [];
const check = (name, ok, detail = '') => results.push({ name, ok, detail });

/* ---------------------------------------------------------------- */
/* Structure                                                         */
/* ---------------------------------------------------------------- */

const h1s = [...html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)];
check('Exactly one H1', h1s.length === 1, `found ${h1s.length}`);
check(
  'H1 text is exact',
  h1s.length === 1 &&
    h1s[0][1].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').trim() ===
      'Structured Cabling & Network Infrastructure in Gauteng',
  h1s[0]?.[1].replace(/<[^>]+>/g, '').trim(),
);

const REQUIRED_SECTIONS = [
  ['1. Hero + trust + CTA', 'hero'],
  ['2. What structured cabling is', 'what-is-structured-cabling'],
  ['3. Why the physical layer matters', 'why-it-matters'],
  ['4. Services table', 'services'],
  ['5. Cat5/5e/6/6A education', 'cable-categories'],
  ['6. CCA vs 100% copper', 'cca-vs-copper'],
  ['7. Solid vs stranded', 'solid-vs-stranded'],
  ['8. UTP vs shielded', 'utp-vs-shielded'],
  ['9. Indoor vs outdoor', 'indoor-vs-outdoor'],
  ['10. Distance & fibre backbones', 'distance'],
  ['11. PoE-ready infrastructure', 'poe'],
  ['12. Data points & patch panels', 'data-points'],
  ['13. Cabinets & server racks', 'racks'],
  ['14. Fibre for backbones', 'fibre'],
  ['15. Upgrades & fault finding', 'upgrades'],
  ['16. Testing, labelling, documentation', 'testing'],
  ['17. Residential & commercial use cases', 'use-cases'],
  ['18. Installation process', 'process'],
  ['19. Why choose CMAXX', 'why-cmaxx'],
  ['20. Gauteng service area', 'service-area'],
  ['21. Related services / internal links', 'related'],
  ['22. FAQ', 'faq'],
];
const missing = REQUIRED_SECTIONS.filter(([, id]) => !html.includes(`id="${id}"`));
check(`All 22 required sections present`, missing.length === 0,
  missing.map(([n]) => n).join('; '));

check('Final conversion CTA section present', html.includes('id="final-cta"'));
check('Breadcrumb present and correctly labelled',
  html.includes('aria-label="Breadcrumb"') &&
  /Home[\s\S]{0,120}Services[\s\S]{0,160}Structured Cabling & Network Infrastructure/.test(
    html.split('aria-label="Breadcrumb"')[1].split('</nav>')[0].replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&')));

/* ---------------------------------------------------------------- */
/* Comparison tables                                                 */
/* ---------------------------------------------------------------- */

for (const [label, id] of [
  ['Cat5/5e/6/6A', 'cable-categories'],
  ['CCA vs copper', 'cca-vs-copper'],
  ['Solid vs stranded', 'solid-vs-stranded'],
  ['Service table', 'services'],
  ['6-stage process table', 'process'],
]) {
  const sec = html.split(`id="${id}"`)[1]?.split('</section>')[0] ?? '';
  check(`${label}: rendered as a real <table>`, /<table[\s\S]*?<\/table>/.test(sec));
  check(`${label}: mobile-responsive (scroll + stack)`,
    sec.includes('table-scroll') && sec.includes('stack-mobile'));
  const bodyCells = [...sec.matchAll(/<td\b[^>]*>/g)];
  const labelled = bodyCells.filter(c => c[0].includes('data-label'));
  check(`${label}: every <td> carries data-label for the stacked view`,
    bodyCells.length > 0 && bodyCells.length === labelled.length,
    `${labelled.length}/${bodyCells.length}`);
}

const stages = ['Assess', 'Design', 'Specify', 'Install', 'Test & Label', 'Commission & Handover'];
const proc = html.split('id="process"')[1]?.split('</section>')[0] ?? '';
const procText = proc.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&');
check('Process table has all 6 named stages',
  stages.every(s => procText.includes(s)),
  stages.filter(s => !procText.includes(s)).join(', '));

/* ---------------------------------------------------------------- */
/* Technical-accuracy guardrails                                     */
/* ---------------------------------------------------------------- */

// "certified" must never appear as a blanket claim.
const BANNED_CERT = [
  /every project (?:is )?certified/i,
  /all (?:projects|installations|cabling) (?:are |is )?certified/i,
  /fully certified/i,
  /certified installation/i,
];
check('No blanket "certified" claim',
  !BANNED_CERT.some(r => r.test(text)),
  BANNED_CERT.filter(r => r.test(text)).map(String).join(' '));
check('Uses "tested and verified" as the default wording',
  /tested and verified/i.test(text));
check('Where "certif" appears it is scoped to an analyser + report',
  !/certif/i.test(text) || /certification analyser/i.test(text));

// Cat6 10GbE must always be qualified.
const cat6Claim = /Cat\s?6\b[^.]{0,120}10\s?G(?:bps|bE)[^.]{0,160}\./gi;
const cat6Sentences = text.match(cat6Claim) ?? [];
const cat6Unqualified = cat6Sentences.filter(s =>
  !/(short|shorter|distance|depends|environment|not a flat|only over)/i.test(s));
check('Cat6 10GbE is always distance/environment-qualified',
  cat6Unqualified.length === 0,
  cat6Unqualified.join(' | '));
check('No flat "Cat6 supports 10Gbps to 100m" claim',
  !/Cat\s?6\b(?!A)[^.]{0,80}10\s?G[^.]{0,40}100\s?m/i.test(text));

// Cat6A must keep the "correctly installed" qualifier.
// Only sentences that assert a capability ("designed to carry", "supports",
// "over a full ... channel") need the qualifier; merely recommending Cat6A
// where 10 Gbps matters is not a capability claim.
const cat6aClaims = (text.match(/Cat\s?6A[^.]{0,240}10\s?G(?:bps|bE)[^.]{0,240}\./gi) ?? [])
  .filter(s => /(designed to carry|supports?|capable of|over a full)/i.test(s));
check('Cat6A 10GbE capability claims keep the "correctly installed" qualifier',
  cat6aClaims.length > 0 && cat6aClaims.every(s => /correctly installed/i.test(s)),
  `${cat6aClaims.length} claim(s); unqualified: ` +
  cat6aClaims.filter(s => !/correctly installed/i.test(s)).join(' | '));

// CCA framing.
check('CCA described as "not equivalent to compliant copper Category" cabling',
  /not equivalent to compliant copper Category/i.test(text));
check('No unqualified "illegal" claim about CCA',
  !/\billegal\b/i.test(text));

// Statistics.
// "100% copper" is a conductor specification, not a statistic.
const pctHits = (text.match(/\d+\s?%(?!\s*copper)/gi) ?? []);
check('No percentage statistics anywhere (100% copper excepted)',
  pctHits.length === 0,
  (text.match(/[^.]{0,70}\d+\s?%(?!\s*copper)[^.]{0,70}/gi) ?? []).join(' | '));
check('No "70% of network failures" style stat',
  !/\b\d{2}\s?%[^.]{0,60}(failure|fault|problem|downtime)/i.test(text));

// "Free".
// Bans the pricing sense only. "Space left free for the next switch" is fine;
// "free assessment / survey / quote / consultation" is not.
const freeHits = (text.match(
  /\bfree\b(?:\s+\w+){0,2}\s*(assessment|survey|quote|quotation|consultation|audit|call-?out|installation)|\b(?:no[- ]obligation|complimentary)\b/gi
) ?? []);
check('No "free" assessment / survey pricing language',
  freeHits.length === 0, freeHits.join(' | '));

// Animated counters.
check('No zero-value animated counters',
  !/(counter|odometer|countup|funfact|\bstat-number\b)/i.test(html) &&
  !/>\s*0\s*(?:%|hr|\+)?\s*</.test(html));

// Leftover copy from the discarded page.
const LEFTOVERS = [
  [/(?<!public & )(?<!public and )guest wifi/i, 'guest WiFi copy'],
  [/why proper CCTV matters/i, 'CCTV "why it matters" copy'],
  [/Infrastructure & Cabling/i, 'old "Infrastructure & Cabling" label'],
  [/Book a Guest WiFi Consultation/i, 'wrong-page CTA label'],
  [/Request a Free Network Assessment/i, 'old free-assessment CTA'],
  [/Most venues offer free WiFi/i, 'old venue WiFi copy'],
];
for (const [re, what] of LEFTOVERS) {
  // "Public & Guest WiFi" is a legitimate nav/related-services link label.
  const hits = (text.match(new RegExp(re.source, 'gi')) ?? []);
  check(`No leftover ${what}`, hits.length === 0, hits.join(' | '));
}
check('"Guest WiFi" appears only as a link label, never as page copy',
  (text.match(/guest wifi/gi) ?? []).length ===
  (text.match(/public (?:&|and) guest wifi/gi) ?? []).length);

/* ---------------------------------------------------------------- */
/* CTA consistency                                                   */
/* ---------------------------------------------------------------- */

const primaryCtas = (html.match(/Book a Cabling Site Survey/g) ?? []).length;
check('Primary CTA "Book a Cabling Site Survey" used repeatedly',
  primaryCtas >= 4, `${primaryCtas} occurrences`);
check('Secondary CTA "Request a Quote" present', html.includes('Request a Quote'));
check('Tertiary CTA "WhatsApp CMAXX" present', html.includes('WhatsApp CMAXX'));
check('CTA above the fold (hero)',
  (html.split('id="what-is-structured-cabling"')[0] ?? '').includes('Book a Cabling Site Survey'));
check('CTA after the technical-education block',
  html.split('id="racks"')[0].split('id="poe"')[1]?.includes('Book a Cabling Site Survey') ?? false);
check('CTA after the FAQ block',
  (html.split('id="faq"')[1] ?? '').includes('Book a Cabling Site Survey'));
check('Micro-CTA on the racks section is verbatim',
  html.includes('Inherited a messy cabinet? Ask CMAXX for a network rack clean-up and documentation assessment.'));
check('FAQ closing CTA copy is verbatim',
  text.includes('Still unsure which cable or network design your property needs? Book a CMAXX cabling site survey and we will assess the existing infrastructure, required devices, cable routes and future requirements before recommending a solution.'));

/* ---------------------------------------------------------------- */
/* SEO / identity                                                    */
/* ---------------------------------------------------------------- */

check('SEO title exact',
  html.includes('<title>Structured Cabling &amp; Network Infrastructure Gauteng | CMAXX</title>'));
check('Meta description exact',
  html.includes('content="Professional Cat6 and Cat6A structured cabling, data points, PoE cabling, network racks and fibre in Midrand and across Gauteng. Book a site survey."'));
check('Canonical points at the production domain',
  html.includes('<link rel="canonical" href="https://www.cmaxxwifisolutions.co.za/structured-cabling/">'));
check('Canonical never points at the staging host',
  !/rel="canonical"[^>]*myftpupload/.test(html));
check('Staging noindex still in place (remove on production launch)',
  /<meta name="robots" content="noindex/.test(html));
check('Contact email is info@cmaxxwifisolutions.co.za',
  html.includes('info@cmaxxwifisolutions.co.za') && !html.includes('admin@cmaxxsolutions.co.za'));
check('Nav + footer use the "Structured Cabling" label',
  (html.match(/>Structured Cabling</g) ?? []).length >= 2);

/* ---------------------------------------------------------------- */
/* Internal links — real crawlable anchors                           */
/* ---------------------------------------------------------------- */

const OUTBOUND = [
  '/wifi-network-solutions/', '/cctv-security-solutions/', '/smart-home/',
  '/managed-wifi/', '/public-guest-wifi/', '/industries/',
  '/areas-we-serve/', '/our-work/', '/contact/',
];
for (const href of OUTBOUND) {
  check(`Outbound link ${href} is a real <a href>`,
    new RegExp(`<a[^>]+href="${href.replace(/\//g, '\\/')}"`).test(html));
}
check('No JS-only pseudo-links', !/href="(#|javascript:)"/.test(html));

/* ---------------------------------------------------------------- */
/* FAQ + accessibility                                               */
/* ---------------------------------------------------------------- */

const faqBlock = html.split('id="faq"')[1]?.split('</section>')[0] ?? '';
const qs = [...faqBlock.matchAll(/<summary>/g)].length;
const as = [...faqBlock.matchAll(/class="faq-answer"/g)].length;
check('FAQ has ~25 questions', qs >= 25, `${qs} questions`);
check('Every FAQ question has an answer in the DOM', qs === as, `${qs} q / ${as} a`);
check('FAQ uses native details/summary (keyboard + screen-reader accessible)',
  faqBlock.includes('<details>') && faqBlock.includes('<summary>'));
check('FAQ answers are in the rendered HTML, not JS-injected',
  !/faqData|renderFaq|innerHTML/.test(html));

check('Skip link present', html.includes('class="skip-link"'));
check('Below-the-fold images lazy-loaded',
  [...html.matchAll(/<img\b[^>]*>/g)]
    .filter(m => !m[0].includes('fetchpriority="high"'))
    .every(m => m[0].includes('loading="lazy"')));
check('Hero image is not lazy-loaded',
  /<img[^>]*fetchpriority="high"[^>]*>/.test(html) &&
  !/<img[^>]*fetchpriority="high"[^>]*loading="lazy"/.test(html));
check('Every image has alt text',
  [...html.matchAll(/<img\b[^>]*>/g)].every(m => /\salt="[^"]+"/.test(m[0])));
check('Every table has a caption and scoped headers',
  [...html.matchAll(/<table[\s\S]*?<\/table>/g)]
    .every(t => t[0].includes('<caption>') && t[0].includes('scope="col"') && t[0].includes('scope="row"')));
check('No heavy decorative animation libraries', !/<script[^>]+src=/.test(html));

/* ---------------------------------------------------------------- */
/* Report                                                            */
/* ---------------------------------------------------------------- */

const failed = results.filter(r => !r.ok);
for (const r of results) {
  console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}${r.ok || !r.detail ? '' : `\n        → ${r.detail}`}`);
}
console.log(`\n${results.length - failed.length}/${results.length} checks passed.`);
process.exit(failed.length === 0 ? 0 : 1);
