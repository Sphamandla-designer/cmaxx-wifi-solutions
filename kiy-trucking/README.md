# KIY Trucking — Letterhead

A4 letterhead built to match the supplied KIY Trucking logo and social artwork
(black ground, distressed white "KIY", red italic "TRUCKING", red speed swoosh,
tagline "Beyond Borders. Delivering Trust.").

## Files

| File | Purpose |
| --- | --- |
| `letterhead.html` | Editable source. Page 1 is the full letterhead, page 2 the continuation sheet. |
| `KIY-Trucking-Letterhead.pdf` | Print-ready A4 export (two pages). |
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

Everything in square brackets in `letterhead.html` is a placeholder:
address, phone, registration and VAT numbers, directors, recipient and
signatory. Replace them, then run `node render.mjs` to regenerate the PDF.
