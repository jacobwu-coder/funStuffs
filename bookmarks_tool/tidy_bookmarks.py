#!/usr/bin/env python3
"""Tidy bookmarks: simple HTML/JSON read, dedupe, and reorganize tool.

Usage:
  python3 tidy_bookmarks.py --input backups/bookmarks-YYYYMMDDTHHMMSSZ.html --audit
  python3 tidy_bookmarks.py --input backups/bookmarks-...html --outdir out --simulate
  python3 tidy_bookmarks.py --input backups/Bookmarks-Profile.json --outdir out --audit

This script is intentionally conservative: it reads exported HTML bookmarks (Chrome export)
or Chrome Bookmarks JSON file and writes a reorganized HTML file to outdir/. It does not modify browser state.
"""
import argparse
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
import datetime


class BookmarkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_a = False
        self.cur_attrs = {}
        self.cur_text = ''
        self.bookmarks = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            self.in_a = True
            self.cur_attrs = dict(attrs)
            self.cur_text = ''

    def handle_endtag(self, tag):
        if tag.lower() == 'a' and self.in_a:
            href = self.cur_attrs.get('href', '')
            name = self.cur_text.strip() or href
            self.bookmarks.append({'name': name, 'url': href})
            self.in_a = False
            self.cur_attrs = {}
            self.cur_text = ''

    def handle_data(self, data):
        if self.in_a:
            self.cur_text += data


def load_bookmarks_from_html(path):
    with open(path,'r',encoding='utf-8') as f:
        data = f.read()
    p = BookmarkHTMLParser()
    p.feed(data)
    return p.bookmarks


def load_bookmarks_from_chrome_json(path):
    # Chrome 'Bookmarks' JSON structure: roots -> (bookmark_bar | other | synced) -> children
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    urls = []
    def walk(node):
        if isinstance(node, dict):
            t = node.get('type')
            if t == 'url':
                urls.append({'name': node.get('name',''), 'url': node.get('url','')})
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(data.get('roots', {}))
    return urls


def dedupe_bookmarks(bookmarks):
    seen = set()
    out = []
    for b in bookmarks:
        key = b.get('url') or b.get('name')
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


DEFAULT_ORDER = [
    '00-Inbox', '10-Work', '20-School', '30-Research', '40-Tools', '50-Finance', '60-Read-Later', '70-Personal', '90-Archive'
]


def reorganize(bookmarks, order=None):
    order = order or DEFAULT_ORDER
    buckets = {k: [] for k in order}
    others = []
    for b in bookmarks:
        u = b.get('url','')
        domain = ''
        try:
            domain = urlparse(u).netloc
        except Exception:
            domain = ''
        # crude routing rules — customize as needed
        if any(x in domain for x in ['github.com','gitlab.com']):
            buckets['40-Tools'].append(b)
        elif any(x in domain for x in ['edu','udel.edu','canvas','instructure']):
            buckets['20-School'].append(b)
        elif any(x in domain for x in ['medium.com','x.com','twitter.com','substack.com']):
            buckets['30-Research'].append(b)
        elif any(x in domain for x in ['mexc.com','binance.com','coinbase.com','bloomberg.com','finance']):
            buckets['50-Finance'].append(b)
        else:
            others.append(b)
    return buckets, others


def write_html(buckets, others, outpath):
    with open(outpath,'w',encoding='utf-8') as f:
        f.write('<!doctype html>\n<html><head><meta charset="utf-8"><title>Bookmarks reorganized</title></head><body>\n')
        f.write(f'<h1>Bookmarks reorganized - {datetime.datetime.utcnow().isoformat()}Z</h1>\n')
        for k, items in buckets.items():
            f.write(f'<h2>{k} ({len(items)})</h2>\n<ul>\n')
            for b in items:
                f.write(f'<li><a href="{b["url"]}">{b["name"]}</a></li>\n')
            f.write('</ul>\n')
        f.write(f'<h2>Others ({len(others)})</h2><ul>\n')
        for b in others:
            f.write(f'<li><a href="{b["url"]}">{b["name"]}</a></li>\n')
        f.write('</ul>\n</body></html>')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--outdir', default='out')
    p.add_argument('--simulate', action='store_true')
    p.add_argument('--audit', action='store_true')
    args = p.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f'Input file not found: {input_path}', file=sys.stderr)
        sys.exit(1)

    # Support both HTML (export) and Chrome Bookmarks JSON
    bookmarks = []
    if input_path.lower().endswith('.html') or input_path.lower().endswith('.htm'):
        bookmarks = load_bookmarks_from_html(input_path)
    elif input_path.lower().endswith('.json') or os.path.basename(input_path) == 'Bookmarks':
        # attempt to parse Chrome JSON format
        try:
            bookmarks = load_bookmarks_from_chrome_json(input_path)
        except Exception as e:
            print('Failed to parse as Chrome Bookmarks JSON:', e, file=sys.stderr)
            sys.exit(2)
    else:
        # try to guess by content
        with open(input_path,'r',encoding='utf-8') as f:
            head = f.read(1024)
        if '<!doctype html' in head.lower() or '<html' in head.lower():
            bookmarks = load_bookmarks_from_html(input_path)
        else:
            try:
                bookmarks = load_bookmarks_from_chrome_json(input_path)
            except Exception as e:
                print('Unknown bookmark file format and parsing failed:', e, file=sys.stderr)
                sys.exit(3)

    print(f'Loaded {len(bookmarks)} bookmarks from {input_path}')

    deduped = dedupe_bookmarks(bookmarks)
    print(f'Deduped -> {len(deduped)} unique bookmarks')

    buckets, others = reorganize(deduped)
    total = sum(len(v) for v in buckets.values()) + len(others)
    print('Bucket counts:')
    for k in buckets:
        print(f' - {k}: {len(buckets[k])}')
    print(f' - Others: {len(others)}')

    if args.audit:
        # write index JSON for review
        os.makedirs('out',exist_ok=True)
        idx = {'buckets': {k: [b for b in buckets[k]] for k in buckets}, 'others':[b for b in others]}
        with open('out/bookmarks_index.json','w',encoding='utf-8') as f:
            json.dump(idx,f,indent=2,ensure_ascii=False)
        print('Wrote audit JSON to out/bookmarks_index.json')
        return

    os.makedirs(args.outdir, exist_ok=True)
    outpath = os.path.join(args.outdir, 'bookmarks-reorganized.html')
    write_html(buckets, others, outpath)
    print(f'Wrote reorganized bookmarks to {outpath}')
    if args.simulate:
        print('Simulation only: file written for review. Will not modify browser bookmarks.')
    else:
        print('Done. To apply changes to browser, import this HTML from the out/ folder into Chrome Bookmarks Manager (or use browser automation).')

if __name__ == '__main__':
    main()
