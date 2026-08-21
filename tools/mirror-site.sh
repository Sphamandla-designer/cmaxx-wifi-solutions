#!/usr/bin/env bash
# Mirror the existing CMAXX website to ./mirror for Phase 1 reconstruction.
#
# Run this on a machine with normal internet access:
#   bash tools/mirror-site.sh [BASE_URL]
#
# Default BASE_URL is the live site. The GoDaddy staging host
# (https://1124817.eu9.myftpupload.com/) can be passed instead.
#
# The mirror captures HTML, CSS, JS, images, fonts and icons exactly as the
# live site serves them, which is what the reconstruction has to match.

set -euo pipefail

BASE_URL="${1:-https://cmaxxsolutions.co.za/}"
HOST="$(printf '%s' "$BASE_URL" | sed -E 's#^https?://##; s#/.*$##')"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/mirror"

mkdir -p "$OUT_DIR"

echo "Mirroring $BASE_URL (host: $HOST) into $OUT_DIR"

# --mirror            recursive, timestamped, infinite depth
# --page-requisites   pull CSS/JS/images/fonts needed to render each page
# --convert-links     rewrite links for local browsing
# --adjust-extension  save text/html as .html
# --span-hosts + --domains  allow the CDN/asset hosts WordPress commonly uses
# --reject-regex      skip WP admin, feeds, and query-string duplicates
wget \
  --mirror \
  --page-requisites \
  --convert-links \
  --adjust-extension \
  --no-parent \
  --span-hosts \
  --domains="$HOST,secureservercdn.net,fonts.googleapis.com,fonts.gstatic.com" \
  --reject-regex '(/wp-admin/|/wp-json/|/feed/|\?replytocom=|\?share=)' \
  --execute robots=off \
  --user-agent='Mozilla/5.0 (compatible; CMAXX-Phase1-Reconstruction/1.0)' \
  --wait=0.5 \
  --random-wait \
  --tries=3 \
  --timeout=30 \
  --no-verbose \
  --directory-prefix="$OUT_DIR" \
  "$BASE_URL" || true   # wget exits non-zero on any single 404; the mirror is still usable

echo
echo "Done. Mirrored files:"
find "$OUT_DIR" -type f | wc -l
echo
echo "Next: npm run audit"
