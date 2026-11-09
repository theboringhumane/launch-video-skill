#!/usr/bin/env bash
# Screenshot local HTML pages (rendered product templates, emails, landing pages) with headless Chrome.
# usage: shoot-pages.sh <dir-with-html> <out-dir> [width=1440] [height=2200] [scale=1.5]
# Serves <dir> on localhost so root-relative assets (/fonts/…) resolve, then shoots every *.html.
set -euo pipefail
src=$1 out=$2 w=${3:-1440} h=${4:-2200} s=${5:-1.5} port=8765
chrome=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
command -v google-chrome >/dev/null && chrome=${CHROME:-google-chrome}
mkdir -p "$out"; out=$(cd "$out" && pwd)
(cd "$src" && python3 -m http.server $port >/dev/null 2>&1) & srv=$!
trap 'kill $srv' EXIT; sleep 1
for f in "$src"/*.html; do
  name=$(basename "$f" .html)
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$s" \
    --window-size="$w,$h" --virtual-time-budget=3000 --screenshot="$out/$name.png" \
    "http://localhost:$port/$name.html" >/dev/null 2>&1
  echo "$out/$name.png"
done
