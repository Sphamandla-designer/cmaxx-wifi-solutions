# CMAXX social media posts

Two 4:5 feed posts (2160 x 2700 px, Instagram / Facebook / LinkedIn ready).

| File | Promotes |
| --- | --- |
| `cmaxx-smart-home-post.png` | https://1124817.eu9.myftpupload.com/smart-home/ |
| `cmaxx-managed-wifi-post.png` | https://1124817.eu9.myftpupload.com/managed-wifi/ |

## Editing

The posters are built from `source/*.html` + `source/poster.css` and rendered with Playwright.
Change the copy in the HTML, then from `source/` run:

```bash
npm i playwright   # once
node render.mjs . ..
```

Background scenes in `source/assets/` were generated for these posts (no stock licensing attached).
The logo is `logo-white.png`, derived from the site logo. Brand accent: `#f37021`.

## Light version (Managed WiFi)

`cmaxx-managed-wifi-post-light.png` (1:1, 2160 x 2160) reuses the bright office/router
reference poster with the original branding and text removed and CMaxx details in the same
layout. Source: `source/managed-wifi-light.html`, background `source/assets/managed-wifi-light-bg.png`.

## Light version (Smart Home)

`cmaxx-smart-home-post-light.png` (4:5, 2160 x 2700) reuses the living-room/phone reference
poster with the original branding and text removed and CMaxx copy in the same positions.
Source: `source/smart-home-light.html`, background `source/assets/smart-home-light-bg.png`.

## All services (light)

`cmaxx-services-post.png` (4:5, 2160 x 2700) lists all seven core services on a bright scene.
Source: `source/services.html`, background `source/assets/services-bg.png`.
