# Release Freeze Pass (2026-03-05)

## Scope
- Remediation cycle after full multi-agent audit.
- Work mode: fix code/docs/configs, do not normalize live `.ai-state` runtime content.

## Applied P0/P1 Fixes
1. `cmd/server`: graceful shutdown now targets active `http.Server`.
2. `cmd/server`: `/vpn/status` no longer returns `private_key` in HTTP response.
3. `cmd/server`: added regression tests for:
   - no `private_key` in response;
   - `Shutdown()` before start;
   - `Shutdown()` on active listener.
4. `.gitignore`: template policy fixed:
   - `.qwen/.codex` versioned;
   - volatile `.ai-state` runtime artifacts ignored (`state.json`, logs, rolling agents/checkpoints).
5. `Makefile`: help text and docker image name aligned (`myvpnservices:latest`).
6. `README` + `STATUS`: baseline policy and remediation status synchronized.

## Verification
1. `go test ./...` — PASS
2. `go vet ./...` — PASS
3. `python3 scripts/validate_ai_state_schema.py` — PASS
4. `python3 .codex/scripts/codex_check.py` — PASS (`131 roles validated`)

## Release Gate
- Current gate: `PARTIAL`

### Remaining blockers
1. Working tree is still not release-clean (`M/??` across many paths).
2. `.ai-state` runtime remains live/mutable in this environment; baseline reset must be done in isolated freeze step.

## Recommended next actions
1. Create isolated release branch/snapshot.
2. Run dedicated `.ai-state` freeze procedure (outside live orchestrator activity).
3. Final docs pass + curated commit set for template release.
