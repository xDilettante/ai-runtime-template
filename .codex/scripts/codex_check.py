#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tomllib


def fail(msg: str) -> None:
    print(f"❌ {msg}")
    raise SystemExit(1)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    codex = root / ".codex"
    config_path = codex / "config.toml"
    manifest_path = codex / "agents_manifest.toml"
    roles_dir = codex / "roles"

    required_paths = [
        config_path,
        manifest_path,
        roles_dir,
        root / "AGENTS.md",
        root / "CODEX.md",
        codex / "CODEX_POLICY.md",
        codex / "CODEX_ORCHESTRATION.md",
    ]

    for p in required_paths:
        if not p.exists():
            fail(f"Missing required path: {p}")

    with config_path.open("rb") as f:
        config = tomllib.load(f)
    with manifest_path.open("rb") as f:
        manifest = tomllib.load(f)

    agents = config.get("agents", {})
    manifest_agents = manifest.get("agents", {})
    if not isinstance(agents, dict):
        fail("Invalid format: [agents] section is missing or malformed")
    if not isinstance(manifest_agents, dict):
        fail("Invalid format: agents manifest is missing or malformed")

    registered = dict(agents)
    manifest_registered = dict(manifest_agents)
    if not registered:
        fail("No agent roles registered in .codex/config.toml")
    if not manifest_registered:
        fail("No agent roles registered in .codex/agents_manifest.toml")
    if registered != manifest_registered:
        fail("config.toml [agents] section is out of sync with .codex/agents_manifest.toml")

    role_files = {p.stem: p for p in roles_dir.glob("*.toml")}
    missing_files = []
    bad_entries = []

    for name, entry in registered.items():
        if not isinstance(entry, dict):
            bad_entries.append(name)
            continue

        cfg = entry.get("config_file")
        if not cfg:
            bad_entries.append(name)
            continue

        cfg_path = (config_path.parent / cfg).resolve()
        if not cfg_path.exists():
            missing_files.append((name, cfg_path))
            continue

        with cfg_path.open("rb") as rf:
            role_data = tomllib.load(rf)

        instructions = role_data.get("developer_instructions")
        if not isinstance(instructions, str) or not instructions.strip():
            fail(f"Empty or missing developer_instructions in {cfg_path}")

    if bad_entries:
        fail("Invalid role entries in config: " + ", ".join(sorted(bad_entries)))

    if missing_files:
        print("❌ Missing role config files:")
        for name, path in missing_files:
            print(f"   - {name}: {path}")
        raise SystemExit(1)

    registered_names = set(registered.keys())
    role_names = set(role_files.keys())

    extra_role_files = sorted(role_names - registered_names)
    missing_role_files = sorted(registered_names - role_names)

    if extra_role_files:
        print("❌ Unregistered role files in .codex/roles:")
        for name in extra_role_files:
            print(f"   - {name}")
        raise SystemExit(1)

    if missing_role_files:
        print("❌ Registered roles missing corresponding .toml file:")
        for name in missing_role_files:
            print(f"   - {name}")
        raise SystemExit(1)

    ai_validate = root / "scripts" / "validate_ai_state_schema.py"
    if not ai_validate.exists():
        fail(f"Missing AI-state validator: {ai_validate}")
    try:
        subprocess.run([sys.executable, str(ai_validate)], check=True)
    except subprocess.CalledProcessError as exc:
        fail(f"AI-state validation failed with exit code {exc.returncode}")

    print(f"✅ codex-check passed: {len(registered_names)} roles validated")


if __name__ == "__main__":
    main()
