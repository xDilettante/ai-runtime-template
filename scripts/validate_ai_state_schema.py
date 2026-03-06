#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    raise SystemExit(1)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid JSON in {path}: {exc}")
    raise AssertionError("unreachable")


def type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_value(value: Any, schema: dict[str, Any], path: str) -> None:
    expected_type = schema.get("type")
    if expected_type is not None:
        if isinstance(expected_type, list):
            if not any(type_ok(value, t) for t in expected_type):
                fail(f"{path}: expected one of types {expected_type}, got {type(value).__name__}")
        elif not type_ok(value, expected_type):
            fail(f"{path}: expected type {expected_type}, got {type(value).__name__}")

    if "enum" in schema and value not in schema["enum"]:
        fail(f"{path}: value '{value}' is not in enum {schema['enum']}")

    if isinstance(value, str) and "minLength" in schema:
        if len(value) < int(schema["minLength"]):
            fail(f"{path}: string length < minLength {schema['minLength']}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                fail(f"{path}: missing required key '{key}'")

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)

        if additional is False:
            allowed = set(properties.keys())
            extra = [k for k in value.keys() if k not in allowed]
            if extra:
                fail(f"{path}: unexpected keys: {', '.join(extra)}")

        for key, prop_schema in properties.items():
            if key in value:
                validate_value(value[key], prop_schema, f"{path}.{key}")

        if isinstance(additional, dict):
            for key, val in value.items():
                if key not in properties:
                    validate_value(val, additional, f"{path}.{key}")

        min_props = schema.get("minProperties")
        if min_props is not None and len(value) < int(min_props):
            fail(f"{path}: object has fewer than minProperties={min_props}")

    if isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(value, start=1):
                validate_value(item, item_schema, f"{path}[{idx}]")


def validate_json_file(path: Path, schema: dict[str, Any]) -> Any:
    if not path.exists():
        fail(f"Missing required file: {path}")
    data = read_json(path)
    validate_value(data, schema, str(path))
    return data


def validate_jsonl_file(path: Path, schema: dict[str, Any]) -> list[dict[str, Any]]:
    if not path.exists():
        fail(f"Missing required file: {path}")

    raw = path.read_text(encoding="utf-8")
    if raw.strip() == "":
        fail(f"{path} is empty; expected JSONL events")

    rows: list[dict[str, Any]] = []
    for n, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            fail(f"{path}:{n} contains blank line; JSONL must be non-empty JSON per line")
        try:
            obj = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            fail(f"{path}:{n} invalid JSON: {exc}")
        if not isinstance(obj, dict):
            fail(f"{path}:{n} expected JSON object")
        validate_value(obj, schema, f"{path}:{n}")
        rows.append(obj)
    return rows


def validate_runtime(orch: Path, state_schema: dict[str, Any], checkpoint_schema: dict[str, Any], watchdog_schema: dict[str, Any], trace_schema: dict[str, Any]) -> None:
    if not orch.exists():
        fail(f"Missing orchestrator directory: {orch}")

    state_path = orch / "state.json"
    state = validate_json_file(state_path, state_schema)

    checkpoints_dir = orch / "checkpoints"
    if not checkpoints_dir.exists():
        fail(f"Missing checkpoints dir: {checkpoints_dir}")

    checkpoint_files = sorted(p for p in checkpoints_dir.glob("*.json"))
    checkpoints_by_step: dict[str, dict[str, Any]] = {}
    for cp in checkpoint_files:
        obj = validate_json_file(cp, checkpoint_schema)
        checkpoints_by_step[obj["step_id"]] = obj

    queue = state.get("queue", [])
    steps = state.get("steps", {})
    active_step = state.get("active_step_id")

    queue_ids: list[str] = []
    for item in queue:
        step_id = item["step_id"]
        queue_ids.append(step_id)
        if step_id not in steps:
            fail(f"{state_path}: queue step '{step_id}' missing in steps object")

    if active_step is not None and active_step not in steps:
        fail(f"{state_path}: active_step_id '{active_step}' missing in steps")

    if queue_ids:
        if active_step is None:
            fail(f"{state_path}: queue is non-empty but active_step_id is null")
        if active_step != queue_ids[0]:
            fail(f"{state_path}: active_step_id '{active_step}' must match first queue step '{queue_ids[0]}'")

    for step_id, step_state in steps.items():
        cp = checkpoints_by_step.get(step_id)
        if cp and cp.get("status") != step_state.get("status"):
            fail(
                f"checkpoint/status mismatch for {step_id}: "
                f"checkpoint={cp.get('status')} state={step_state.get('status')}"
            )

    validate_jsonl_file(orch / "agent_trace.log", trace_schema)
    validate_jsonl_file(orch / "watchdog.log", watchdog_schema)


def runtime_roots(root: Path, mode: str) -> list[Path]:
    if mode == "all":
        return [root / ".ai-state" / "codex" / "orchestrator", root / ".ai-state" / "qwen" / "orchestrator"]
    if mode == "legacy":
        return [root / ".ai-state" / "orchestrator"]
    return [root / ".ai-state" / mode / "orchestrator"]


def parse_mode() -> str:
    parser = argparse.ArgumentParser(description="Validate AI-state schemas for codex/qwen runtime roots")
    parser.add_argument("--runtime", choices=["all", "codex", "qwen", "legacy"], default=None)
    args = parser.parse_args()

    if args.runtime:
        return args.runtime

    env_runtime = os.getenv("AI_STATE_RUNTIME", "").strip().lower()
    if env_runtime in {"all", "codex", "qwen", "legacy"}:
        return env_runtime

    return "all"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    mode = parse_mode()

    shared = root / "contracts" / "orchestrator" / "schemas"
    if not shared.exists():
        fail(f"Missing shared schemas directory: {shared}")

    state_schema = read_json(shared / "state.schema.json")
    checkpoint_schema = read_json(shared / "checkpoint.schema.json")
    watchdog_schema = read_json(shared / "watchdog.schema.json")
    trace_schema = read_json(shared / "agent_trace.schema.json")

    for orch in runtime_roots(root, mode):
        validate_runtime(orch, state_schema, checkpoint_schema, watchdog_schema, trace_schema)

    print(f"✅ ai-state schema validation passed (runtime={mode})")


if __name__ == "__main__":
    main()
