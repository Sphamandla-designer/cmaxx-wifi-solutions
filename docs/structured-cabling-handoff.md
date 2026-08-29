# Structured Cabling & Network Infrastructure — build + handoff

Rebuild of `/infrastructure-cabling/` as a completely new page, `/structured-cabling/`.
Full replacement, not a copy edit: none of the old page's guest-WiFi copy, "why proper
CCTV matters" content, generic WiFi troubleshooting content, unsourced percentage claims
or animated counters carry over.

## What is in this repository

| Path | What it is |
| --- | --- |
| `site/structured-cabling/index.html` | The complete page — all 22 sections, ~30 FAQs, final CTA |
| `site/structured-cabling/assets/styles.css` | Design tokens lifted from the live Elementor kit |
| `site/structured-cabling/assets/img/` | Three genuine CMAXX photos, plus a README on the three still wanted |
| `dist/structured-cabling-complete.html` | One fully self-contained file — CSS, fonts and photos all embedded, zero external requests |
| `content/structured-cabling.md` | The page copy as plain text, for pasting into Elementor |
| `tools/qa-structured-cabling.mjs` | Executable pre-launch checklist — `node tools/qa-structured-cabling.mjs` |

Open `site/structured-cabling/index.html` in a browser to review the page as built, or
run `npm run build:embedded` and open `dist/structured-cabling-complete.html` — a single
file with the stylesheet, the Outfit webfont and every photo embedded, which renders
identically with no network connection at all.

## Two things this session could not do

**1. It could not publish to WordPress.** The session has no WP admin, FTP or REST
credentials for `1124817.eu9.myftpupload.com`, so nothing here is live. Everything below
under "WordPress tasks" has to be carried out by someone with site access. The HTML is
written to be usable either as the source for rebuilding the page in Elementor, or dropped
straight into an HTML widget / page template — the CSS is self-contained and namespaced to
this page.

**2. It did not have `CMAXX_Structured_Cabling_Website_Developer_Brief.pdf`.** The brief is
not in this repository, not on the staging site, and not in the connected Google Drive.
The build prompt asks for the *exact* customer-facing copy from section 02 and the FAQ list
from section 03, and says explicitly not to paraphrase the three technical comparison
tables. **Every word on this page was therefore written for this build, not taken from the
brief.** It is all written to the accuracy guardrails (see below) and is safe to publish as
it stands, but before launch it should be diffed against sections 02 and 03 of the PDF and
the brief's wording used wherever the two differ — particularly in the Cat5/5e/6/6A, CCA vs
copper and solid vs stranded tables, whose wording the brief says has been checked against
manufacturer and standards sources. Send the PDF through and the copy can be reconciled.

## Design system

Taken verbatim from the live site, not invented. Source: `.elementor-kit-8` global tokens
plus `post-493.css` (the WiFi & Network Solutions page stylesheet).

| Token | Value | Origin |
| --- | --- | --- |
| Brand orange | `#FF6C24` | `--e-global-color-3280544` |
| Dark navy | `#0E1725` | `--e-global-color-4a9b6d6` |
| Muted (body on dark) | `#94A2B8` | `--e-global-color-a3173ef` |
| Body (on light) | `#54595F` | `--e-global-color-secondary` |
| Navy 4% wash | `#0E17250A` | `--e-global-color-7bedddd` |
| Font | Outfit | the only font family used on the WiFi page (111 declarations) |
| H1 / H2 / card H3 | 50 / 40 / 22 px, weights 800 / 800 / 600 | WiFi page |
| Buttons | radius 6px, padding 16×36, weight 500, letter-spacing 0.2px | WiFi page |
| Button hover | orange → navy background, orange text | WiFi page |
| Cards | radius 8px | most-used radius on the WiFi page |

## Technical accuracy guardrails — how each is honoured

Each of these is asserted by `tools/qa-structured-cabling.mjs`, so a later copy edit that
breaks one fails the check rather than reaching production quietly.

| Guardrail | How the page handles it |
| --- | --- |
| Certification | Default wording is "tested and verified" throughout. §16 and the FAQ both explain that certification means a certification analyser plus report, that it is an available scope on projects that require it, and that CMAXX confirms in writing which applies. No blanket "every project certified". |
| Cat6 10GbE | Always qualified: "can support 10 Gbps only over shorter runs, and the achievable distance depends on the installation and the surrounding electrical environment — it is not a flat capability across a full-length link." Never stated as 10Gbps to 100 m. |
| Cat6A 10GbE | Stated as "designed to carry 10 Gbps over a full 100 m channel **when correctly installed**". The qualifier appears in every capability claim. |
| CCA | Framed as "not equivalent to compliant copper Category cabling", with the reasons given (resistance, PoE heat and voltage drop, brittleness). The word "illegal" appears nowhere on the page. |
| Failure statistics | No percentages anywhere. §3 describes physical-layer fault causes qualitatively and offers a survey instead of a statistic. (The only `%` on the page is "100% copper", a conductor spec.) |
| Experience / project counts | No stat section, no counters, no numbers. Nothing rendered as 0/0%/0hr. |
| "Free" | The page never uses the pricing sense of "free". CTA is "Book a Cabling Site Survey" everywhere. |

## CTA identity

One primary CTA label across the whole page — **"Book a Cabling Site Survey"** — at the
hero, after the technical-education block, after the FAQ, and in the final CTA section.
Secondary "Request a Quote", tertiary "WhatsApp CMAXX" / "Call Us". No label drift.

## Internal linking — outbound

Four of the twelve targets in the build prompt **do not exist on the live site** (verified
by HTTP status against the staging host):

| Prompt target | Status | What the page does instead |
| --- | --- | --- |
| `/home-wifi-solutions/` | 404 | Links to `/wifi-network-solutions/`, which carries "Home WiFi Optimisation" as a section |
| `/business-office-wifi-solutions/` | 404 | Links to `/wifi-network-solutions/` ("Business & Office WiFi Solutions" section) |
| `/outdoor-wifi-solutions/` | 404 | Links to `/wifi-network-solutions/` ("Outdoor WiFi Solutions" section) |
| `/wifi-assessment-troubleshooting/` | 404 | Links to `/wifi-network-solutions/` ("Network Assessment" section) |

Those four sections on `/wifi-network-solutions/` have no anchor IDs, so a deep link is not
possible either. **Decision needed:** if those four pages are planned, say so and the links
can be repointed; if they are not, adding anchor IDs to the WiFi page would let this page
link to the right section rather than the page top. Anchor text on this page is already
written to match the intended destinations ("Home WiFi Solutions", "Business & Office WiFi
Solutions", "outdoor WiFi coverage", "WiFi assessment and troubleshooting"), so repointing
is a one-line change per link.

The remaining eight targets all resolve and are implemented as real crawlable `<a href>`
elements: `/wifi-network-solutions/`, `/cctv-security-solutions/`, `/smart-home/`,
`/managed-wifi/`, `/public-guest-wifi/`, `/industries/`, `/areas-we-serve/`, `/our-work/`.

## Internal linking — inbound (WordPress task, not done here)

Each of these existing pages needs one contextual link back to `/structured-cabling/`,
placed where the page already talks about data points, wired backhaul, PoE, Ethernet,
network racks or physical infrastructure. Anchor text is varied deliberately — do not
repeat one exact anchor.

| Page | Suggested anchor text |
| --- | --- |
| `/wifi-network-solutions/` | structured cabling |
| `/home-wifi-solutions/` *(when it exists)* | Ethernet data points |
| `/business-office-wifi-solutions/` *(when it exists)* | Cat6 network cabling |
| `/wifi-assessment-troubleshooting/` *(when it exists)* | wired network infrastructure |
| `/outdoor-wifi-solutions/` *(when it exists)* | network cabling installation |
| `/managed-wifi/` | wired network infrastructure |
| `/cctv-security-solutions/` | PoE cabling |
| `/smart-home/` | Ethernet data points |
| `/public-guest-wifi/` | network cabling installation |

The four pages marked *(when it exists)* are the same 404s listed above; their inbound links
have to wait until those pages are built, or be added to `/wifi-network-solutions/` instead.

## WordPress tasks (require site access)

1. **Create the page** at slug `/structured-cabling/`, titled
   "Structured Cabling & Network Infrastructure".
2. **301 redirect** `/infrastructure-cabling/` → `/structured-cabling/`. The old URL is
   currently live and returns 200, so this is required, not conditional.
3. **Navigation label** → "Structured Cabling". The primary menu currently reads
   "Infrastructure & Cabling"; the footer's Core Services list says the same. Both must
   change. Check for any other occurrence site-wide before signing off.
4. **Breadcrumb** → Home > Services > Structured Cabling & Network Infrastructure.
5. **SEO title / meta description** — exactly as set in the `<head>` of `index.html`.
6. **Canonical** — `https://www.cmaxxwifisolutions.co.za/structured-cabling/`. Never
   canonical to `1124817.eu9.myftpupload.com`.
7. **noindex** — staging stays `noindex` (and ideally password-protected) until the final
   domain launch. The `<meta name="robots" content="noindex, nofollow">` line in
   `index.html` is marked for deletion at launch.
8. **Contact details** — the page uses `info@cmaxxwifisolutions.co.za` throughout, per the
   brief. Note the live site also has `admin@cmaxxsolutions.co.za` in places; that address
   is deliberately not used here.
9. **Photography** — the hero, the outdoor section and the PoE section now carry genuine
   CMAXX photos pulled from the media library. Three further slots (a data-point
   termination, fibre work, a Cat6/Cat6A close-up) have no real photo yet; those sections
   were rebuilt to work without one rather than carry stock. See
   `site/structured-cabling/assets/img/README.md`.
10. **Inbound links** — the nine pages in the table above.

## Pre-launch checklist

Run `node tools/qa-structured-cabling.mjs` — it enforces the mechanical items (one H1, all
22 sections, the three comparison tables and their mobile behaviour, every guardrail above,
CTA consistency and placement, crawlable internal links, FAQ answers present in the DOM,
lazy-loading, alt text, table captions and scoped headers).

These still need a human:

- [ ] Copy reconciled against sections 02 and 03 of the developer brief
- [ ] Hero, outdoor and PoE photos approved (all genuine CMAXX work, no stock)
- [ ] Optional: shoot the three missing subjects — data-point termination, fibre, Cat6A close-up
- [ ] Nav, breadcrumb and footer say "Structured Cabling" — no "Infrastructure & Cabling"
      left anywhere on the site
- [ ] 301 from `/infrastructure-cabling/` in place and tested
- [ ] Inbound links added to the nine related pages
- [ ] Phone, WhatsApp, email and enquiry buttons all tested live
- [ ] Staging still noindex; production canonical correct once live
- [ ] The three high-risk claims re-read by hand after any copy edit: Cat6 10GbE
      qualification, "tested and verified" vs "certified", CCA framing

## Notes

- FAQ uses native `<details>`/`<summary>`: keyboard and screen-reader accessible by
  default, and every question and answer is in the rendered DOM. No FAQPage schema is
  included — per the brief, it is not treated as an SEO requirement. It can be added later
  if it accurately mirrors the visible copy.
- The three comparison tables scroll horizontally on tablet and reflow into stacked cards
  on mobile (each `<td>` carries a `data-label`), so they are never shrunk to unreadable.
- No JavaScript on the page at all, and no decorative animation.
