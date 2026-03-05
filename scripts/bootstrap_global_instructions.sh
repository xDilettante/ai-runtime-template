#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_CODEX="$ROOT_DIR/bootstrap/global-instructions/GLOBAL_CODEX_AGENTS.md"
SRC_QWEN="$ROOT_DIR/bootstrap/global-instructions/GLOBAL_QWEN_QWEN.md"

DEST_CODEX_DIR="${HOME}/.codex"
DEST_QWEN_DIR="${HOME}/.qwen"
DEST_CODEX_FILE="$DEST_CODEX_DIR/AGENTS.md"
DEST_QWEN_FILE="$DEST_QWEN_DIR/QWEN.md"

if [[ ! -f "$SRC_CODEX" || ! -f "$SRC_QWEN" ]]; then
  echo "[error] global instruction snapshots not found in bootstrap/global-instructions" >&2
  exit 1
fi

mkdir -p "$DEST_CODEX_DIR" "$DEST_QWEN_DIR"

TS="$(date +%Y%m%d-%H%M%S)"
if [[ -f "$DEST_CODEX_FILE" ]]; then
  cp "$DEST_CODEX_FILE" "${DEST_CODEX_FILE}.bak.${TS}"
fi
if [[ -f "$DEST_QWEN_FILE" ]]; then
  cp "$DEST_QWEN_FILE" "${DEST_QWEN_FILE}.bak.${TS}"
fi

cp "$SRC_CODEX" "$DEST_CODEX_FILE"
cp "$SRC_QWEN" "$DEST_QWEN_FILE"

echo "[ok] installed Codex global instructions: $DEST_CODEX_FILE"
echo "[ok] installed Qwen global instructions: $DEST_QWEN_FILE"
echo "[info] backups (if existed) saved with suffix .bak.${TS}"
