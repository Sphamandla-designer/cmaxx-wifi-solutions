# CMAXX WiFi Solutions — Phase 1 Reconstruction Source of Truth

## The rule

This document set describes **WHAT EXISTS** on the live site today.
It does not describe **WHAT SHOULD EXIST**.

Every value here was measured or transcribed from
`https://1124817.eu9.myftpupload.com`. Nothing has been redesigned, corrected,
normalised, consolidated or improved. Where the live site is inconsistent, the
inconsistency is reproduced and both variants are kept.

**When reconstructing, a difference between two pages is a specification, not a defect.**
Page `/` has hero variant A; page `/about/` has hero variant C. Build both. Do not
merge them. The Phase 2 backlog in `known-issues.md` is where consolidation gets
proposed — not here, and not during the build.

---

## The document set

| Document | Contains | Status |
| --- | --- | --- |
| `content-map.md` | All 46 pages, verbatim copy, in exact current order, with page structure outlines | Complete — 46/46 |
| `asset-map.md` | 88 image assets, 1 PDF, 6 font families, 4 icon packs | Complete — 88/88 originals retrieved |
| `component-inventory.md` | 27-widget census, chrome, component definitions, **per-page variant map** | Complete |
| `design-system.md` | Typography, colour, layout, spacing, responsive behaviour | Complete |
| `known-issues.md` | Existing defects — **Phase 2 backlog, do not fix in Phase 1** | Complete |

---

## 1. Page coverage

**46 of 46 discovered pages are mapped.**

| Page type | Count | Pages |
| --- | --- | --- |
| Home | 1 | `/` |
| Service hub | 1 | `/about/` (titled "Services") |
| Service | 7 | `/wifi-network-solutions/`, `/cctv-security-solutions/`, `/infrastructure-cabling/`, `/cloud-microsoft-365/`, `/managed-wifi/`, `/smart-home/`, `/public-guest-wifi/` |
| Industries | 1 | `/industries/` |
| Areas served | 1 | `/areas-we-serve/` |
| Case study hub | 1 | `/our-work/` |
| Case study | 3 | `/office-wifi-solutions-network-optimisation/`, `/home-wifi-optimisation-for-a-double-storey-property-in-sandton/`, `/office-wifi-upgrade-for-a-growingbusiness-in-midrand/` |
| Blog index | 1 | `/blogs-articles/` |
| Blog post | 1 | `/why-professional-wifi-installation-matters-for-homes-and-offices-in-gauteng/` |
| About | 2 | `/about-2/`, `/company-profile/` |
| Contact | 1 | `/contact/` |
| Legal | 6 | `/policy-popia/`, `/policy-popia-2/`, `/policy-popia-cmaxx/`, `/terms-conditions/`, `/cookie-policy/`, `/policy-for-public-guest-wifi/` |
| Technology brand | 18 | `/aruba/`, `/cuby/`, `/dahua/`, `/edimax/`, `/eufy/`, `/ezviz/`, `/grandstream/`, `/hilook/`, `/linkbasic/`, `/mikrotik/`, `/reyee/`, `/reyee-2/`, `/sonoff/`, `/tenda/`, `/tp-link/`, `/tp-link-tapo/`, `/ubiquiti/`, `/zte/` |
| System | 2 | `/metform-form/request-a-free-network-assessment/`, `/elementskit-content/dynamic-content-megamenu-menuitem696/` |

`/blog/` 301-redirects to `/blogs-articles/` and is not counted separately.
`/services/`, `/case-studies/` and `/privacy-policy/` return 404 and do not exist.

---

## 2. FONT SOURCE OF TRUTH

Measured on all 46 pages by reading the computed `font-family` of every visible
text-bearing element in each page body (2,189 elements sampled).

### A. Fonts actually rendered — **use these**

| Family | Rendered on | Coverage |
| --- | --- | --- |
| **Outfit** | **2,183 of 2,189 text elements, all 46 pages** | The site's typeface. Weights in use: 400, 500, 600, 700, 800, 900. |
| **Poppins** | 4 elements on 4 pages | `/`, `/industries/`, `/managed-wifi/`, `/public-guest-wifi/` |
| **Roboto** | 2 elements on 2 pages | `/about/`, `/wifi-network-solutions/` |

Poppins and Roboto each render on a handful of isolated elements. They are recorded
as rendering because they do. Reproduce them where they occur; do not spread them,
and do not remove them.

### B. Fonts loaded but not rendered

Requested from Google Fonts on every page at weights 100–900 plus italics, but no
visible text element resolves to them:

- `Roboto Slab`
- `IBM Plex Sans`
- `Work Sans`

`Roboto` is also loaded site-wide but only renders on the 2 elements above.

Also served from the origin but not used by any page body:
`font-inter.css` with `QGYvz_MVcBeNP4NJuktqUYTkntBJ2fk.woff2` and
`QGYvz_MVcBeNP4NJtEtqUYTkntBJ.woff2` — the Twenty Twenty theme's Inter.

### C. Elementor factory / default typography

The Elementor global kit (`post-8.css`) still holds unedited factory defaults:

| Token | Value |
| --- | --- |
| `--e-global-typography-primary-font-family` | `"Roboto"`, weight 600 |
| `--e-global-typography-secondary-font-family` | `"Roboto Slab"`, weight 400 |
| `--e-global-typography-text-font-family` | `"Roboto"`, weight 400 |
| `--e-global-typography-accent-font-family` | `"Roboto"`, weight 500 |

These tokens are referenced 532 times in page CSS, but every referencing widget also
sets `font-family: "Outfit"` at a higher specificity, so the kit values do not win.

**Reconstruction directive:** set Outfit as the working typeface, reproduce the 4
Poppins and 2 Roboto elements where they occur, and do not carry over Roboto Slab,
IBM Plex Sans or Work Sans.

---

## 3. COLOUR SOURCE OF TRUTH

Measured the same way — computed `color` and `background-color` of every visible
element in all 46 page bodies.

### A. Actual CMAXX colours — **use these**

| Colour | Hex | Rendered as text | Rendered as background | Token |
| --- | --- | --- | --- | --- |
| Brand dark navy | `#0E1725` | 1,181 elements / 42 pages | 108 elements / 38 pages | `--e-global-color-4a9b6d6` |
| Brand orange | `#FF6C24` | 299 elements / 42 pages | 60 elements / 34 pages | `--e-global-color-3280544` |
| White | `#FFFFFF` | 286 elements / 43 pages | 62 elements / 10 pages | — |
| Slate / muted | `#94A2B8` | 198 elements / 32 pages | — | `--e-global-color-a3173ef` |
| Near-black body | `#1F2124` | 76 elements / 18 pages | — | — |
| Black | `#000000` | 68 elements / 5 pages | `#000000/0.75` on 2 pages | — |

Alpha variants that render: `#0E1725` at 0.04 (28 elements, 14 pages),
`#FFFFFF` at 0.05 (17 elements, 13 pages) and at 0.02 (5 elements, 5 pages),
`#FF6C24` at 0.18 (8 elements, 8 pages), 0.21 and 0.15 (1 each).

### B. Elementor default colours present in the global kit

Defined in `post-8.css` as untouched factory values:

| Token | Value | Does it render? |
| --- | --- | --- |
| `--e-global-color-primary` | `#6EC1E4` | **Yes — 7 text elements on 2 pages.** Elementor's default sky blue is visible on the live site. |
| `--e-global-color-secondary` | `#54595F` | **Yes — 12 text elements on 4 pages**, plus `#54595F/0.08` as a background on 5 pages. |
| `--e-global-color-text` | `#7A7A7A` | **Yes — 15 text elements on 9 pages**, plus `#7A7A7A/0.15` (22 elements, 5 pages) and `/0.08` (4 elements, 4 pages) used for the oversized watermark numerals. |
| `--e-global-color-accent` | `#61CE70` | Only as `#61CE70/0` (fully transparent) on 1 page — never visibly green. |

These are Elementor defaults that happen to be rendering. They are part of
"what exists" and must be reproduced. Whether to keep them is a Phase 2 decision.

### C. Colours loaded but not visibly used

Declared in the stylesheets, but no visible element resolves to them:

| Colour | Where declared |
| --- | --- |
| `#FF2424` | `--e-global-color-66b6963` in the global kit |
| `#0D1427` | 60 declarations in page CSS — the second, near-duplicate navy |
| `#605BE1` | 8 declarations, including a link hover state |
| `#29D8D8`, `#27BDBD` | 4 declarations |
| `#F00` | 13 declarations |
| `#D6D6D6`, `#E8E8E8`, `#ECECEC`, `#ECEAEA`, `#E0E0E0`, `#EAEAEA` | border greys in page CSS |

Rendered but rare enough to note separately: `#E22658` (9 elements, 6 pages),
`#1E1E2F` background (15 elements, 4 pages), `#6D6D6D`, `#101010`, `#666668`,
`#FF6600`, `#FCFCFC`, `#C9C9C9`, `#F2F2F2`, `#F7F7F7`, `#211F2D`, `#25D366`
(the WhatsApp green, on the floating chat button).

**Reconstruction directive:** reproduce section A exactly, reproduce section B where
it renders, and introduce no colour that is not on this page.

---

## 4. COMPONENT SOURCE OF TRUTH

Full per-page variant tables are in `component-inventory.md` §4. Summary:

| Component | Variants live today | Kept separate? |
| --- | --- | --- |
| Header | 2 rendered rows (desktop/tablet, mobile) + 2 rows hidden on all breakpoints | Yes — build all four rows as they exist |
| Navigation | 1 desktop `wpr-nav-menu` + 1 mobile menu, one dropdown (Services) | Yes |
| Mega menu | 1 orphan ElementsKit block, not wired into the header | Yes — reproduce as an unlinked page |
| Hero | **6 variants** (A–F) across 46 pages | **Yes** |
| Section heading | eyebrow + title + optional paragraph; eyebrow colour varies (`#FF6C24` / `#94A2B8`) | Yes |
| Buttons | **12 rendered variants** — 2 radii, 2 padding scales, 6 heights | **Yes** |
| Service / industry / problem cards | `elementskit-icon-box` on 9 pages | Yes |
| Case-study cards | container + image + heading + button, `/our-work/` only | Yes |
| Technology cards | image tile linking to a brand page | Yes |
| Testimonials | **2 systems** — Trustindex (6 pages), `premium-addon-testimonials` (2 pages) | **Yes** |
| Statistics | `premium-counter` on 6 pages | Yes |
| CTA section | closing band, dark or light ground depending on page | Yes |
| Contact form | MetForm #143 on 13 pages | Yes |
| Breadcrumb | plain text on 7 pages, absent on 39 | Yes |
| Footer | 1 template, 4 link columns | Yes |

---

## 5. Layout constants

| Property | Value |
| --- | --- |
| Container max-width | 1140px desktop / 1024px ≤1024px / 767px ≤767px |
| Measured content width | 1140px at 1440px viewport, all Elementor pages |
| Tablet gutters | 900px on 9 pages, 880px on 9 pages |
| Mobile gutters | 390px on 10 pages, 370px on 7, 350px on 1 |
| Default flex gap | 20px row / 20px column |
| Breakpoints | `max-width: 767px` (43 uses), `max-width: 1024px` (4 uses) — Elementor defaults only |
| Sticky header offset | `padding-top: 90px` on the first section of most pages |

---

## 6. How to use this during reconstruction

1. **Copy is law.** Take every string from `content-map.md` exactly as written.
   `Slow Spped`, `Infra & cCable`, `GrowingBusiness`, `out specialists` and the
   Hikvision text on `/reyee/` are all correct for Phase 1.
2. **Order is law.** Build sections in the order the content map lists them,
   including the blocks the home page repeats.
3. **Assets are law.** Use the original files at the paths in `asset-map.md`.
   No substitutions, no regeneration, no renaming.
4. **Variants are law.** If two pages differ, build both. Consult
   `component-inventory.md` §4 for which page gets which variant.
5. **Do not consult `known-issues.md` for build decisions.** It exists so the
   defects are on record, and so nobody "helpfully" fixes them mid-reconstruction.

---

## 7. Verification state

| Check | Result |
| --- | --- |
| Pages discovered | 46 |
| Pages content-mapped | **46 / 46** |
| Content blocks recorded | 2,584 |
| Image assets identified | 88 |
| Original image files retrieved and measured | **88 / 88** |
| Documents retrieved | 1 / 1 (BBBEE PDF, 251 KB) |
| Fonts confirmed by computed style | 46 / 46 pages |
| Colours confirmed by computed style | 46 / 46 pages |

### Known gaps

- **No JavaScript-dependent state was captured.** Counters read `0 +`, slider tracks
  are un-initialised, accordions are closed, and the mobile burger is unopened. The
  content map records the served HTML, which is what a reconstruction starts from.
- **Hover and focus states** come from CSS declarations, not from exercised interaction.
- **The WordPress REST API is blocked by Cloudflare**, so Elementor's stored element
  settings were never readable; everything is derived from served HTML and CSS.
- **`/wp-content/uploads/premium-addons-elementor/pafe-2293.css` could not be retrieved**
  (repeated 403). It styles the Premium Addons testimonial on one case-study page.
