#!/usr/bin/env python3
"""Convert Chrome Bookmarks JSON to Chrome‑importable HTML.

This is a small helper around the Chrome `Bookmarks` JSON format (or a backup
JSON exported from your profile). It flattens all URL entries into a single
folder and writes a classic Netscape bookmark HTML file that Chrome can import.

Usage (from repo root or inside bookmarks_tool/):

  python3 bookmarks_tool/json_to_chrome_html.py \
      --input bookmarks_tool/backups/Bookmarks-....json \
      --output bookmarks_tool/out/bookmarks-from-json.html

You can then import the generated HTML via:
  Chrome → Bookmarks Manager → ⋮ → Import Bookmarks
"""

import argparse
import html
import json
import os
import sys
import time
from typing import Dict, List


def load_bookmarks_from_chrome_json(path: str) -> List[Dict[str, str]]:
    """Load a flat list of {name, url} from a Chrome Bookmarks JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls: List[Dict[str, str]] = []

    def walk(node):
        if isinstance(node, dict):
            t = node.get("type")
            if t == "url":
                urls.append(
                    {
                        "name": node.get("name", "") or node.get("url", ""),
                        "url": node.get("url", ""),
                    }
                )
            for v in node.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    roots = data.get("roots", {})
    walk(roots)
    return urls


def write_chrome_import_html(
    bookmarks: List[Dict[str, str]],
    outpath: str,
    folder_name: str = "Imported-from-JSON",
    title: str = "Bookmarks",
) -> None:
    """Write a minimal Netscape bookmark file Chrome can import.

    We keep the structure simple:
      - <DL> root
      - one <H3> folder containing all converted bookmarks as <A> entries
    """
    ts = str(int(time.time()))
    esc_title = html.escape(title, quote=False)
    esc_folder = html.escape(folder_name, quote=False)

    os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        f.write("<!-- This is an automatically generated file.\n")
        f.write("     It will be read and overwritten.\n")
        f.write("     DO NOT EDIT! -->\n")
        f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
        f.write(f"<TITLE>{esc_title}</TITLE>\n")
        f.write(f"<H1>{esc_title}</H1>\n")
        f.write("<DL><p>\n")
        f.write(
            f'<DT><H3 ADD_DATE="{ts}" LAST_MODIFIED="{ts}" PERSONAL_TOOLBAR_FOLDER="false">{esc_folder}</H3>\n'
        )
        f.write("<DL><p>\n")

        for b in bookmarks:
            url = (b.get("url") or "").strip()
            if not url:
                continue
            name = (b.get("name") or url).strip()
            esc_name = html.escape(name, quote=False)
            esc_url = html.escape(url, quote=True)
            f.write(f'<DT><A HREF="{esc_url}">{esc_name}</A>\n')

        f.write("</DL><p>\n")
        f.write("</DL><p>\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Chrome Bookmarks JSON to Chrome‑importable HTML."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to Chrome Bookmarks JSON (e.g. backups/Bookmarks-*.json or 'Bookmarks').",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output HTML path that Chrome can import.",
    )
    parser.add_argument(
        "--folder-name",
        default="Imported-from-JSON",
        help="Name of the folder that will contain all imported links.",
    )
    parser.add_argument(
        "--title",
        default="Bookmarks",
        help="HTML <TITLE>/<H1> text for the generated file.",
    )
    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        bookmarks = load_bookmarks_from_chrome_json(input_path)
    except Exception as e:  # pragma: no cover - simple CLI guard
        print(f"Failed to parse Chrome Bookmarks JSON: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(bookmarks)} bookmarks from {input_path}")
    write_chrome_import_html(
        bookmarks,
        outpath=args.output,
        folder_name=args.folder_name,
        title=args.title,
    )
    print(f"Wrote Chrome-importable HTML to {args.output}")
    print("You can now import this file in Chrome's Bookmarks Manager.")


if __name__ == "__main__":
    main()

