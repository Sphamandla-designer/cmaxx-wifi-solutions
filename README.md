# CMAXX WiFi Solutions — Website Rebuild

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
