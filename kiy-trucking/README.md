# KIY Trucking — Letterhead

A4 letterhead built to match the supplied KIY Trucking logo and social artwork
(black ground, distressed white "KIY", red italic "TRUCKING", red speed swoosh,
tagline "Beyond Borders. Delivering Trust.").

## Files

| File | Purpose |
| --- | --- |
| `letterhead.html` | Editable source. Page 1 is the full letterhead, page 2 the continuation sheet. |
| `KIY-Trucking-Letterhead.pdf` | Print-ready A4 export (two pages). |
| `KIY-Trucking-Letterhead.docx` | Editable Word version. Header and footer are editable tables; the stripes are decorative images. Uses Arial so it renders the same on any machine. |
| `docx/build-docx.cjs` | Rebuilds the Word file: `node docx/build-docx.cjs`. `docx/make-stripes.mjs` regenerates the stripe artwork. |
| `letterhead-page1.png`, `letterhead-page2.png` | Previews at 2× (1588 px wide). |
| `kiy-trucking-logo.jpg` | Logo as supplied. |
| `render.mjs` | Re-exports the PDF and PNGs with Playwright: `node render.mjs`. |

## Identity tokens

| Token | Value | Source |
| --- | --- | --- |
| Black | `#000000` | logo background |
| Red | `#B5010D` | sampled from "TRUCKING" |
| Hot red | `#E3121F` | highlight red from the social artwork |
| Display type | Barlow Condensed (italic 800/900 for headings) | closest open font to the logo lettering |
| Body type | Barlow 400/500 | |

## Filling in company details

Everything in square brackets in `letterhead.html` and the Word file is a placeholder:
address, phone, registration and VAT numbers, directors, recipient and
signatory. Replace them, then run `node render.mjs` to regenerate the PDF.

## Editing the Word version

Double-click the header or footer in Word to edit the contact block, registration
details, directors and tagline. The logo and red stripes are images and can be
swapped by right-clicking them and choosing "Change Picture". The first page uses
the full header; every following page automatically gets the compact one.
