# CCTV service cluster — per-page SEO specification

The six CCTV child pages are built as `data-page` sections inside the single
design-canvas document (`src/site.dc.html`, packed into
`CMAXX Website (standalone).html`). One document cannot carry six titles, six
meta descriptions, six canonicals or six schema blocks, so the per-page SEO
metadata below is specified here for the WordPress implementation rather than
faked in the prototype.

Everything else in the brief's launch checklist — heading hierarchy, crawlable
`<a href>` links with descriptive anchor text, breadcrumbs, server-rendered FAQ
copy in accessible accordions, unique copy per page, careful non-absolute
language — is implemented in the pages themselves.

## Pages

| # | Page | Slug |
| --- | --- | --- |
| Parent | CCTV & Security Solutions | `/cctv-security-solutions/` |
| 1 | Residential CCTV Installation | `/residential-cctv-installation/` |
| 2 | Commercial & Business CCTV Systems | `/commercial-cctv-solutions/` |
| 3 | Wireless CCTV & Smart Cameras | `/wireless-cctv-smart-cameras/` |
| 4 | Solar CCTV Camera Installation | `/solar-cctv-camera-installation/` |
| 5 | CCTV Maintenance, Repairs & Upgrades | `/cctv-maintenance-upgrades/` |
| 6 | Remote CCTV Viewing & Alerts | `/remote-cctv-viewing/` |

## 1. Residential CCTV Installation

- **URL** `/residential-cctv-installation/`
- **SEO title** Residential CCTV Installation Gauteng | CMAXX
- **Meta description** Professional residential CCTV installation for homes, estates and smallholdings across Gauteng. Coverage planning, wired, wireless and solar cameras, recording and remote viewing.
- **H1** Residential CCTV Installation for Homes and Properties in Gauteng
- **Breadcrumb** Home > Services > CCTV & Security Solutions > Residential CCTV Installation
- **Primary CTA** Book a CCTV Assessment

## 2. Commercial & Business CCTV Systems

- **URL** `/commercial-cctv-solutions/`
- **SEO title** Commercial CCTV Installation Gauteng | CMAXX
- **Meta description** Commercial CCTV systems for offices, retail, warehouses, hospitality, schools and multi-site operations across Gauteng. IP/PoE design, retention, permissions and support.
- **H1** Commercial CCTV Systems for Businesses Across Gauteng
- **Breadcrumb** Home > Services > CCTV & Security Solutions > Commercial & Business CCTV Systems
- **Primary CTA** Book a Site Assessment

## 3. Wireless CCTV & Smart Cameras

- **URL** `/wireless-cctv-smart-cameras/`
- **SEO title** Wireless CCTV & Smart Camera Installation Gauteng | CMAXX
- **Meta description** Professional Wi-Fi, battery and smart camera installation across Gauteng. Signal surveys, storage and alert configuration, account security and honest wired-versus-wireless advice.
- **H1** Wireless CCTV and Smart Camera Installation in Gauteng
- **Breadcrumb** Home > Services > CCTV & Security Solutions > Wireless CCTV & Smart Cameras
- **Primary CTA** Book a CCTV Assessment

## 4. Solar CCTV Camera Installation

- **URL** `/solar-cctv-camera-installation/`
- **SEO title** Solar CCTV Camera Installation Gauteng | CMAXX
- **Meta description** Solar and 4G/LTE CCTV camera installation for gates, farms, plots and remote areas in Gauteng. Site assessed for sunlight, signal, mounting and expected activity.
- **H1** Solar CCTV Camera Installation for Remote Areas in Gauteng
- **Breadcrumb** Home > Services > CCTV & Security Solutions > Solar CCTV Camera Installation
- **Primary CTA** Book a Site Assessment

## 5. CCTV Maintenance, Repairs & Upgrades

- **URL** `/cctv-maintenance-upgrades/`
- **SEO title** CCTV Maintenance & Repairs Gauteng | CMAXX
- **Meta description** CCTV repairs, fault finding, health checks and system upgrades across Gauteng. Offline cameras, recorder and storage faults, lost remote viewing and analogue-to-IP migration.
- **H1** CCTV Maintenance, Repairs and System Upgrades in Gauteng
- **Breadcrumb** Home > Services > CCTV & Security Solutions > CCTV Maintenance, Repairs & Upgrades
- **Primary CTA** Report a CCTV Fault

## 6. Remote CCTV Viewing & Alerts

- **URL** `/remote-cctv-viewing/`
- **SEO title** Remote CCTV Viewing Setup Gauteng | CMAXX
- **Meta description** Secure remote CCTV viewing, playback and alert setup for phone, tablet and desktop. User permissions, notification tuning, account security and remote-access troubleshooting.
- **H1** Remote CCTV Viewing, Playback and Alert Setup
- **Breadcrumb** Home > Services > CCTV & Security Solutions > Remote CCTV Viewing & Alerts
- **Primary CTA** Book a Setup Session

## Applies to every page

- Self-referencing canonical to the final live URL; index, follow; include in the
  XML sitemap and request indexing after QA.
- `Service` structured data naming CMAXX as provider, with a truthful
  `areaServed`. `BreadcrumbList` markup matching the visible breadcrumb.
- Organisation / local-business details kept consistent with the rest of the site
  and the Google Business Profile.
- No self-serving review or `aggregateRating` markup. FAQ content is published
  for users and topical depth, not for a rich result.
- Hero image not lazy-loaded, with width and height set; below-the-fold images
  lazy-loaded with reserved dimensions.
- Every `<image-slot>` placeholder in the prototype needs a real CMAXX photograph
  before launch, with a descriptive filename, factual alt text, WebP or AVIF
  compression and responsive sizes. Faces, number plates, addresses, device QR
  codes, serial numbers and sensitive camera views must be removed or blurred,
  with customer permission obtained.
- Track CTA clicks, form submissions, phone clicks and WhatsApp clicks.

## Deliberate deviation

The brief's internal-link map uses `/infrastructure-cabling/` for the cabling
page, while the existing site's page is `/structured-cabling/`. Rather than
change either, the prototype's router aliases `/infrastructure-cabling/` to the
structured cabling page so the brief's anchor text resolves. Decide on one
canonical slug before launch and redirect the other.

## Not yet published

Verified CCTV case studies. Per the brief, no placeholder projects have been
written. Each page links to `/our-work/` instead, and a proof section should be
added to the child pages once real projects, photographs and permissions exist.
