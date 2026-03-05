#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <codex|qwen> <command...>" >&2
  exit 2
fi

runtime="$1"
shift

if [[ "$runtime" != "codex" && "$runtime" != "qwen" ]]; then
  echo "runtime must be codex or qwen" >&2
  exit 2
fi

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
lock_dir="$root_dir/.ai-state/locks"
mkdir -p "$lock_dir"
lock_file="$lock_dir/${runtime}.lock"

# Keep lock descriptor open for the command lifetime.
exec 9>"$lock_file"
timeout_sec="${AI_STATE_LOCK_TIMEOUT_SEC:-60}"
if ! flock -w "$timeout_sec" 9; then
  echo "failed to acquire ai-state lock: $lock_file (timeout ${timeout_sec}s)" >&2
  exit 1
fi

export AI_STATE_RUNTIME="$runtime"
export AI_STATE_ROOT="$root_dir/.ai-state/$runtime/orchestrator"

"$@"
