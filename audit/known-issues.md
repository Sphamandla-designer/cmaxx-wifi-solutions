# CMAXX WiFi Solutions — Known Issues in the Existing Site

Defects and inconsistencies observed on the **live site**. This is a Phase 2 backlog.
**Nothing in this list has been fixed**, and nothing here was corrected in the audit
documents — `design-system.md` and `component-inventory.md` record the site as it is.

Severity is an observation of impact, not a schedule.

---

## A. Structural / semantic

### A1 — 44 of 46 pages have no `<h1>` · High
Only 10 `<h1>` tags exist across the whole site, and 8 of those are on 404 pages or
Cloudflare block pages. The only content pages with a real `<h1>` are the blog post and
`/office-wifi-upgrade-for-a-growingbusiness-in-midrand/` — the two pages that use the
theme template rather than Elementor. Every Elementor page builds its hierarchy from
`h2`/`h3` only.

### A2 — `h2` spans 15px to 70px · High
The `h2` tag is used for eyebrow labels (15px), small block titles (16px), section titles
(40px) and decorative watermark numerals (60–70px). Tag level carries no hierarchy.

### A3 — Breadcrumbs on 6 of 46 pages · Medium
`HOME | PAGE NAME` appears on Areas We Serve, Cookie Policy, Public & Guest Policy, the
three POPIA pages and Terms & Conditions. It is plain text, not a widget, and has no
schema markup. The other 40 pages have no breadcrumb.

### A4 — Two pages bypass the Elementor template entirely · Medium
The blog post and one case study render through the WordPress theme template, producing a
completely different layout, an 84px `h1`, and a "Post author / Post date" byline
(`By 1003642pwpadmin`) that appears nowhere else.

---

## B. Typography

### B1 — Global typography tokens unused · Medium
The Elementor kit defines Roboto / Roboto Slab as the global type system. Every widget
overrides it with **Outfit**, set per element. The site loads all weights and italics of
Roboto and Roboto Slab on every page for nothing.

### B2 — 23 font sizes in use · High
14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 28, 30, 31, 33, 35, 38, 40, 47, 50, 60, 70, 84 px.
There is no type scale; sizes were set per element.

### B3 — Line-heights set in pixels · Medium
All line-heights are absolute (`26px`, `29px`, `48px`…), so text does not reflow
proportionally when a size is changed at a breakpoint.

### B4 — Ten different letter-spacing values · Low
`0.1px`, `0.2px`, `−0.1px`, `0px`, `0.3px`, `0.6px`, `0.7px`, `1px`, `1.5px`, `5.7px`,
plus computed values such as `−0.789688px` and `−2.49375px` from percentage tracking.

### B5 — Body copy inherits Elementor's default grey · Medium
Rendered body text frequently computes to `#7A7A7A` — the untouched
`--e-global-color-text` default — rather than a brand colour.

### B6 — Stray typefaces · Low
Poppins (×4) and IBM Plex Sans (×4) declarations survive in page CSS.

---

## C. Colour

### C1 — Four Elementor factory colours still in the kit · Medium
`--e-global-color-primary: #6EC1E4`, `secondary: #54595F`, `text: #7A7A7A`,
`accent: #61CE70` are unedited defaults. The real brand colours live in unnamed custom
slots (`3280544`, `4a9b6d6`, `a3173ef`), so the palette is not self-describing.

### C2 — Two near-identical dark navies · Medium
`#0E1725` (the token, 1,094 uses) and `#0D1427` (60 uses) are both in play.

### C3 — Six near-identical border greys · Low
`#D6D6D6`, `#E8E8E8`, `#ECECEC`, `#ECEAEA`, `#E0E0E0`, `#EAEAEA`.

### C4 — Off-brand colours in the stylesheet · Low
Purple `#605BE1` (8 uses, including a link hover), teal `#29D8D8` / `#27BDBD` (4),
red `#F00` (13), alt dark `#1E1E2F` (15).

### C5 — A malformed shadow colour · Low
`rgba(2.9999999999999996, 28.00000000000002, 90, 0.4)` — floating-point residue from the
editor.

---

## D. Components

### D1 — Twelve button variants · High
Two radii (**3px** and **6px**), two padding scales (**12×24** and **16×36**), and six
rendered heights (**39, 47, 48, 51, 52, 53px**). The same label gets different treatment
on different pages — "Call Us Now" appears as a ghost button, an outlined button and a
solid button.

### D2 — 33 CTA labels for roughly four actions · High
"Get a Free Assessment", "Request a Free Assessment", "Book Free Assessment",
"Request a Free Network Assessment", "Request Network Assessment", "Book a Free Home WiFi
Assessment", "Request Home Assessment", "Get Free Security Assessment",
"Book A Free Connectivity Assessment" — nine phrasings of one action. Likewise
"Call Us Now" / "Call Us Today" / "Call Us Directly" / "Call 010 140 3660", and
"Explore Service" / "Learn More" / "View Case Studies".

### D3 — Two social-icon implementations · Low
`social-icons` (47) and `elementskit-social-media` (47) are both used in the same chrome.

### D4 — Two testimonial systems · Medium
Trustindex sliders on 6 marketing pages; `premium-addon-testimonials` on 2 case studies.
Different markup, different visual treatment.

### D5 — Six hero patterns · Medium
No shared hero component; each page type opens differently (see
`component-inventory.md` §3.1).

### D6 — Duplicated "Why Choose CMAXX" block on the home page · Medium
The home page renders the same content block twice: "Public / Guest WiFi Portals with
Advanced Analytics & Reporting", "BBBEE Level 1 Certified", "9+ Years Industry
Experience", "100+ Projects Completed" and the four "Why Gauteng Businesses… Trust CMAXX"
items all appear a second time in the source order.

### D7 — Orphan mega-menu content block · Low
`/elementskit-content/dynamic-content-megamenu-menuitem696/` is published and indexed by
the sitemap but is not wired into the rendered header.

---

## E. Layout & spacing

### E1 — Container gutters differ per page · High
At 1440px every page resolves to a 1140px column, but at 900px half the pages measure
**900px** and half **880px**, and at 390px pages measure **390px**, **370px** or **350px**.
Card edges therefore do not align between pages at the same viewport.

### E2 — Hand-dragged column widths · High
Column widths include `11.286%` (52 uses), `96.57%`, `100.656%`, `93.302%`, `47.285%`,
`52.332%`, `40.541%` — values produced by dragging the editor handle, not by a grid.

### E3 — Fixed pixel card widths · Medium
`329.188px` (149 uses), `322.062px` (18), `303.203px` (17) — sub-pixel widths hard-coded
on desktop cards.

### E4 — Thirteen border-radius values · Medium
`0, 5, 6, 8, 10, 14, 15, 16, 20px` plus four asymmetric combinations. One is written
`08px` (leading zero) and one carries `!important`.

### E5 — Two ambient shadows that differ only in alpha · Low
`rgba(0,0,0,0.06)` (35 uses) and `rgba(0,0,0,0.04)` (35 uses), otherwise identical.

### E6 — Section padding set per element · Medium
Inner container padding includes `16px 36px`, `20px`, `40px 34px 30px 34px`,
`15px 24px 17px 24px`, `14px 28px`, `10px`, `15px`. No spacing scale.

---

## F. Responsive

### F1 — Tablet is unstyled · High
Tablet typography is byte-identical to desktop on all 20 pages inspected. The
`max-width: 1024px` query is used only 4 times sitewide, versus 43 uses of
`max-width: 767px`. The 768–1024px range receives desktop type at tablet widths.

### F2 — Mobile heading sizes set ad hoc · High
The same 40px/900 desktop section title becomes 16px on Home and Public & Guest WiFi,
21px on About, 30px on six pages, 33px on the service hub, and stays 40px on
WiFi & Network Solutions.

### F3 — Mobile body copy sometimes grows · Medium
Body text steps **up** from 15px to 18px on Areas We Serve, Contact and
Infrastructure & Cabling, while other pages hold or reduce.

### F4 — Two parallel header implementations · Medium
Desktop/tablet and mobile are served by two separate header rows with different contents —
the mobile header drops the contact strip, the "Get in Touch" CTA and the social icons.

### F5 — Two header rows never render · Medium
Rows 1 and 2 of header template `624` carry `elementor-hidden-desktop`,
`elementor-hidden-tablet` **and** `elementor-hidden-mobile` simultaneously. They are dead
markup shipped on every page request.

---

## G. Content & links
*(carried forward from the Phase 1 page inventory)*

### G1 — `/reyee/` contains Hikvision content · High
Page title is "Hikvision", body opens "Hikvision is a major video security technology
brand". A separate `/reyee-2/` holds the actual Reyee content.

### G2 — Three near-duplicate POPIA pages · Medium
`/policy-popia/`, `/policy-popia-2/` and `/policy-popia-cmaxx/` carry the same 29-heading
policy. Only `/policy-popia/` is linked from the footer.

### G3 — Navigation labels point at unrelated URLs · Medium
"Services" → `/about/`; "About" → `/about-2/`; "Case Studies" → `/our-work/`.
`/services/` and `/case-studies/` both return 404.

### G4 — Two case studies with near-identical titles · Medium
`/office-wifi-solutions-network-optimisation/` ("Office WiFi Upgrade for a Growing
Business in Midrand", content set in Centurion) and
`/office-wifi-upgrade-for-a-growingbusiness-in-midrand/`. The second is not linked from
Our Work and uses the theme template.

### G5 — Malformed email link · Medium
Industries page renders `http://info@cmaxxwifisolutions.co.za` as an `http://` link.

### G6 — Empty and generic social links · Medium
Facebook (header) and "Google Profile" (footer) have empty `href` attributes.
LinkedIn points to `linkedin.com/feed/` and `linkedin.com`, not a company page.

### G7 — Leftover plugin demo link in the footer · Low
The footer logo links to `https://wpmet.com/plugin/elementskit/car-repair/`.

### G8 — Two email domains · Medium
`info@cmaxxwifisolutions.co.za` (footer, body) vs `admin@cmaxxsolutions.co.za` (header).

### G9 — Phone number written three ways · Low
`tel:0101403660`, `tel:010 140 3660`, `tel:010%20140%203660`.

### G10 — Whole site is `noindex, nofollow` · High at launch
Every page serves `<meta name="robots" content="noindex, nofollow">`. Expected on the
GoDaddy staging domain; must not survive the move to the live domain.

### G11 — Typos in live copy · Low
"Slow Spped" (home), "Infra & cCable" (mega-menu block), "GrowingBusiness" (case-study
title), "out specialists" for "our specialists" (home contact block).

---

## H. Audit limitations

Recorded so later phases know what was **not** verified:

1. **No JavaScript executed.** Measurements come from a local mirror with stylesheets and
   images but no JS. Slider tracks, counters, the animated headline, accordions and the
   mobile burger were measured in their pre-initialisation state. A ~2181px wide logo
   strip appears to overflow the viewport in that state; on the live site a script may
   clip it. **Horizontal overflow is therefore unconfirmed and is not claimed as a defect.**
2. **Hover and focus states** were read from CSS declarations, not exercised in a browser.
3. **The WordPress REST API is blocked by Cloudflare**, so Elementor's stored element
   settings could not be read; all values are computed from served CSS.
4. Measurements were taken at exactly 1440 / 900 / 390 px. Behaviour between those widths
   was not sampled.
5. 20 of 46 pages were rendered in the browser. The remaining 26 (18 technology brand
   pages, 5 legal pages, 3 case studies) were analysed from CSS and HTML only; the brand
   and legal pages are template clones of pages that were rendered.
