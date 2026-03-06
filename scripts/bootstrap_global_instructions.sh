#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_CODEX="$ROOT_DIR/bootstrap/global-instructions/GLOBAL_CODEX_AGENTS.md"
SRC_QWEN="$ROOT_DIR/bootstrap/global-instructions/GLOBAL_QWEN_QWEN.md"

DEST_HOME="${HOME}"
DRY_RUN=0
ASSUME_YES=0
RESTORE=0
RESTORE_STAMP=""

usage() {
  cat <<'EOF'
Usage:
  bash scripts/bootstrap_global_instructions.sh [--dry-run] [--yes] [--dest-home PATH]
  bash scripts/bootstrap_global_instructions.sh --restore [--dest-home PATH] [--stamp YYYYmmdd-HHMMSS]

Options:
  --dry-run         Show planned actions without writing files.
  --yes             Skip confirmation prompt.
  --dest-home PATH  Alternate HOME root containing .codex/ and .qwen/.
  --restore         Restore the latest backups (or a specific --stamp).
  --stamp VALUE     Backup timestamp suffix to restore.
  -h, --help        Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    --yes)
      ASSUME_YES=1
      ;;
    --dest-home)
      shift
      [[ $# -gt 0 ]] || { echo "[error] --dest-home requires a path" >&2; exit 1; }
      DEST_HOME="$1"
      ;;
    --restore)
      RESTORE=1
      ;;
    --stamp)
      shift
      [[ $# -gt 0 ]] || { echo "[error] --stamp requires a value" >&2; exit 1; }
      RESTORE_STAMP="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[error] unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

DEST_CODEX_DIR="${DEST_HOME}/.codex"
DEST_QWEN_DIR="${DEST_HOME}/.qwen"
DEST_CODEX_FILE="${DEST_CODEX_DIR}/AGENTS.md"
DEST_QWEN_FILE="${DEST_QWEN_DIR}/QWEN.md"

if [[ ! -f "$SRC_CODEX" || ! -f "$SRC_QWEN" ]]; then
  echo "[error] global instruction snapshots not found in bootstrap/global-instructions" >&2
  exit 1
fi

sha256_file() {
  if [[ -f "$1" ]]; then
    sha256sum "$1" | awk '{print $1}'
  else
    echo "-"
  fi
}

confirm_or_exit() {
  if [[ "$ASSUME_YES" -eq 1 ]]; then
    return 0
  fi
  read -r -p "Proceed? [y/N] " reply
  case "$reply" in
    y|Y|yes|YES)
      return 0
      ;;
    *)
      echo "[info] aborted"
      exit 0
      ;;
  esac
}

select_backup() {
  local target="$1"
  if [[ -n "$RESTORE_STAMP" ]]; then
    local candidate="${target}.bak.${RESTORE_STAMP}"
    [[ -f "$candidate" ]] || { echo "[error] backup not found: $candidate" >&2; exit 1; }
    echo "$candidate"
    return 0
  fi
  local latest
  latest="$(ls -1t "${target}".bak.* 2>/dev/null | head -n 1 || true)"
  [[ -n "$latest" ]] || { echo "[error] no backup found for $target" >&2; exit 1; }
  echo "$latest"
}

if [[ "$RESTORE" -eq 1 ]]; then
  CODEX_BACKUP="$(select_backup "$DEST_CODEX_FILE")"
  QWEN_BACKUP="$(select_backup "$DEST_QWEN_FILE")"

  echo "[plan] restore global instructions"
  echo "  codex: $CODEX_BACKUP -> $DEST_CODEX_FILE"
  echo "  qwen:  $QWEN_BACKUP -> $DEST_QWEN_FILE"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] no files changed"
    exit 0
  fi

  confirm_or_exit
  mkdir -p "$DEST_CODEX_DIR" "$DEST_QWEN_DIR"
  cp "$CODEX_BACKUP" "$DEST_CODEX_FILE"
  cp "$QWEN_BACKUP" "$DEST_QWEN_FILE"
  echo "[ok] restored Codex global instructions: $DEST_CODEX_FILE"
  echo "[ok] restored Qwen global instructions: $DEST_QWEN_FILE"
  exit 0
fi

echo "[plan] install global instruction snapshots"
echo "  source codex: $SRC_CODEX"
echo "  source qwen:  $SRC_QWEN"
echo "  target home:  $DEST_HOME"
echo "  codex current sha256: $(sha256_file "$DEST_CODEX_FILE")"
echo "  qwen  current sha256: $(sha256_file "$DEST_QWEN_FILE")"
echo "  codex source  sha256: $(sha256_file "$SRC_CODEX")"
echo "  qwen  source  sha256: $(sha256_file "$SRC_QWEN")"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "[dry-run] no files changed"
  exit 0
fi

confirm_or_exit

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
