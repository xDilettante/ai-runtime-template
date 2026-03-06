# STATUS

- Template: `ai-runtime-template`
- Scope: AI infrastructure only (Codex + Qwen)
- Runtime code: excluded by design
- Release state source of truth: this file
- State: truth-synced and template-hardened baseline
- Release gate: `ready`
- Notes:
  - shared `.ai-state` contracts are versioned in-repo
  - legacy release/audit notes remain only as archival context
  - safer Codex defaults and reversible bootstrap flow are in place

## Readiness checklist

- [x] Codex and Qwen entrypoint instructions are present
- [x] Agent catalogs for both engines are present
- [x] Policy and orchestration docs are present
- [x] Validation scripts are present
- [x] Runtime artifacts and binaries are excluded
- [x] Clean-clone quick start is self-contained
- [x] Release notes and status docs are fully synchronized
- [x] Legacy Go/xlog references are removed from template-facing docs
