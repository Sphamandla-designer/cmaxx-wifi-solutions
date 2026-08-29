# Photography for /structured-cabling/

The brief requires **real CMAXX installation photography** on this page. Stock imagery —
especially the generic "blue cable" stock shot — must not be used for the hero.

Drop the real photos in at these exact paths. The filenames are the naming convention
specified in the brief; the alt text is already written into `index.html` and should be
kept (adjust only if the photo shows something different).

| Path | Subject | Used in |
| --- | --- | --- |
| `network-rack-patch-panel-midrand.jpg` | Clean CMAXX rack / terminated patch panel | Hero (§1) — **required** |
| `ethernet-data-point-installation.jpg` | Data point / wall outlet being terminated | §12 Data points |
| `fibre-backbone-network-installation.jpg` | Fibre / backbone work | §14 Fibre |
| `cat6-cat6a-structured-cabling-gauteng.jpg` | Cat6 / Cat6A cable and termination | Spare — for §5 if a photo is added |
| `poe-wifi-access-point-cabling.jpg` | Ceiling AP cable run | Spare — for §11 if a photo is added |
| `outdoor-network-cabling-gauteng.jpg` | Outdoor protected run | Spare — for §9 if a photo is added |

Before committing photos:

- Compress for web (target < 250 KB each; WebP alongside JPEG is preferable).
- Keep the `width`/`height` attributes in `index.html` in step with the real aspect ratio
  so the page does not shift as images load.
- Everything below the fold already carries `loading="lazy" decoding="async"`; the hero
  image carries `fetchpriority="high"` and must **not** be lazy-loaded.

Candidate source images already in the WordPress media library (verify each actually shows
CMAXX work before using — several are stock):

- `2026/08/WhatsApp-Image-2026-08-19-at-10.*.jpeg` — appear to be genuine site photos
- `2026/07/WhatsApp-Image-2026-06-21-at-16.03.2*.jpeg` — appear to be genuine site photos
- `2026/07/network-infrastructure-copper-cabling-1321663487-600x350-1.png` — **stock**, do not use for the hero
