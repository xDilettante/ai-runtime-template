# Codex Agents Audit (2026-03-04)

## Official structure (from OpenAI Codex sources)

1. Agent registry entries under `[agents.<name>]` support only:
- `description`
- `config_file`
- `nickname_candidates`

2. Per-role file referenced by `config_file` is a full config profile layer.
- It can set model/runtime fields like `model`, `model_reasoning_effort`,
  `approval_policy`, `sandbox_mode`, etc.

3. Relevant official enums in Codex config schema:
- `approval_policy`: `untrusted`, `on-failure`, `on-request`, `never`
- `sandbox_mode`: `read-only`, `workspace-write`, `danger-full-access`

Sources:
- https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json
- https://raw.githubusercontent.com/openai/codex/main/README.md

## Comparison with current repo (before fix)

1. `.codex/config.toml` used valid `[agents.<name>]` structure with `description/config_file`.
2. Coordinator role files had only `developer_instructions`, with no explicit runtime fields:
- no pinned `model`
- no explicit `approval_policy`
- no explicit `sandbox_mode`
3. Coordinator instructions were long and generic, with weak anti-hang behavior
   for `approval needed` / stalled `running` states.

## Why orchestration stalled

Primary causes:
1. Approval flow deadlock:
- spawned agent requested approval/question,
- coordinator reported text status but did not enforce a mandatory `NEW task-call`
  with resume context.

2. Missing anti-stall control:
- no strict timeout rule for `running` without active tool progress,
- no deterministic recovery branch (`rerun/escalate/stop`) after timeout.

3. Runtime defaults were implicit:
- behavior depended on environment defaults instead of explicit per-role settings.

## Applied fixes

1. Added explicit runtime fields to coordinator roles:
- `.codex/roles/multi-agent-coordinator.toml`
- `.codex/roles/workflow-orchestrator.toml`
- `.codex/roles/task-distributor.toml`
- `.codex/roles/agent-organizer.toml`

Fields added:
- `model = "gpt-5-codex"`
- `model_reasoning_effort = "high|medium"`
- `approval_policy = "never"`
- `sandbox_mode = "workspace-write"`

2. Added hard run-control rules (multi-agent/workflow orchestrators):
- set `awaiting_approval` when approval is needed,
- after approval always do a new tool call with `RESUME_CONTEXT`,
- recover if no progress for 120s,
- never keep stale `running` without active job.

3. Added explicit top-level runtime defaults in `.codex/config.toml`:
- `model`, `model_reasoning_effort`, `approval_policy`, `sandbox_mode`
- `max_threads`, `max_depth`, `job_max_runtime_seconds`

## Validation

Commands:
- `python3 ./.codex/scripts/codex_check.py`
- `python3 ./scripts/validate_ai_state_schema.py`

Result:
- passed

