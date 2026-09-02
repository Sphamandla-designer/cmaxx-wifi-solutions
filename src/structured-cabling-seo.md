# Structured cabling page — SEO and implementation specification

The structured cabling page is a `data-page` section inside the single
design-canvas document (`src/site.dc.html`, packed into
`CMAXX Website (standalone).html`). One document cannot carry per-page titles,
canonicals or schema, so the metadata below is specified here for the
WordPress implementation rather than faked in the prototype.

Everything in the brief's customer-facing copy — the full 22-section flow, the
Cat5/Cat5e/Cat6/Cat6A comparison, CCA versus copper, solid versus stranded,
UTP versus shielded, indoor versus outdoor, the 90 m / 100 m distance
explanation, PoE, data points, cabinets, fibre, upgrades, testing and
documentation, use cases, process, differentiators, service area, related
services, FAQs and the final CTA — is implemented in the page itself.

## Page identity

| Element | Value |
| --- | --- |
| Navigation label | Structured Cabling |
| Page name | Structured Cabling & Network Infrastructure |
| Slug | `/structured-cabling/` |
| H1 | Structured Cabling & Network Infrastructure in Gauteng |
| SEO title | Structured Cabling & Network Infrastructure Gauteng \| CMAXX |
| Meta description | Professional Cat6 and Cat6A structured cabling, data points, PoE cabling, network racks and fibre in Midrand and across Gauteng. Book a site survey. |
| Breadcrumb | Home > Services > Structured Cabling & Network Infrastructure |
| Primary CTA | Book a Cabling Site Survey |
| Secondary CTA | Request a Quote / WhatsApp CMAXX |

## Technical SEO

- Self-canonical to `https://www.cmaxxwifisolutions.co.za/structured-cabling/`.
  Never inherit a staging-domain canonical or `noindex` tag.
- Staging must stay `noindex` or password-protected until the final domain
  launches; the production page must be indexable.
- If `/infrastructure-cabling/` ever exists on the live domain, 301 it to
  `/structured-cabling/`. The prototype's router aliases the old path so the
  CCTV cluster's `/infrastructure-cabling/` anchors resolve; decide on one
  canonical slug before launch.
- `Service` and `BreadcrumbList` structured data, with organisation and
  local-business information at the appropriate site level. Mark up only facts
  visible and true on the page.
- FAQ content is published for users and topical depth. Do not expect a Google
  FAQ rich result for a commercial service page.
- Keep name, telephone, email and Midrand/Gauteng service information
  consistent with the site and the Google Business Profile.
- Add the URL to the XML sitemap and request indexing after QA.

## Image plan

The page carries six `<image-slot>` placeholders. Each needs a genuine CMAXX
project photograph before launch — real rack, cabling, access-point and
data-point photos, ahead of generic stock.

| Slot id | Suggested filename | Alt text |
| --- | --- | --- |
| `p6-cabling-hero` | `network-rack-patch-panel-midrand.jpg` | Labelled network rack and patch panel installation in Midrand |
| `p6-cable-termination` | `cat6-cat6a-structured-cabling-gauteng.jpg` | Cat6 and Cat6A structured cabling installation by CMAXX WiFi Solutions |
| `p6-outdoor-run` | `outdoor-network-cabling-gauteng.jpg` | Protected outdoor network cabling installation in Gauteng |
| `p6-poe-ap-cabling` | `poe-wifi-access-point-cabling.jpg` | PoE Ethernet cabling for a ceiling WiFi access point |
| `p6-data-point` | `ethernet-data-point-installation.jpg` | Professional Ethernet data point installation |
| `p6-fibre-backbone` | `fibre-backbone-network-installation.jpg` | Fibre backbone network link for a multi-building property |

Compress to WebP or AVIF, serve responsive sizes, lazy-load everything below
the fold, and set width and height on the hero image without lazy-loading it.

## Accuracy guardrails held in the copy

- "Tested and verified" is the standard claim. "Certified" is used only when
  describing formal standards-based certification as a separately scoped
  service with a report.
- Cat6 10GbE is described as distance- and environment-dependent, not as
  10 Gbps to 100 m. Cat6A is described as designed for 10GbE over a full 100 m
  channel when correctly installed.
- CCA is described as not equivalent to compliant copper Category cable. No
  South Africa-specific legality claim is made.
- No failure statistics, no animated counters, no invented project counts.
- "Book a Site Survey", not "free assessment".

## Outstanding before launch

- **Operational confirmation.** The brief asks CMAXX to confirm that all
  permanent Category cable purchased for future projects is genuine copper, not
  CCA, before the copper-cabling standard is published as company policy.
- **Six linked-to pages do not exist yet** in the prototype:
  `/smart-home/`, `/managed-wifi/`, `/public-guest-wifi/`, `/industries/`,
  `/areas-we-serve/` and `/case-studies/`. The cabling page links to all of
  them per the brief's internal-link map; in the prototype those links fall
  through to the contact section. The brief specifies no copy for these pages.
- **Backlinks into this page** exist from every WiFi page and the CCTV hub and
  cluster. They still need adding to Smart Home, Managed WiFi and Public &
  Guest WiFi once those pages exist, using varied anchors: "structured
  cabling", "Cat6 network cabling", "Ethernet data points", "wired network
  infrastructure", "PoE cabling", "network cabling installation".
- **Verified case studies.** No placeholder projects have been written.
