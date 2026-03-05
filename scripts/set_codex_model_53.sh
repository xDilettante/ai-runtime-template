#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! mount | grep -q " $(pwd)/.codex .* (rw"; then
  echo "ERROR: .codex is not writable (mount is read-only)"
  echo "Current mount:"
  mount | grep " $(pwd)/.codex " || true
  exit 1
fi

updated=0
for f in .codex/config.toml .codex/roles/*.toml; do
  if grep -q '^model\s*=\s*"gpt-5-codex"' "$f"; then
    sed -i 's/^model\s*=\s*"gpt-5-codex"/model = "gpt-5.3-codex"/' "$f"
    updated=$((updated+1))
  fi
done

echo "Updated files: $updated"
python3 ./.codex/scripts/codex_check.py
