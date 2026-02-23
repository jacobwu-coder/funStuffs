Subprojects index — funStuff

This file lists the subprojects inside this repository and their current status.

- todo/ — simple CLI todo app (Completed: first version)
  - Path: todo/
  - Notes: package with __main__.py; storage: ~/.local/share/funstuff/todos.json

- web/ — tiny web demos (Planned)
  - Path: web/
  - Notes: placeholder folder for Flask/static demos

- tools/ — small CLI utilities (Planned)
  - Path: tools/
  - Notes: helper scripts and utilities; good place for git helpers and quick automations

- experiments/ — QMD + retrieval samples and summarizers (Planned)
  - Path: experiments/
  - Notes: place to experiment with qmd, local embeddings, retrieval → summarization flows

- quant_demo/ — CCXT grid-strategy demo for testnet (Active)
  - Path: quant_demo/
  - Notes: minimal CCXT-based scaffold; demo_grid.py for ticker, order book, spread, simple grid; testnet-only by default; see README for venv and env vars

- bookmarks_tool/ — Chrome bookmarks backup and reorganizer (Active)
  - Path: bookmarks_tool/
  - Notes: export_bookmarks.sh (Mac), tidy_bookmarks.py (parse/dedupe/reorg HTML); works on exported backups only, does not modify Chrome profile

How to add a new subproject
1. Create a new folder at repo root (e.g. myproject/) and add README.md describing purpose and usage.  
2. Prefer package layout (myproject/__init__.py) for anything runnable by python -m myproject.  
3. Add tests under tests/ or myproject/tests and update README and SUBPROJECTS.md.  
4. Use Codex or the coding-agent skill to scaffold initial files, then review and commit.
