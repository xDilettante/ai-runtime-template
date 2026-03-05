#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def ensure_runtime(root: Path, runtime: str) -> None:
    orch = root / ".ai-state" / runtime / "orchestrator"
    agents = orch / "agents"
    checkpoints = orch / "checkpoints"

    agents.mkdir(parents=True, exist_ok=True)
    checkpoints.mkdir(parents=True, exist_ok=True)

    (agents / ".gitkeep").touch(exist_ok=True)
    (checkpoints / ".gitkeep").touch(exist_ok=True)

    state_path = orch / "state.json"
    if not state_path.exists():
        state = {
            "version": 1,
            "run_id": f"idle-{runtime}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "goal": f"idle baseline for {runtime} runtime",
            "updated_at": now_iso(),
            "queue": [],
            "active_step_id": None,
            "steps": {},
            "last_decision": "stop",
        }
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    trace_path = orch / "agent_trace.log"
    if not trace_path.exists() or trace_path.read_text(encoding="utf-8").strip() == "":
        bootstrap_trace = {
            "ts": now_iso(),
            "run_id": f"idle-{runtime}",
            "step_id": "S0",
            "agent": "bootstrap",
            "event": "parsed_context",
            "source_actor": runtime if runtime in {"qwen", "codex"} else "agent",
            "request_id": f"bootstrap-{runtime}",
            "summary": f"initialized runtime state for {runtime}",
            "status": "ok",
            "artifacts": [str(state_path)],
        }
        trace_path.write_text(json.dumps(bootstrap_trace, ensure_ascii=False) + "\n", encoding="utf-8")

    watchdog_path = orch / "watchdog.log"
    if not watchdog_path.exists() or watchdog_path.read_text(encoding="utf-8").strip() == "":
        bootstrap_watchdog = {
            "ts": now_iso(),
            "step_id": "S0",
            "event": "init",
            "reason": f"runtime initialized for {runtime}",
            "action": "none",
            "details": "bootstrap event",
        }
        watchdog_path.write_text(json.dumps(bootstrap_watchdog, ensure_ascii=False) + "\n", encoding="utf-8")


def maybe_migrate_legacy(root: Path, runtime: str) -> None:
    legacy = root / ".ai-state" / "orchestrator"
    target = root / ".ai-state" / runtime / "orchestrator"

    if runtime != "qwen" or not legacy.exists():
        return

    target_state = target / "state.json"
    legacy_state = legacy / "state.json"
    if target_state.exists() and legacy_state.exists():
        try:
            target_obj = json.loads(target_state.read_text(encoding="utf-8"))
            if target_obj.get("queue"):
                return
        except Exception:
            pass

    if legacy_state.exists() and not target_state.exists():
        shutil.copy2(legacy_state, target_state)

    for name in ["agent_trace.log", "watchdog.log"]:
        src = legacy / name
        dst = target / name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    for sub in ["checkpoints", "agents"]:
        src_dir = legacy / sub
        dst_dir = target / sub
        if src_dir.exists() and not any(dst_dir.glob("*")):
            for p in src_dir.glob("*"):
                if p.is_file() and p.name != ".gitkeep":
                    shutil.copy2(p, dst_dir / p.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize per-runtime AI state layout")
    parser.add_argument("--runtime", choices=["codex", "qwen", "all"], default="all")
    parser.add_argument("--no-migrate-legacy", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    runtimes = ["codex", "qwen"] if args.runtime == "all" else [args.runtime]

    for runtime in runtimes:
        ensure_runtime(root, runtime)
        if not args.no_migrate_legacy:
            maybe_migrate_legacy(root, runtime)

    print("✅ ai-state runtime layout initialized")


if __name__ == "__main__":
    main()
