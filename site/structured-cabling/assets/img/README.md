# Photography for /structured-cabling/

Three genuine CMAXX installation photos are now in place, sourced from the WordPress
media library and re-cropped and compressed for this page. Three of the brief's suggested
slots have **no genuine photo behind them**, so rather than fill those with stock, the
sections were rebuilt to work without a photo.

## In place — real CMAXX work

| File | Shows | Used in |
| --- | --- | --- |
| `network-rack-patch-panel-midrand.jpg` | Wall-mounted lockable LinkBasic cabinet, switch and patch leads visible through the door | Hero (§1) |
| `outdoor-network-cabling-gauteng.jpg` | External run in flexible conduit into a weatherproof box, feeding two PoE cameras on brick | §9 Indoor vs outdoor |
| `poe-camera-cabling-gauteng.jpg` | PoE camera on a boundary-wall bracket — a powered device at the far end of a run | §11 PoE-ready infrastructure |

Source files, before cropping:
`2026/08/WhatsApp-Image-2026-08-19-at-10.06.30.jpeg`,
`2026/07/WhatsApp-Image-2026-06-21-at-16.03.26.jpeg`,
`2026/08/WhatsApp-Image-2026-08-19-at-10.13.05.jpeg`.

Alt text is written to describe what each photo actually shows. If you swap a photo,
update the alt text in `index.html` to match — do not keep alt text describing a
different subject.

## Still wanted — no genuine photo exists yet

These are worth shooting on the next job. The brief's filenames are kept as the naming
convention so they drop straight in:

| File | Subject | Would go in |
| --- | --- | --- |
| `ethernet-data-point-installation.jpg` | Data point / wall outlet being terminated | §12 Data points (currently a two-card layout) |
| `fibre-backbone-network-installation.jpg` | Fibre / backbone termination | §14 Fibre (currently a single card) |
| `cat6-cat6a-structured-cabling-gauteng.jpg` | Cat6 / Cat6A cable and termination close-up | §5 Cable categories |

**Do not fill these with stock.** The brief is explicit that genuine CMAXX photography
comes ahead of stock, and a stock "blue cable" shot in a section about termination quality
actively undermines the page's argument. A section with no photo reads better than a
section with a misleading one.

## Rules when adding a photo

- Compress before committing. Current three total 167 KB; keep the page light.
- Keep `width`/`height` on the `<img>` in step with the real file, so the page does not
  shift as images load.
- Below-the-fold images need `loading="lazy" decoding="async"`. The hero image carries
  `fetchpriority="high"` and must **not** be lazy-loaded.
- Wrap an inline section photo in `<figure class="fig-inset">` so it is capped at 720px
  and does not dominate the section.
- Re-run `npm run build:embedded` afterwards so the single-file build picks the photo up.
