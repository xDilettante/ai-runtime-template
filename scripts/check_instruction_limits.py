#!/usr/bin/env python3
"""Check instruction sizes for native Codex/Qwen layout."""

from __future__ import annotations

from collections import deque
from pathlib import Path
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# Codex hard-cap is configurable; fallback default is 64 KiB for this project policy.
CODEX_MAX = int(os.getenv("CODEX_PROJECT_DOC_MAX_BYTES", "65536"))
QWEN_SOFT_MAX = int(os.getenv("QWEN_CONTEXT_SOFT_MAX_BYTES", "65536"))
BUNDLE_MAX = int(os.getenv("AI_INSTRUCTIONS_BUNDLE_MAX_BYTES", "65536"))

FILES = {
    "project_agents": ROOT / "AGENTS.md",
    "project_qwen": ROOT / "QWEN.md",
    "project_codex_adapter": ROOT / "CODEX.md",
    "project_codex_operator": ROOT / "CODEX_OPERATOR_CHEATSHEET.md",
    "project_qwen_operator": ROOT / "QWEN_OPERATOR_CHEATSHEET.md",
    "project_operator_canonical": ROOT / "docs" / "AI_OPERATOR_CHEATSHEET.md",
    "project_policy": ROOT / "docs" / "AI_UNIFIED_POLICY.md",
    "project_checklist": ROOT / "docs" / "AI_UNIFIED_CHECKLIST.md",
    "global_codex_native": Path.home() / ".codex" / "AGENTS.md",
    "global_qwen_native": Path.home() / ".qwen" / "QWEN.md",
}

BUNDLES = {
    "codex_bundle": [
        Path.home() / ".codex" / "AGENTS.md",
        ROOT / "AGENTS.md",
    ],
    "qwen_bundle": [
        Path.home() / ".qwen" / "QWEN.md",
        ROOT / "QWEN.md",
    ],
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

errors: list[str] = []
warnings: list[str] = []


def size(path: Path) -> int:
    return path.stat().st_size


def is_local_link(target: str) -> bool:
    low = target.lower().strip()
    return not (
        low.startswith("http://")
        or low.startswith("https://")
        or low.startswith("mailto:")
        or low.startswith("#")
    )


def resolve_link(source: Path, target: str) -> Path | None:
    cleaned = target.strip().split("#", 1)[0].strip()
    if not cleaned or not is_local_link(cleaned):
        return None

    p = Path(cleaned)
    if p.is_absolute():
        return p if p.exists() else None

    resolved = (source.parent / p).resolve()
    return resolved if resolved.exists() else None


def collect_bundle(roots: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    queue: deque[Path] = deque()

    for root in roots:
        if root.exists():
            queue.append(root.resolve())

    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)

        if current.suffix.lower() != ".md":
            continue

        try:
            text = current.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            warnings.append(f"cannot read {current}: {exc}")
            continue

        for match in LINK_RE.finditer(text):
            target = match.group(1)
            nxt = resolve_link(current, target)
            if nxt is None:
                continue
            if nxt.suffix.lower() == ".md" and nxt not in seen:
                queue.append(nxt)

    return sorted(seen)


print("Instruction size report:")
for name, path in FILES.items():
    if not path.exists():
        warnings.append(f"missing (skip): {name} -> {path}")
        continue

    value = size(path)
    print(f"- {name}: {path} -> {value} bytes")

    if name in {"project_agents", "global_codex_native"} and value > CODEX_MAX:
        errors.append(f"codex native entry too large: {path} ({value} > {CODEX_MAX})")

    if name in {"project_qwen", "global_qwen_native"} and value > QWEN_SOFT_MAX:
        warnings.append(f"qwen native entry above soft limit: {path} ({value} > {QWEN_SOFT_MAX})")

print("\nBundle report (with local markdown links):")
for bundle_name, roots in BUNDLES.items():
    files = collect_bundle(roots)
    total = sum(size(p) for p in files if p.exists())
    print(f"- {bundle_name}: {total} bytes across {len(files)} file(s)")
    for p in files:
        print(f"  - {p} ({size(p)} bytes)")
    if total > BUNDLE_MAX:
        errors.append(f"bundle limit exceeded: {bundle_name} ({total} > {BUNDLE_MAX} bytes)")

if warnings:
    print("\nWarnings:")
    for item in warnings:
        print(f"- {item}")

if errors:
    print("\nErrors:")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("\nOK: instruction limits check passed")
