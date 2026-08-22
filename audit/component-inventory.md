# CMAXX WiFi Solutions — Existing Component Inventory

Observed record of the components the **live site uses today**. Counts are occurrences of
the underlying Elementor widget across all 46 live pages.

## 1. Widget census

| Widget | Uses | Rendered as |
| --- | --- | --- |
| `text-editor` | 916 | Body copy, eyebrows, stat labels, most "headings" that aren't heading tags |
| `heading` | 469 | Section titles, card titles |
| `icon-list` | 372 | Feature/benefit bullet lists, contact lists |
| `elementskit-heading` | 282 | Footer column titles, decorated headings |
| `image` | 235 | Photos, logos, technology brand marks |
| `icon` | 198 | Inline glyphs beside contact details and list items |
| `button` | 149 | All CTAs |
| `wpr-nav-menu` | 94 | Header navigation (desktop + mobile instances) |
| `elementskit-header-search` | 94 | Header search toggle |
| `elementskit-icon-box` | 76 | Service / industry / feature cards |
| `mf-text` | 56 | MetForm text inputs |
| `social-icons` | 47 | Header/footer social |
| `elementskit-social-media` | 47 | Header/footer social (second implementation) |
| `nested-accordion` | 23 | FAQ blocks |
| `eael-fancy-text` | 23 | Animated hero headline |
| `premium-counter` | 21 | Statistics counters |
| `mf-textarea` | 14 | Form message field |
| `mf-recaptcha` | 14 | Form captcha |
| `mf-button` | 14 | Form submit |
| `metform` | 13 | Form embed wrapper |
| `shortcode` | 7 | Trustindex review sliders |
| `wpr-posts-timeline` | 3 | Process/timeline blocks |
| `eael-post-grid` | 3 | Blog listing |
| `premium-addon-testimonials` | 2 | Case-study testimonials |
| `google_maps` | 2 | Contact + Areas We Serve maps |
| `nested-tabs` | 1 | Smart Home tabbed block |
| `image-carousel` | 1 | Our Work gallery |

**27 distinct widget types.**

## 2. Global chrome

### 2.1 Header — Elementor template `624`

Four top-level rows; two never render (see `known-issues.md`).

| Row | Visible on | Sticky | Contents |
| --- | --- | --- | --- |
| 1 | *nothing* | no | icon-list (email, phone) |
| 2 | *nothing* | no | social-icons + icon-list |
| 3 | desktop, tablet | yes | contact strip (phone / WhatsApp / email / location) → logo, header search, "Get in Touch" button, `wpr-nav-menu`, social |
| 4 | mobile | yes | logo, header search, `wpr-nav-menu` (burger) |

- **Logo:** image widget linking to `/`
- **Search:** `ekit-search-group`, `GET ?s=`, placeholder "Search..."
- **Primary CTA:** "Get in Touch" → `/contact/`, orange, 3px radius, 12/24 padding, 39px tall
- **Modals:** two ElementsKit popups (`ekit_modal-popup-11929540`, `ekit_modal-popup-80198e2`)

### 2.2 Navigation

- Component: `wpr-nav-menu`, horizontal, `data-trigger="hover"`, `wpr-sub-menu-fx-fade`
- 15 menu items, one with children (`menu-item-has-children`)
- **Dropdown:** Services → 7 service pages
- **Mobile:** `wpr-mobile-nav-menu-container` with `wpr-mobile-menu-item` / `wpr-mobile-sub-menu-item`
- **Active state:** `current-menu-item` / `wpr-active-menu-item`
- A separate ElementsKit mega-menu content block exists but is not wired into the header

### 2.3 Footer — Elementor template `659`

Single row, four link columns plus a brand block:

| Block | Contents |
| --- | --- |
| Brand | Logo + one-line descriptor |
| Core Services | 7 service links |
| Our Company | About, Case Studies, Blogs, Areas, Industries, Company Profile |
| Legal & Policies | POPIA, T&Cs, **BBBEE Certificate (PDF)**, Cookies, Public & Guest Policy |
| Contact Us | WhatsApp, phone, email, location, Google Profile, LinkedIn |

Column titles use `elementskit-heading`. Credit line: "© 2026 Cmaxx Wifi Solutions.
All Rights Reserved. Designed by AX-Channels".

## 3. Page-level components

### 3.1 Hero

Not one component — **five distinct hero patterns**:

| Pattern | Widgets | Pages |
| --- | --- | --- |
| A — Split hero with image | `text-editor` + `eael-fancy-text` + `text-editor` + `icon-list` + 2× `button` + `image` | Home |
| B — Centred text hero | `eael-fancy-text` + `text-editor` + `button`(s) | Service hub, service pages, cases hub, contact |
| C — Eyebrow + title + CTA | `text-editor` (eyebrow) + `eael-fancy-text` + `text-editor` + `button` | Industries, About |
| D — Plain heading | `heading` only | Legal pages |
| E — Project header | 2× `heading` + `text-editor` + `icon-list` | Case studies |
| F — Image only | `image` | Technology brand pages |

`eael-fancy-text` (animated typing/rotating headline) carries the main headline on 13 pages.

### 3.2 Breadcrumb

`HOME | PAGE NAME`, rendered as plain text (not a widget, not schema markup).
Present on **6 of 46 pages only**: Areas We Serve, Cookie Policy, Public & Guest Policy,
POPIA ×3, Terms & Conditions.

### 3.3 Section heading block

Recurring pattern: uppercase eyebrow (`text-editor` or `h2` at 15–17px, orange or slate)
→ section title (`h2`, 40px/900) → optional supporting paragraph.

### 3.4 Cards

| Card | Component | Where | Spec |
| --- | --- | --- | --- |
| Service card | `elementskit-icon-box` (`.elementskit-infobox`) | Home, service hub | icon + `elementskit-info-box-title` + copy + "Explore Service" |
| Industry card | `elementskit-icon-box` | Industries | icon + title + copy |
| Technology card | `image` + link | Home, service pages, About, Company Profile | brand logo tile linking to a brand page |
| Case-study card | container + `image` + `heading` + `button` | Our Work | "View Case Studies" CTA |
| Blog card | `eael-post-grid` | Blog index, Home | thumbnail + title + "Read More" |
| Problem card | `elementskit-icon-box` | Home, service pages | "Dead Zone", "Slow Speed", etc. |

Card widths are fixed pixels on desktop (`329.188px`, `322.062px`, `303.203px`) and fluid at
mobile. Radii vary by card family (6 / 8 / 10 / 15 / 16 / 20px).

### 3.5 Buttons

Twelve rendered variants (full table in `design-system.md` §2.3). Functionally:

| Variant | Style | Typical labels |
| --- | --- | --- |
| Primary solid | `#FF6C24` / white, 6px, 16×36 | "Request a Free Assessment", "Get a Free Assessment" |
| Primary compact | `#FF6C24` / white, **3px, 12×24** | "Get in Touch" (header) |
| Ghost on dark | `rgba(255,255,255,.05)` / white | "Call Us Now" |
| Tinted | `rgba(255,108,36,.18)` / orange | "WhatsApp Us" |
| Outlined | 2px `#FF6C24` border | "Call Us Now" (light sections) |
| Text-only | transparent / orange, weight 700 | "Explore Service" |
| Light | `#F7F7F7` / navy | "Book a Guest WiFi Consultation" |
| Scroll cue | `rgba(255,255,255,.02)` | "Scroll Down" |

**33 distinct CTA labels** sitewide.

### 3.6 Statistics

`premium-counter` on 6 pages (Home, CCTV, Cloud, Cabling, Our Work, WiFi & Network).
Structure: `premium-counter-value-wrap` (animated number) + `premium-counter-title`.
Rendered as `0 +` until the JS counter runs. Examples: "9+ Years", "100+ Projects",
"↑ % Avg coverage increase", "0/7 Remote monitoring".

### 3.7 Testimonials

Two separate implementations:
- **Trustindex** review slider via `shortcode` — 6 pages, under "What Our Clients are Saying"
- **`premium-addon-testimonials`** — 2 case-study pages only

### 3.8 CTA sections

Closing band on most marketing pages: title + supporting line + 2–3 buttons
(assessment / call / WhatsApp). Appears on dark navy or white ground depending on page.

### 3.9 Forms

Single form sitewide — **MetForm #143 "Request a Free Network Assessment"**, embedded on
13 pages, AJAX-rendered (no `<form>` in served HTML).

| Field | Widget | Label | Placeholder |
| --- | --- | --- | --- |
| `mf-Your-name` | `mf-text` | Full Name | Your Name |
| — | `mf-text` | Phone Number | +27..... |
| `mf-email` | `mf-text` | Email Address | Enter your Email |
| — | `mf-text` | Service Required | How can we help you |
| `mf-comment` | `mf-textarea` | Message | Tell about your network challenge |
| — | `mf-recaptcha` | — | reCAPTCHA |
| — | `mf-button` | **Send Message** | — |

Plus the header **search form** (`ekit-search-group`, `GET ?s=`).

### 3.10 Accordion / FAQ

`nested-accordion` on 22 pages — all 18 technology brand pages plus Company Profile,
Managed WiFi, Public & Guest WiFi and Smart Home. On brand pages the recurring outline is
Brand Overview → Ideal Use Cases → Why CMAXX May Recommend This Brand → FAQs →
Professional recommendation.

### 3.11 Timeline / process

`wpr-posts-timeline` on Company Profile, Industries, Smart Home. Numbered process steps
(`01 Assessment & Survey` → `04 Handover & Training`) appear on service pages as
`heading` + `text-editor` pairs rather than a timeline widget.

### 3.12 Maps

`google_maps` widget on **Contact** and **Areas We Serve**.

### 3.13 Other recurring patterns

- **Technology logo strip** — "Trusted Technologies We Install & Support", repeated on Home, WiFi & Network, About, Company Profile
- **Watermark numerals** — oversized `h2` at 60–70px/900 in `rgba(122,122,122,.08–.15)` behind process steps
- **Floating WhatsApp button** — Click to Chat plugin, all pages
- **Preloader** — `the-preloader` plugin, all pages
- **Scroll cue** — "Scroll Down" button in hero on 6 pages

---

## 4. Component variant map — which page has which variant

**Variants are preserved as separate variants. Nothing here is consolidated.**

### 4.1 Hero variant per page

| Page | Hero variant |
| --- | --- |
| `/` | A — split hero w/ image |
| `/about-2/` | B — centred animated headline |
| `/about/` | B — centred animated headline |
| `/cctv-security-solutions/` | B — centred animated headline |
| `/cloud-microsoft-365/` | B — centred animated headline |
| `/contact/` | B — centred animated headline |
| `/industries/` | B — centred animated headline |
| `/infrastructure-cabling/` | B — centred animated headline |
| `/managed-wifi/` | B — centred animated headline |
| `/our-work/` | B — centred animated headline |
| `/public-guest-wifi/` | B — centred animated headline |
| `/smart-home/` | B — centred animated headline |
| `/wifi-network-solutions/` | B — centred animated headline |
| `/company-profile/` | C — eyebrow + headline |
| `/cookie-policy/` | C — eyebrow + headline |
| `/policy-for-public-guest-wifi/` | C — eyebrow + headline |
| `/policy-popia-2/` | C — eyebrow + headline |
| `/policy-popia-cmaxx/` | C — eyebrow + headline |
| `/policy-popia/` | C — eyebrow + headline |
| `/terms-conditions/` | C — eyebrow + headline |
| `/areas-we-serve/` | D — plain heading |
| `/blogs-articles/` | D — plain heading |
| `/elementskit-content/dynamic-content-megamenu-menuitem696/` | D — plain heading |
| `/home-wifi-optimisation-for-a-double-storey-property-in-sandton/` | D — plain heading |
| `/office-wifi-solutions-network-optimisation/` | D — plain heading |
| `/aruba/` | E — image only |
| `/cuby/` | E — image only |
| `/dahua/` | E — image only |
| `/edimax/` | E — image only |
| `/eufy/` | E — image only |
| `/ezviz/` | E — image only |
| `/grandstream/` | E — image only |
| `/hilook/` | E — image only |
| `/linkbasic/` | E — image only |
| `/mikrotik/` | E — image only |
| `/reyee-2/` | E — image only |
| `/reyee/` | E — image only |
| `/sonoff/` | E — image only |
| `/tenda/` | E — image only |
| `/tp-link-tapo/` | E — image only |
| `/tp-link/` | E — image only |
| `/ubiquiti/` | E — image only |
| `/zte/` | E — image only |
| `/metform-form/request-a-free-network-assessment/` | F — theme template (no Elementor hero) |
| `/office-wifi-upgrade-for-a-growingbusiness-in-midrand/` | F — theme template (no Elementor hero) |
| `/why-professional-wifi-installation-matters-for-homes-and-offices-in-gauteng/` | F — theme template (no Elementor hero) |

**Variant differences**

| Variant | Pages | What differs |
| --- | --- | --- |
| A — split hero w/ image | 1 | Two-column: eyebrow, animated headline, paragraph, 3-item icon-list, two buttons, image on the right. Only the home page uses this. |
| B — centred animated headline | 12 | Single centred column: animated headline, paragraph, one or two buttons. No image, no icon-list. |
| C — eyebrow + headline | 7 | Adds an uppercase eyebrow paragraph above the animated headline; otherwise like B. |
| D — plain heading | 5 | A single `<h2>` heading widget, no animated headline, no button, no image. |
| E — image only | 18 | A lone image widget opens the page body — used by every technology brand page. |
| F — theme template (no Elementor hero) | 3 | No Elementor container at all; the WordPress theme renders an `<h1>` entry title and a byline. |

### 4.2 Breadcrumb (`HOME | PAGE NAME`, plain text)

Present on 7 of 46 pages. The other 39 pages have no breadcrumb.

| Page | Instances |
| --- | --- |
| `/areas-we-serve/` | present |
| `/cookie-policy/` | present |
| `/policy-for-public-guest-wifi/` | present |
| `/policy-popia-2/` | present |
| `/policy-popia-cmaxx/` | present |
| `/policy-popia/` | present |
| `/terms-conditions/` | present |

### 4.3 ElementsKit icon-box cards (service / industry / problem cards)

| Page | Instances |
| --- | --- |
| `/` | 19 |
| `/about-2/` | 16 |
| `/public-guest-wifi/` | 12 |
| `/industries/` | 7 |
| `/managed-wifi/` | 6 |
| `/cctv-security-solutions/` | 4 |
| `/company-profile/` | 4 |
| `/infrastructure-cabling/` | 4 |
| `/wifi-network-solutions/` | 4 |

### 4.4 Statistics — `premium-counter`

| Page | Instances |
| --- | --- |
| `/` | 4 |
| `/cctv-security-solutions/` | 3 |
| `/cloud-microsoft-365/` | 3 |
| `/infrastructure-cabling/` | 3 |
| `/our-work/` | 4 |
| `/wifi-network-solutions/` | 4 |

### 4.5 Testimonials — Trustindex shortcode

**Variant 1 of 2.** Google-review slider injected by shortcode.

| Page | Instances |
| --- | --- |
| `/` | Trustindex slider |
| `/cctv-security-solutions/` | Trustindex slider |
| `/cloud-microsoft-365/` | Trustindex slider |
| `/infrastructure-cabling/` | Trustindex slider |
| `/our-work/` | Trustindex slider |
| `/wifi-network-solutions/` | Trustindex slider |

### 4.6 Testimonials — `premium-addon-testimonials`

**Variant 2 of 2.** A different widget with different markup and styling. Both variants are kept separate for Phase 1.

| Page | Instances |
| --- | --- |
| `/home-wifi-optimisation-for-a-double-storey-property-in-sandton/` | 1 |
| `/office-wifi-solutions-network-optimisation/` | 1 |

### 4.7 Contact form — MetForm #143

One form, embedded on 13 pages. AJAX-rendered — no `<form>` element in the served HTML.

| Page | Instances |
| --- | --- |
| `/` | embedded |
| `/blogs-articles/` | embedded |
| `/contact/` | embedded |
| `/cookie-policy/` | embedded |
| `/industries/` | embedded |
| `/infrastructure-cabling/` | embedded |
| `/metform-form/request-a-free-network-assessment/` | embedded |
| `/policy-for-public-guest-wifi/` | embedded |
| `/policy-popia-2/` | embedded |
| `/policy-popia-cmaxx/` | embedded |
| `/policy-popia/` | embedded |
| `/terms-conditions/` | embedded |
| `/wifi-network-solutions/` | embedded |

### 4.8 Accordion — `nested-accordion`

| Page | Instances |
| --- | --- |
| `/aruba/` | 1 |
| `/company-profile/` | 1 |
| `/cuby/` | 1 |
| `/dahua/` | 1 |
| `/edimax/` | 1 |
| `/eufy/` | 1 |
| `/ezviz/` | 1 |
| `/grandstream/` | 1 |
| `/hilook/` | 1 |
| `/linkbasic/` | 1 |
| `/managed-wifi/` | 1 |
| `/mikrotik/` | 1 |
| `/public-guest-wifi/` | 2 |
| `/reyee-2/` | 1 |
| `/reyee/` | 1 |
| `/smart-home/` | 1 |
| `/sonoff/` | 1 |
| `/tenda/` | 1 |
| `/tp-link-tapo/` | 1 |
| `/tp-link/` | 1 |
| `/ubiquiti/` | 1 |
| `/zte/` | 1 |

### 4.9 Google Maps embed

| Page | Instances |
| --- | --- |
| `/areas-we-serve/` | map |
| `/contact/` | map |

### 4.10 Blog listing — `eael-post-grid`

| Page | Instances |
| --- | --- |
| `/` | post grid |
| `/blogs-articles/` | post grid |

### 4.11 Timeline — `wpr-posts-timeline`

| Page | Instances |
| --- | --- |
| `/company-profile/` | timeline |
| `/industries/` | timeline |
| `/smart-home/` | timeline |

### 4.12 Image carousel / tabs (single-use components)

| Page | Instances |
| --- | --- |
| `/our-work/` | image-carousel |
| `/smart-home/` | nested-tabs |

### 4.13 Animated headline — `eael-fancy-text`

| Page | Instances |
| --- | --- |
| `/` | animated headline |
| `/about-2/` | animated headline |
| `/about/` | animated headline |
| `/cctv-security-solutions/` | animated headline |
| `/cloud-microsoft-365/` | animated headline |
| `/company-profile/` | animated headline |
| `/contact/` | animated headline |
| `/industries/` | animated headline |
| `/infrastructure-cabling/` | animated headline |
| `/managed-wifi/` | animated headline |
| `/our-work/` | animated headline |
| `/public-guest-wifi/` | animated headline |
| `/smart-home/` | animated headline |
| `/wifi-network-solutions/` | animated headline |