# STATUS

- Template: `ai-runtime-template`
- Scope: AI infrastructure only (Codex + Qwen)
- Runtime code: excluded by design
- Release state source of truth: this file
- Maturity: `operator-tested`
- State: operator-tested template baseline
- Release gate: `fork-ready`
- Notes:
  - shared runtime contracts are versioned in `contracts/orchestrator`
  - legacy release/audit notes remain only as archival context
  - safe Codex defaults and reversible bootstrap flow are in place

## Readiness checklist

- [x] Codex and Qwen entrypoint instructions are present
- [x] Agent catalogs for both engines are present
- [x] Policy and orchestration docs are present
- [x] Validation scripts are present
- [x] Runtime artifacts and binaries are excluded
- [x] Clean-clone quick start is self-contained
- [x] Versioned contracts are separate from generated runtime-state
- [x] Release notes and status docs are fully synchronized
- [x] Legacy Go/xlog references are removed from template-facing docs
