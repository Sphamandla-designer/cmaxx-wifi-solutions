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
