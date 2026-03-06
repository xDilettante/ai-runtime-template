#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid JSON in {path}: {exc}")
    raise AssertionError("unreachable")


def validate_jsonl(path: Path, required_fields: list[str] | None = None) -> None:
    if not path.exists():
        fail(f"Missing required file: {path}")

    raw = path.read_text(encoding="utf-8")
    if raw.strip() == "":
        fail(f"{path} is empty; expected JSONL events")

    for n, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            fail(f"{path}:{n} contains blank line; JSONL must be non-empty JSON per line")
        try:
            obj = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            fail(f"{path}:{n} invalid JSON: {exc}")
        if required_fields:
            missing = [k for k in required_fields if k not in obj]
            if missing:
                fail(f"{path}:{n} missing required fields: {', '.join(missing)}")


def main() -> None:
    print(
        "[legacy] .codex/scripts/validate_ai_state.py validates only the pre-split "
        ".ai-state/orchestrator layout. For current codex/qwen runtime roots use "
        "scripts/validate_ai_state_schema.py."
    )
    root = Path(__file__).resolve().parents[2]
    orch = root / ".ai-state" / "orchestrator"
    if not orch.exists():
        print(f"[legacy] skipped: no legacy orchestrator directory at {orch}")
        return

    state_path = orch / "state.json"
    if not state_path.exists():
        print(f"[legacy] skipped: shared directory exists but no legacy state file at {state_path}")
        return

    state = read_json(state_path)
    required_state_keys = {"version", "goal", "updated_at", "queue", "active_step_id", "steps"}
    missing_state = required_state_keys - state.keys()
    if missing_state:
        fail(f"{state_path} missing keys: {', '.join(sorted(missing_state))}")

    queue_ids = {item.get("step_id") for item in state.get("queue", []) if isinstance(item, dict)}

    checkpoints_dir = orch / "checkpoints"
    if not checkpoints_dir.exists():
        fail(f"Missing checkpoints dir: {checkpoints_dir}")
    checkpoint_files = [p for p in checkpoints_dir.glob("*.json")]

    for cp in checkpoint_files:
        obj = read_json(cp)
        for k in ("step_id", "agent", "status", "goal", "updated_at"):
            if k not in obj:
                fail(f"{cp} missing key: {k}")
        step_id = obj["step_id"]
        if queue_ids and step_id not in queue_ids:
            fail(f"{cp} step_id={step_id} not found in state.queue")

    validate_jsonl(
        orch / "agent_trace.log",
        required_fields=["ts", "run_id", "step_id", "agent", "event", "summary", "status"],
    )
    validate_jsonl(
        orch / "watchdog.log",
        required_fields=["ts", "step_id", "event", "reason", "action"],
    )

    print("✅ ai-state validation passed")


if __name__ == "__main__":
    main()
