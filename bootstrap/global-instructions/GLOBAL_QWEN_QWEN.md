# Global AI Instructions (Native Entrypoint)

Unified global baseline for Codex and Qwen.
This file is self-contained fallback policy with high-signal operational defaults.

## 1) Role and Priority
- This file defines global fallback behavior.
- Effective priority:
1. system/developer/user runtime instructions
2. project-local native entrypoint (`AGENTS.md` or `QWEN.md`)
3. this global entrypoint
- Project-local instructions override project-specific behavior.

## 2) Global Execution Defaults
- Use explicit `S1..Sn` planning for non-trivial work.
- Default mode: sequential execution.
- Parallel execution only for independent merge-safe subtasks.
- One active decision per step: `continue|rerun|escalate|stop`.

## 3) Intake and Scope Defaults
Before major execution, make explicit:
- objective,
- acceptance,
- constraints,
- non-goals,
- evidence expectation.

Avoid scope drift:
- no unrelated edits during focused tasks,
- no broad refactors without explicit approval.

## 4) Evidence and Validation Defaults
- Do not claim substantial outcomes without run evidence.
- Evidence minimum:
  - command(s),
  - key result summary,
  - touched paths,
  - validation status.
- If checks cannot run, explicitly state reason and residual risk.

Validation depth:
- low risk: focused checks,
- medium risk: focused + adjacent,
- high risk: broader coverage + risk note.

## 5) Engineering Quality Defaults
- Prefer minimal, reversible, scope-safe changes.
- Prefer root-cause fixes over cosmetic churn.
- Keep behavior explicit and predictable.
- Preserve repository conventions unless explicitly requested otherwise.
- Avoid speculative abstraction and dead scaffolding.

## 6) Runtime-State Conflict Avoidance
When both engines work in same repo, use split runtime-state:
- Qwen root: `.ai-state/qwen/orchestrator`
- Codex root: `.ai-state/codex/orchestrator`

Use serialized writes where possible:
- `./scripts/ai_state_with_lock.sh qwen <command...>`
- `./scripts/ai_state_with_lock.sh codex <command...>`

## 7) Git Defaults
- Treat git-write actions as high-impact operations.
- Do not run destructive git operations without explicit user request.
- Keep diffs logically grouped and reviewable.

## 8) Practical Security Defaults
- Never hardcode secrets.
- Never expose secrets in logs/docs/output.
- Validate input at boundaries.
- Keep controls practical and proportional to actual risk.

## 9) Multi-Agent Defaults
- Coordinator owns global objective and final synthesis.
- Specialists own bounded subtasks only.
- No silent work: progress must be visible.
- Repeated non-converging reruns should escalate.

## 10) Output Defaults
For substantive tasks provide:
- `status`
- `summary`
- `evidence`
- `changes`
- `assumptions`
- `risks`
- `next_steps`

## 11) Anti-Patterns
- claims without evidence,
- hidden behavior shifts in unrelated diffs,
- repeated reruns without changed hypothesis,
- finishing high-risk tasks without validation narrative.

## 12) Done Criteria
Task is done when:
- acceptance met (or explicitly re-scoped),
- checks executed (or skipped with rationale),
- evidence attached,
- residual risks listed,
- next action is clear.
