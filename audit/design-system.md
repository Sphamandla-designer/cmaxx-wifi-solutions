# CMAXX WiFi Solutions — Existing Design System

**Status:** observed record of the **live site as it exists today**. Nothing here is a
recommendation, a target, or a corrected value. Where the site is internally
inconsistent, every observed variant is listed and the inconsistency is recorded in
`known-issues.md` rather than resolved here.

| | |
| --- | --- |
| Origin audited | `https://1124817.eu9.myftpupload.com` |
| Date | 21 August 2026 |
| Pages inspected | 20 representative pages covering all 14 page types |
| Method | Live crawl → local mirror (HTML + 122 stylesheets + page images) → Chromium computed styles at 1440 / 900 / 390 px |
| Builder | WordPress 7.0.4 · Elementor 4.2.3 · ElementsKit Lite 4.0.1 |

## 1. Typography

### 1.1 Font families

| Role | Family observed | Notes |
| --- | --- | --- |
| Everything visible | **Outfit** | 1,688 declarations across page CSS. The de-facto site face. |
| Elementor global "primary" | Roboto, weight 600 | Kit default, **never applied** — every widget overrides it with Outfit |
| Elementor global "secondary" | Roboto Slab, weight 400 | Kit default, unused |
| Elementor global "text" | Roboto, weight 400 | Kit default, unused |
| Elementor global "accent" | Roboto, weight 500 | Kit default, unused |
| Poppins | Poppins (×4 declarations) | **Renders** on 4 elements across 4 pages |
| IBM Plex Sans | IBM Plex Sans (×4 declarations) | Loaded; renders on no visible text element |

Google Fonts requested by the page: `Outfit`, `Poppins`, `Roboto`, `Roboto Slab`,
`IBM Plex Sans`, `Work Sans` — all at weights 100–900 plus italics.

Verified by computed style across all 46 pages (2,189 visible text elements sampled):
**Outfit renders on 2,183 elements on all 46 pages; Poppins renders on 4 elements across
4 pages** (`/`, `/industries/`, `/managed-wifi/`, `/public-guest-wifi/`); **Roboto renders
on 2 elements across 2 pages** (`/about/`, `/wifi-network-solutions/`). Roboto Slab,
IBM Plex Sans and Work Sans are loaded on every page but render on no text element.
See `reconstruction-source-of-truth.md` §2.

`body` computes to **Outfit, 18px, line-height 20.7px, colour `rgb(0,0,0)`**.

### 1.2 Font weights in use

`400` (720 declarations) · `500` (222) · `600` (288) · `700` (321) · `800` (49) · `900` (107)

### 1.3 Heading scale as rendered (desktop 1440px)

There is **no `h1` on 44 of 46 pages** (see `known-issues.md`). The visible hierarchy is
built entirely from `h2` and `h3`, with size — not tag — carrying the hierarchy.

| Rendered role | Size / weight | Line-height | Letter-spacing | Transform | Colour |
| --- | --- | --- | --- | --- | --- |
| Section title (dominant) | 40px / 900 | 48px | normal | none | `#0E1725` |
| Section title on dark | 40px / 900 | 48px | normal | none | `#FFFFFF` |
| Oversized watermark numeral | 60px / 900 | 60px | −2.49px | none | `rgba(122,122,122,.15)` |
| Watermark numeral (variant) | 70px / 900 | 70px | 5.7px | none | `rgba(122,122,122,.08)` |
| Legal-page heading | 25px / 700 | 25px | −1.04px | none | `#0E1725` |
| Card / sub-block title | 21px / 700 | 21px | −0.1px | none | `#FFFFFF` |
| Eyebrow label (orange) | 17px / 700 | 17px | −0.1px | none | `#FF6C24` |
| Eyebrow label (uppercase) | 17px / 600 | 17px | −0.71px | uppercase | `#94A2B8` |
| Small block title | 16px / 700 | 16px or 22px | −0.1px | none | `#0E1725` |
| Kicker (uppercase) | 22px / 800 | 22px | 0.7px | uppercase | `#0E1725` |
| Kicker (small, uppercase) | 15px / 600 | 15px | 1px | uppercase | `#FF6C24` |
| Feature heading (`h3`) | 19px / 700 | 24px | −0.79px | none | `#FF6C24` |
| List item heading (`h3`) | 16px / 500 | 26px | −0.1px | none | `#FFFFFF` |
| List item heading on light | 16px / 500 | 26px | −0.1px | none | `#0E1725` |
| Blog post title (`h1`, theme) | 84px / 800 | 95.7px | −3.49px | none | `#000000` |

### 1.4 Body copy as rendered

| Variant | Size / weight | Line-height | Colour | Where |
| --- | --- | --- | --- | --- |
| Default body | 18px / 400 | 27px | `#0E1725` | Service pages, legal, case studies |
| Body on dark | 15px / 400 | 22.5px | `#FFFFFF` | Dark bands |
| Muted body | 17px / 400 | 25.5px | `#94A2B8` | Managed WiFi, secondary copy |
| Muted body (small) | 16px / 400 | 24px | `#94A2B8` | Dense blocks |
| Emphasis / list label | 14px / 600 | 21px | `#FF6C24` | Feature lists |
| Elementor default grey | 18px / 400 | 27px | `#7A7A7A` | Inherited where no colour was set |

### 1.5 Metrics summary

- **Font sizes present:** 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 28, 30, 31, 33, 35, 38, 40, 47, 50, 60, 70, 84 px
- **Line-heights** are set in **px, not unitless** — 18px/19px/22px/24px/26px/29px/40px/41px/48px/52px
- **Letter-spacing:** `0.1px` (283×), `0.2px` (216×), `−0.1px` (155×), `0px` (81×), `0.3px`, `1px`, `0.6px`, `0.7px`, `1.5px`, `5.7px`
- **text-transform:** only `uppercase` is ever used (218 declarations); no `capitalize` or `lowercase`

## 2. Colours

### 2.1 Elementor global colour tokens (`post-8.css`)

| Token | Value | Status |
| --- | --- | --- |
| `--e-global-color-3280544` | **`#FF6C24`** | **Brand orange** — the primary accent, 1,352 references |
| `--e-global-color-4a9b6d6` | **`#0E1725`** | **Brand dark navy** — 1,094 references |
| `--e-global-color-a3173ef` | **`#94A2B8`** | Slate/muted — 73 references |
| `--e-global-color-66b6963` | `#FF2424` | Red — defined, effectively unused |
| `--e-global-color-7bedddd` | `#0E17250A` | Navy at 4% alpha — 1 reference |
| `--e-global-color-primary` | `#6EC1E4` | Elementor factory default — **and it renders**: 7 text elements on 2 pages |
| `--e-global-color-secondary` | `#54595F` | Elementor factory default — **renders** on 12 text elements / 4 pages, plus `/0.08` backgrounds on 5 pages |
| `--e-global-color-text` | `#7A7A7A` | Elementor factory default — **renders** on 15 text elements / 9 pages, and at `/0.15` and `/0.08` for the watermark numerals |
| `--e-global-color-accent` | `#61CE70` | Elementor factory default green — appears only at `/0` (fully transparent); never visibly green |

### 2.2 Colours as actually used

| Role | Value | Evidence |
| --- | --- | --- |
| Primary brand / accent | `#FF6C24` (orange) | Buttons, eyebrows, feature headings, icons, hover state |
| Secondary brand | `#0E1725` (dark navy) | Dark section grounds, headings |
| Near-duplicate navy | `#0D1427` | 60 declarations — a second, slightly different dark navy |
| Muted text / slate | `#94A2B8` | Secondary copy, uppercase eyebrows |
| Inherited body grey | `#7A7A7A` | Elementor default, appears in rendered body text |
| Page background | `#FFFFFF` | 313 declarations |
| Dark band background | `#0E1725` / `#0D1427` | Alternating dark sections |
| Body/base text | `#000000` (body default) / `#0E1725` (set) | 117 declarations of `#000000` |
| Borders (light) | `#D6D6D6`, `#E8E8E8`, `#ECECEC`, `#ECEAEA`, `#E0E0E0`, `#EAEAEA` | Six near-identical greys |
| Card surface | `#FFFFFF`, `#F7F7F7`, `#F2F2F2`, `#FCFCFC`, `#F6F7FA` | |
| Stray purple | `#605BE1` | 8 declarations, incl. a link hover |
| Stray teal | `#29D8D8`, `#27BDBD` | 4 declarations |
| Stray red | `#F00` | 13 declarations |
| Alt dark | `#1E1E2F` | 15 declarations |

### 2.3 Buttons — every rendered variant (desktop)

| Count | Background | Text | Radius | Padding | Border | Height |
| --- | --- | --- | --- | --- | --- | --- |
| 32 | `#FF6C24` | `#FFFFFF` | 6px | 16px 36px | none | 47px |
| 20 | `#FF6C24` | `#FFFFFF` | **3px** | **12px 24px** | none | **39px** |
| 12 | `rgba(255,255,255,.05)` | `#FFFFFF` | 6px | 16px 36px | none | 47px |
| 6 | `rgba(255,108,36,.18)` | `#FF6C24` | 6px | 16px 36px | none | 48px |
| 5 | transparent | `#FF6C24` | 3px | 12px 24px | none | 39px |
| 5 | `rgba(255,255,255,.02)` | `#FFFFFF` | 6px | 16px 36px | none | 48px |
| 4 | `#FF6C24` | `#FFFFFF` | 6px | 16px 36px | **2px `#FF6C24`** | 52px |
| 4 | `rgba(255,255,255,.05)` | `#FF6C24` | 6px | 16px 36px | 2px `#FF6C24` | 51px |
| 2 | `#FF6C24` | `#FFFFFF` | 6px | 16px 36px | 2px `#FF6C24` | 51px |
| 1 | `#FF6C24` | `#FFFFFF` | 6px | 16px 36px | none | 48px |
| 1 | `#F7F7F7` | `#0E1725` | 6px | 16px 36px | none | 47px |
| 1 | `rgba(255,108,36,.18)` | `#FCFCFC` | 6px | 16px 36px | none | 48px |

All buttons render at **15px**; weight `500` except the transparent text variant at `700`.

### 2.4 Hover states

| Declaration | Count |
| --- | --- |
| `color: #FF6C24` | 70 |
| `color: #000000` | 25 |
| `background-color: #000000` | 16 |
| `background-color: #FF6C2412` (7% orange) | 10 |
| `background-color: #522A2A00` (transparent) | 6 |
| `color: #FFFFFF` | 6 |
| `color: #605BE1` | 4 |

Transitions: `color 0.3s` (178×), `fill 0.3s` (89×), `0.3s` (35×), `0.1s` (15×), `1.9s` (16×).

## 3. Layout

### 3.1 Containers

Declared in the Elementor kit:

| Breakpoint | `--container-max-width` |
| --- | --- |
| Desktop | **1140px** |
| ≤1024px | 1024px |
| ≤767px | 767px |

Measured inner content width:

| Viewport | Observed | Note |
| --- | --- | --- |
| 1440px | **1140px** on every Elementor page | consistent |
| 900px | **900px** (9 pages) / **880px** (9 pages) | two gutter treatments |
| 390px | **390px** (10) / **370px** (7) / **350px** (1) | three gutter treatments |

Gutters are therefore **0 / 10 / 20px per side depending on the page**, not a single rule.

### 3.2 Section spacing

- Top-level section wrappers carry **no padding** (`0/0`); vertical rhythm sits on inner containers.
- Inner container padding observed: `16px 36px` (96×), `20px` all round (92×), `40px 34px 30px 34px` (76×), `0 20px` (39×), `15px 24px 17px 24px` (20×), `10px` (19×), `14px 28px` (3×), `15px` (5×).
- The first section on most pages carries `padding-top: 90px` — the sticky-header offset.
- Repeating inner row padding is `10px` top and bottom on most content rows.

### 3.3 Grid & columns

- Elementor **flex containers** (`.e-con`), not a numeric grid system.
- Default gap: **`20px` row / `20px` column** (89 of 115 inner containers). Also `0`, `0/10px`, `0/18px`.
- Column widths are set as explicit percentages per element:
  **50%** (46×) · **33.33%** (17×) · **32%** (21×) · **30%** (35×) · **25%** (16×) · **20%** (22×) · **66.67%** (12×)
- Also hand-dragged, non-round values: **11.286%** (52×), **96.57%**, **40.541%**, **52.332%**, **47.285%**, **93.302%**, **100.656%**
- Fixed pixel widths appear on cards: `329.188px` (149×), `322.062px` (18×), `303.203px` (17×)
- Legacy sections use `elementor-col-50` (94×) — the only legacy column class still present.

### 3.4 Border radius

`6px` (98×) · `0` (86×) · `08px` (77×) · `8px` (62×) · `20px` (61×) · `10px` (53×) · `15px` (41×) · `16px` (40×) · `0 0 10px 10px` (17×) · `16px 16px 0 0` (14×) · `16px 0 0 16px` (8×) · `5px !important` (6×) · `14px` (5×)

`08px` is written with a leading zero; it computes to `8px`.

### 3.5 Shadows

| Shadow | Count |
| --- | --- |
| `0 0 10px 0 rgba(0,0,0,0.06)` | 35 |
| `0 0 10px 0 rgba(0,0,0,0.04)` | 35 |
| `0 0 20px 1px rgba(0,0,0,0.1)` | 3 |
| `0 0 10px 0 rgba(0,0,0,0.05)` | 2 |
| `0 10px 10px 0 rgba(0,0,0,0.14)` | 1 |
| `0 2px 4px 0 rgba(3,28,90,0.4)` | 1 |
| `0 19px 26px 1px rgba(255,255,255,0.02)` | 1 |

All shadows are ambient (no y-offset) except the last three.

### 3.6 Images

- `object-fit: fill`, `border-radius: 0`, `max-width: 100%` on content images.
- Images scale proportionally down to mobile (e.g. `411×457` → `370×412`, aspect ratio held at 0.90).
- No `srcset` art direction observed on Elementor image widgets; WordPress size suffixes (`-300x300`, `-1024x559`) are used instead.

### 3.7 Alignment

- Content is centred in a `1140px` column; hero rows are two-column (text left, image right).
- Section headings are centre-aligned on marketing pages, left-aligned on legal and case-study pages.

## 4. Responsive behaviour

### 4.1 Breakpoints

Only Elementor's defaults are used — **no custom breakpoints**:

| Query | Count |
| --- | --- |
| `@media (max-width: 767px)` | 43 |
| `@media (min-width: 768px)` | 42 |
| `@media (max-width: 1024px)` | 4 |
| `@media (min-width: 1025px)` | 4 |

### 4.2 Navigation

The header template (`624`) contains **four top-level rows**:

| Row | Visibility | Contents |
| --- | --- | --- |
| 1 | hidden on desktop **and** tablet **and** mobile | contact icon-list — never rendered |
| 2 | hidden on desktop **and** tablet **and** mobile | social icons + contact list — never rendered |
| 3 | hidden on mobile; **sticky** | contact strip, logo, search, "Get in Touch" button, `wpr-nav-menu`, social |
| 4 | hidden on desktop **and** tablet; **sticky** | logo, search, `wpr-nav-menu` |

So desktop/tablet and mobile are served by **two separate header implementations**, and two
rows are dead markup. Stickiness comes from `wpr-sticky-section-yes` plus
`uicore_onscroll_effect: simple-sticky`.

The Services dropdown is a standard `wpr-nav-menu` sub-menu with a fade effect
(`wpr-sub-menu-fx-fade`), opened on hover (`data-trigger="hover"`). Mobile uses
`wpr-mobile-nav-menu-container` with `wpr-mobile-menu-item` / `wpr-mobile-sub-menu-item`.

The `elementskit_content` mega-menu block (`dynamic-content-megamenu-menuitem696`) exists as
a published item but is not wired into the rendered header.

### 4.3 Typography across breakpoints

**Tablet typography is byte-identical to desktop on every page inspected.** There is no
tablet type scale. Mobile reductions are set per page, with no shared rule:

| Page | Desktop h2 | Tablet h2 | Mobile h2 |
| --- | --- | --- | --- |
| Home | 40px/900 | 40px/900 | **16px/700** |
| Service hub | 40px/900 | 40px/900 | 33px/900 |
| WiFi & Network | 40px/900 | 40px/900 | **40px/900 (no change)** |
| Smart Home | 40px/900 | 40px/900 | 30px/900 |
| Public & Guest WiFi | 40px/900 | 40px/900 | **16px/700** |
| Industries / Areas / Cases / Contact / Company Profile | 40px/900 | 40px/900 | 30px/900 |
| About | 40px/900 | 40px/900 | **21px/700** |
| Blog index | 40px/700 | 40px/700 | 30px/700 |

Body copy likewise changes only at mobile, and inconsistently — some pages step **up**
(15px → 18px on Areas, Contact, Cabling), others hold, others step down.

### 4.4 Columns, cards and CTAs

- Columns are percentage-based flex children; at `≤767px` Elementor stacks them to full width.
- Card fixed widths (`329.188px`, `322.062px`, `303.203px`) are desktop-only; cards go fluid at mobile.
- Container gutters change per page (§3.1), so card edges do not align consistently across pages at the same viewport.
- CTA buttons keep `15px` type at every breakpoint; only padding/width change.

## 5. Third-party visual dependencies

| Plugin | Visual role |
| --- | --- |
| ElementsKit Lite | Header/footer templates, icon-box cards, header search, social icons, accordion |
| Royal Elementor Addons | `wpr-nav-menu`, sticky header, posts timeline |
| Essential Addons (EAEL) | `eael-fancy-text` animated headline (13 pages), `eael-post-grid` (blog) |
| Premium Addons | `premium-counter` statistics (6 pages), `premium-addon-testimonials` (2 case studies) |
| Trustindex | Google-review testimonial sliders (6 pages) |
| MetForm | Form #143 |
| Slider Text Scroll / uicore-animate / the-preloader | Scroll effects, preloader |
