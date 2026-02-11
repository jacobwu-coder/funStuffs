funStuffs — playground for small coding projects (AI-assisted)

Overview
- This repository is a workspace for small, focused projects generated and maintained with Codex + OpenClaw assistance.
- Philosophy: local-first, modular, and documented. Each subproject lives in its own folder under the repo root.

Subprojects index
- See SUBPROJECTS.md for the full index and status of subprojects in this repo.

Current subprojects
- todo/ — simple CLI todo app (first version completed)
  - Usage: python -m todo add "Buy milk"; python -m todo list --all
  - Data file: ~/.local/share/funstuff/todos.json

Planned subprojects (examples)
- web/ — tiny web demos (Flask/Static)  
- tools/ — small CLI utilities (git helpers, data cleaners)  
- experiments/ — QMD + retrieval samples and summarizers

Workflows
- Generate code with Codex CLI (npx @openai/codex) or via the coding-agent skill and review before committing.
- Local dev: create a virtual env, run tests with pytest, and commit changes via commit_and_push.sh.

How to add a new subproject
1. mkdir myproject && cd myproject
2. Create a minimal README and a small script or package (we recommend package layout)
3. Run Codex to scaffold features or ask the coding-agent to generate code interactively
4. Add tests under tests/ or myproject/tests and run pytest from the repo root
5. Commit and push to your fork; open PRs if collaborating

AI & code generation (best practices)
- Use precise prompts and ask Codex to output only code. Review and test all generated code before running it.
- Keep generated artifacts in a named subfolder and commit them to version control after review.
- The coding-agent skill is configured to run safe commands only in allowed paths. It will not run arbitrary shell commands from chat.

How to try AI generation (example)
- From the macmini (or any machine with Codex CLI):
  npx @openai/codex exec --output-last-message ./myproject/generated.py "Generate a single-file Python script that..."

Contact
- If you want the assistant to scaffold a new subproject for you, tell it: "Create subproject <name> with <spec>" and it will generate a starting layout in the repo.
