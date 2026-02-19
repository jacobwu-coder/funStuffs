#!/usr/bin/env bash
# Export Chrome Bookmarks (macOS default profile) to a timestamped HTML file in backups/
set -euo pipefail
mkdir -p backups
TS=$(date -u +"%Y%m%dT%H%M%SZ")
# Default Chrome bookmark file location (macOS). This copies the Bookmarks file database (JSON) and also uses Chrome's Export via AppleScript fallback.
PROFILE_DIR="$HOME/Library/Application Support/Google/Chrome/Default"
BOOKMARKS_JSON="$PROFILE_DIR/Bookmarks"
OUT_HTML="backups/bookmarks-$TS.html"

# If Google Chrome is running, AppleScript export may be more reliable for HTML; otherwise attempt simple JSON->HTML fallback (limited).
if pgrep -x "Google Chrome" >/dev/null 2>&1; then
  echo "Chrome running — using AppleScript to export bookmarks to HTML (requires Chrome to show bookmarks manager)."
  /usr/bin/osascript <<APPLE
  tell application "Google Chrome"
    activate
    delay 0.3
    tell application "System Events"
      keystroke "o" using {command down, shift down}
    end tell
  end tell
APPLE
  echo "Please use Chrome's Bookmarks Manager to Export HTML and save to: $OUT_HTML"
  echo "After saving, run: python3 tidy_bookmarks.py --input $OUT_HTML --audit"
else
  if [ -f "$BOOKMARKS_JSON" ]; then
    echo "Chrome Bookmarks JSON found at $BOOKMARKS_JSON"
    echo "Converting to basic HTML backup (best-effort)."
    python3 - <<PY
import json,sys
p='$BOOKMARKS_JSON'
with open(p) as f:
    data=json.load(f)
# Very small converter: extract urls from 'roots' recursively
urls=[]
def walk(node):
    if isinstance(node,dict):
        if node.get('type')=='url':
            urls.append((node.get('name',''), node.get('url','')))
        for k in node:
            walk(node[k])
    elif isinstance(node,list):
        for x in node:
            walk(x)
walk(data.get('roots',{}))
print('<!doctype html>\n<html><head><meta charset="utf-8"><title>Bookmarks backup</title></head><body>')
print('<h1>Bookmarks backup</h1>')
print('<ul>')
for n,u in urls:
    print(f'<li><a href="{u}">{n or u}</a></li>')
print('</ul></body></html>')
PY > "$OUT_HTML"
    echo "Wrote backup HTML to $OUT_HTML"
  else
    echo "No Chrome Bookmarks JSON found at $BOOKMARKS_JSON. Please export bookmarks from Chrome to HTML and place the file in backups/." >&2
    exit 1
  fi
fi
