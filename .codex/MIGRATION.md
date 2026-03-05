# Codex Agent Migration Notes

This project now uses an official Codex multi-agent baseline:
- `./.codex/config.toml`
- `./.codex/roles/*.toml`

## Current migration state
- `./.codex/roles/*.toml` is the single source of truth.
- Legacy markdown role library was removed.
- Role instructions are now maintained directly in TOML `developer_instructions`.

## Runtime registration
- `./.codex/config.toml` registers all roles in `[agents."<name>"]`.
- Each registration points to `config_file = ".codex/roles/<name>.toml"`.

## Operating mode
- Default execution remains sequential (one active orchestration step) for deterministic handoffs.
- Runtime thread cap in this environment is 6 active subagents (`max_threads = 6` in config).
- Increase concurrency only when runtime capabilities and task safety allow it.
