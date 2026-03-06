#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import tomllib


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / ".codex" / "config.toml"
MANIFEST_PATH = ROOT / ".codex" / "agents_manifest.toml"

AGENTS_MARKER = "\n[agents]\n"
GENERATED_HEADER = "[agents]\n# Generated from .codex/agents_manifest.toml via .codex/scripts/generate_codex_config.py.\n\n"


def load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def render_agents(agents: dict[str, dict[str, str]]) -> str:
    parts: list[str] = []
    for name in sorted(agents):
        entry = agents[name]
        description = entry["description"].replace("\\", "\\\\").replace('"', '\\"')
        config_file = entry["config_file"].replace("\\", "\\\\").replace('"', '\\"')
        parts.append(f'[agents."{name}"]\n')
        parts.append(f'description = "{description}"\n')
        parts.append(f'config_file = "{config_file}"\n\n')
    return "".join(parts)


def build_config_text(current_text: str, agents: dict[str, dict[str, str]]) -> str:
    if AGENTS_MARKER not in current_text:
        raise SystemExit(f"Missing [agents] section in {CONFIG_PATH}")
    prefix, _ = current_text.split(AGENTS_MARKER, 1)
    return prefix + "\n" + GENERATED_HEADER + render_agents(agents)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate .codex/config.toml [agents] section from manifest")
    parser.add_argument("--check", action="store_true", help="fail if config.toml is not in sync")
    args = parser.parse_args()

    config_text = CONFIG_PATH.read_text(encoding="utf-8")
    manifest = load_toml(MANIFEST_PATH)
    agents = manifest.get("agents")
    if not isinstance(agents, dict) or not agents:
        raise SystemExit(f"Invalid or empty agents manifest: {MANIFEST_PATH}")

    rendered = build_config_text(config_text, agents)

    if args.check:
        if rendered != config_text:
            raise SystemExit("config.toml is out of sync with agents_manifest.toml")
        print("✅ codex config is in sync with agents manifest")
        return

    CONFIG_PATH.write_text(rendered, encoding="utf-8")
    print(f"✅ regenerated {CONFIG_PATH} from {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
