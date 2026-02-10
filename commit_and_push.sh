#!/usr/bin/env bash
set -euo pipefail

# commit_and_push.sh
# Simple safe helper to stage, commit, and optionally push changes.
# Usage:
#   ./commit_and_push.sh
# or specify repo path:
#   ./commit_and_push.sh /path/to/repo

REPO_DIR=${1:-$(pwd)}
cd "$REPO_DIR"

# Show status
echo "===== git status ====="
git status --short --branch

echo
read -p "Stage all changes and continue? (y/N) " yn
if [[ "${yn}" != "y" ]]; then
  echo "Aborting. No changes staged."
  exit 1
fi

git add -A

echo
read -p "Enter commit message: " msg
if [[ -z "$msg" ]]; then
  echo "Empty message — aborting."
  exit 1
fi

# Optional: run tests here if you want
# echo "Running tests..."
# if ! pytest -q; then
#   echo "Tests failed — aborting commit."
#   exit 1
# fi

git commit -m "$msg"

echo
read -p "Push to origin? (y/N) " yn2
if [[ "${yn2}" == "y" ]]; then
  git push origin HEAD
  echo "Pushed to origin."
else
  echo "Committed locally. Run 'git push origin HEAD' when ready."
fi
