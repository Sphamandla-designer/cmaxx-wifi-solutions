# CMAXX WiFi Solutions — Website

The site lives in **`CMAXX Website (standalone).html`**: a single self-contained file
(open it in any browser) that holds every page and switches between them by URL hash,
e.g. `…standalone.html#/managed-wifi/`.

## Pages (26)

| Cluster | Pages |
| --- | --- |
| WiFi & Network | WiFi & Network Solutions · Home WiFi · Business & Office WiFi · WiFi Assessment & Troubleshooting · Outdoor WiFi · Event WiFi |
| Managed WiFi | **Managed WiFi** · Businesses & Offices · Restaurants & Cafes · Retail & Customer-Facing Premises · Schools & Training Facilities · Residential Estates · Event Venues & Events · Community & Public Facilities |
| Smart Home | **Smart Home Services** · Smart Lighting & Switches · Connected Entertainment · Smart Security & Access · Climate Control · Reliable Connectivity · Smart Utilities · Setup & Troubleshooting |
| Infrastructure & IT | Structured Cabling · CCTV & Security · Cloud & Microsoft 365 |
| Industries | Student Accommodation WiFi Solutions |

Every page has at most 10 sections excluding the hero and footer. All publishable copy
from the *Managed WiFi* and *Smart Home Services* developer briefs is used.

- **Parent pages** keep the overview, education, scope, process, FAQs and enquiry. Their
  card grids ("Find the right approach for your environment", "Choose what you want your
  smart home to do") link to one sub-page per card.
- **Sub-pages** hold the detail for each environment or service. Managed WiFi sector copy
  comes from brief C10–C12 and C16. Smart Home service copy comes from P04 and P07–P10,
  plus the Part 07 future-page specs for entertainment and access.
- Every sub-page has its own enquiry form. The form preselects that service or property
  type. The briefs originally kept this sector detail on the parent pages; the sub-pages
  were added at CMAXX's request.

Sub-page content and layout live in `src/subpages.py` (data plus a small renderer).

### How the pages are connected

- A site navigation bar in every page header (collapses to an "All services & pages"
  menu on phones) and a site directory in every footer.
- Contextual links and the brief section anchors (`#managed-scope`, `#ecosystems`, …),
  including cross-page deep links such as `/smart-home/#ecosystems`.
- Targeted bridge copy on the nine existing pages (Managed WiFi brief §E4,
  Smart Home brief Part 06 "links back"), added inside existing sections.
- `/infrastructure-cabling/` (the slug named in the briefs) routes to this build's
  `/structured-cabling/` page.

## Editing and rebuilding

Do not edit the standalone file by hand. Edit the sources and rebuild:

```
src/base-template.html        original 9-page template (as extracted from the bundle)
src/partials/components.css   shared cx- component styles (uses the existing design tokens)
src/partials/router.js        routing, in-page anchors, form validation, image fallback
src/pages/*.html              bodies of the five hand-written new pages
src/subpages.py               the 12 Managed WiFi / Smart Home sub-pages
tools/build_site.py           page config (titles, meta, nav), existing-page bridge copy

npm run build                 # = python3 tools/build_site.py
```

## Launch gates still open (from the briefs)

- **Enquiry forms are not connected.** Validation and all brief microcopy are in place,
  but `FORM_ENDPOINT` in `src/partials/router.js` is empty, so a valid submission tells
  the visitor it was *not* sent and offers phone/WhatsApp. Set the endpoint only once
  the recipient, storage and privacy notice are confirmed (briefs H02/H05, Part 10).
- **Email address hidden.** The live site shows conflicting addresses; no email button
  is shown until CMAXX confirms one.
- **WhatsApp** on the new pages uses the published mobile 083 212 7065 with the briefs'
  prefilled messages. The original pages still use `wa.me/27101403660` (the landline);
  confirm which is correct.
- **Images** are illustrative stock photos hot-linked from Unsplash and captioned
  "Illustrative image". Replace with approved CMAXX installation photos when available.
  If an image cannot load, a styled placeholder is shown instead.
- **Pages outside this file** (Contact, Areas We Serve, Industries hub, Public & Guest
  WiFi, Privacy Policy, Case Studies) are linked as in the briefs; in this file those
  links scroll to the current page's enquiry section. The Industries-hub (§E4.7) and
  Areas/Contact (§E4.8) amendments need those pages.

---

## Background: Phase 1 site-audit toolchain


Two-phase project.

- **Phase 1 — Reconstruction.** Rebuild the existing website faithfully so it can be
  visually inspected and approved. No redesign, no copy changes, no new sections.
- **Phase 2 — Premium UI/UX rebuild.** Begins **only** after explicit written approval
  of Phase 1.

## Current status: Phase 1 blocked on site access

The existing website cannot be reached from the Claude Code remote session. Both
hosts are refused by the organisation's network egress proxy:

| Host | Result |
| --- | --- |
| `1124817.eu9.myftpupload.com` (GoDaddy staging) | `403` at CONNECT — blocked by egress policy |
| `cmaxxsolutions.co.za` (live domain) | `403` at CONNECT — blocked by egress policy |

Egress from the session is restricted to an allowlist (package registries and
GitHub). Neither `curl` nor the fetch tooling can reach the site, so the page
inventory, content map, asset capture and visual comparison that Phase 1 depends
on cannot be produced here.

Phase 1 forbids inventing content, so no reconstruction has been written. See
"Unblocking" below.

## Unblocking

Any one of these makes Phase 1 runnable:

1. **Allowlist the hosts.** An owner adds `cmaxxsolutions.co.za` and
   `1124817.eu9.myftpupload.com` to the egress policy for this environment
   (see the Claude Code on the web docs on environments and network policy).
2. **Supply the site offline.** Run the mirror step below on any machine with
   normal internet access and commit the result, or attach a WordPress export
   (`Tools → Export → All content`) or a full-site backup archive.
3. **Run locally.** Clone this branch and run both steps on a normal network.

## Phase 1 toolchain

```bash
npm install

# 1. Mirror the live site (HTML, CSS, JS, images, fonts) into ./mirror
npm run mirror                                     # defaults to the live domain
npm run mirror -- https://1124817.eu9.myftpupload.com/   # or the staging host

# 2. Audit the mirror into ./audit
npm run audit
```

`npm run audit` writes:

| File | Contents |
| --- | --- |
| `audit/page-inventory.md` | Every page: URL, title, type, heading outline, CTA labels, form fields, SEO metadata |
| `audit/page-inventory.json` | The same data plus full body copy, links, images and section structure |
| `audit/design-system.md` | Observed typography, colours, spacing, max-widths, radii, shadows, theme tokens |
| `audit/design-system.json` | The same, machine-readable |
| `audit/assets.md` | Images with alt text and the pages using them, plus every binary in the mirror |
| `audit/known-issues.md` | Defects found in the **existing** site — Phase 2 backlog, **not** fixed in Phase 1 |

The audit tool only records. It never normalises or corrects copy, so spelling
mistakes, duplicated content and inconsistent terminology survive into the
reconstruction exactly as they appear on the live site, as Phase 1 requires.

Once `mirror/` and `audit/` exist, the reconstruction can be built against them
and compared page by page with the live site.
