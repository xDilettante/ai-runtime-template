#!/usr/bin/env python3
"""Verify Codex/Qwen instruction alignment with unified policy."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SUBSTRINGS = {
    "AGENTS.md": [
        "Project AI Instructions (Native Entrypoint)",
        "## 8) Runtime State Isolation (Critical)",
        ".ai-state/codex/orchestrator",
        ".ai-state/qwen/orchestrator",
        "cross-runtime bridge is one-way",
        "Cross-runtime bridge: `Qwen -> Codex` forbidden",
        "ai_state_with_lock.sh",
        "## 12) Operator Quick Patterns",
    ],
    "QWEN.md": [
        "Project AI Instructions (Native Entrypoint)",
        "## 8) Runtime State Isolation (Critical)",
        ".ai-state/codex/orchestrator",
        ".ai-state/qwen/orchestrator",
        "cross-runtime bridge is one-way",
        "Cross-runtime bridge: `Qwen -> Codex` forbidden",
        "ai_state_with_lock.sh",
        "## 12) Operator Quick Patterns",
    ],
    "CODEX.md": [
        "spawn_agent",
        "close_agent",
        "Codex may invoke external Qwen worker as one-way bridge",
        "CODEX_OPERATOR_CHEATSHEET.md",
    ],
    "QWEN_OPERATOR_CHEATSHEET.md": [
        "docs/AI_OPERATOR_CHEATSHEET.md",
    ],
    "CODEX_OPERATOR_CHEATSHEET.md": [
        "docs/AI_OPERATOR_CHEATSHEET.md",
    ],
    "docs/AI_OPERATOR_CHEATSHEET.md": [
        "Base Request Template",
        "Runtime Mapping",
        "One-way cross-runtime bridge",
        "ai_state_with_lock.sh",
    ],
    ".qwen/AGENT_ORCHESTRATION.md": [
        ".ai-state/qwen/orchestrator/state.json",
        ".ai-state/qwen/orchestrator/agent_trace.log",
        ".ai-state/qwen/orchestrator/watchdog.log",
    ],
}

FORBIDDEN_SUBSTRINGS = {
    ".qwen/AGENT_ORCHESTRATION.md": [
        ".ai-state/orchestrator/state.json",
        ".ai-state/orchestrator/agents/<agent>.md",
        ".ai-state/orchestrator/checkpoints/<step_id>.json",
        ".ai-state/orchestrator/agent_trace.log",
        ".ai-state/orchestrator/watchdog.log",
    ],
}


def read(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(rel_path)
    return path.read_text(encoding="utf-8")


def extract_shared_rules(text: str) -> str:
    marker = "## 3)"
    start = text.find(marker)
    if start == -1:
        return ""
    rest = text[start + len(marker) :]
    end = rest.find("\n## ")
    section = rest if end == -1 else rest[:end]
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("-")]
    return "\n".join(lines)


errors: list[str] = []

for rel_path, required in REQUIRED_SUBSTRINGS.items():
    try:
        text = read(rel_path)
    except FileNotFoundError:
        errors.append(f"missing file: {rel_path}")
        continue

    for needle in required:
        if needle not in text:
            errors.append(f"{rel_path}: missing required fragment: {needle!r}")

for rel_path, forbidden in FORBIDDEN_SUBSTRINGS.items():
    try:
        text = read(rel_path)
    except FileNotFoundError:
        errors.append(f"missing file: {rel_path}")
        continue
    for needle in forbidden:
        if needle in text:
            errors.append(f"{rel_path}: forbidden legacy fragment present: {needle!r}")

try:
    agents_text = read("AGENTS.md")
    qwen_text = read("QWEN.md")
    agents_shared = extract_shared_rules(agents_text)
    qwen_shared = extract_shared_rules(qwen_text)
    if not agents_shared or not qwen_shared:
        errors.append("cannot extract shared rules section from AGENTS.md or QWEN.md")
    elif agents_shared != qwen_shared:
        errors.append("AGENTS.md and QWEN.md shared-rules sections differ")
except FileNotFoundError as exc:
    errors.append(f"missing file: {exc}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("✅ ai policy sync check passed")
