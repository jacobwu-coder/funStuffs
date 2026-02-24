bookmarks_tool — Chrome bookmarks organizer

Purpose
- Small tool to help back up, audit, dedupe, and reorganize Chrome bookmarks.
- Designed as a safe, local-first utility you run on your Mac. It does not modify browser state unless you explicitly apply a reorganization.

Contents
- export_bookmarks.sh — convenience script to export Chrome bookmarks to HTML (backups). Mac-specific (uses Chrome's default profile path).
- tidy_bookmarks.py — Python script to parse Chrome bookmarks HTML (or Chrome Bookmarks JSON), dedupe exact-duplicate URLs, and write a reorganized HTML file into an output folder. It can also produce a JSON index.
- json_to_chrome_html.py — convert Chrome Bookmarks JSON to Chrome-importable HTML (Netscape bookmark format). Use when you have a JSON backup and want to import it via Bookmarks Manager → Import Bookmarks.
- README.md — this file.

Quickstart
1) Backup your bookmarks (export in Chrome or run the included script):
   ./export_bookmarks.sh
   This writes backups to ./backups/ with timestamped filenames.

2) Create a temp venv and install dependencies (python script uses only stdlib, no deps required):
   python3 -m venv .venv && source .venv/bin/activate

3) Run the audit (no changes):
   python3 tidy_bookmarks.py --input backups/bookmarks-YYYYMMDD-HHMMSS.html --audit

4) Run a simulated reorganization (writes reorganized HTML to ./out/):
   python3 tidy_bookmarks.py --input backups/bookmarks-YYYYMMDD-HHMMSS.html --outdir out --simulate

5) If you like the result, run without --simulate to produce the reorganized HTML.

JSON to HTML (Chrome import)
- If you have a Chrome Bookmarks JSON file (e.g. from backups/ or a copied `Bookmarks` file), convert it to HTML so Chrome can import it:
  python3 json_to_chrome_html.py --input backups/Bookmarks-Profile-YYYYMMDD.json --output out/bookmarks-from-json.html
- Optional: `--folder-name "My folder"` and `--title "Bookmarks"`. Then in Chrome: Bookmarks Manager → ⋮ → Import Bookmarks → select the output HTML.

Safety
- The tool never writes to your Chrome profile. It works on exported HTML backups only. Always keep the backups/ folder until you’ve verified the result.

Customization
- Edit the folder_order list in tidy_bookmarks.py to change the target top-level folders and ordering.

Notes
- This is a lightweight starting point. If you want browser-automated reorganization, we can add an optional step that uses the OpenClaw browser relay (requires you to attach a Chrome tab and explicit approval).