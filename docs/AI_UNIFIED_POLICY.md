# AI Unified Policy

Canonical policy for both Codex and Qwen in this repository.

## 0) Extended Playbooks
- [AI_BEST_PRACTICES_ENGINEERING.md](./AI_BEST_PRACTICES_ENGINEERING.md)
- [AI_BEST_PRACTICES_ORCHESTRATION.md](./AI_BEST_PRACTICES_ORCHESTRATION.md)
- [AI_BEST_PRACTICES_DELIVERY.md](./AI_BEST_PRACTICES_DELIVERY.md)
- [AI_PATTERN_LIBRARY.md](./AI_PATTERN_LIBRARY.md)
- [AI_REVIEW_CATALOG.md](./AI_REVIEW_CATALOG.md)
- [AI_PROMPT_CATALOG.md](./AI_PROMPT_CATALOG.md)
- [AI_DEBUG_PLAYBOOK.md](./AI_DEBUG_PLAYBOOK.md)
- [AI_CHECK_MATRIX.md](./AI_CHECK_MATRIX.md)

## 1) Scope and Priority
- Scope: whole repository.
- Priority order:
1. system/developer/user runtime instructions
2. `AGENTS.override.md` (if present)
3. nearest local entrypoint (`AGENTS.md` or `QWEN.md`)
4. this file
5. runtime adapters and checklists
- More specific directory-level instructions override less specific ones.

## 2) Mission of This Repository
- This repo is a reusable template for AI-assisted engineering.
- The template must remain understandable, reproducible, and easy to fork.

## 3) Operating Protocol
- Use explicit plan `S1..Sn` for non-trivial work.
- Default mode is sequential.
- Step lifecycle:
1. define acceptance criteria
2. execute
3. validate
4. decide (`continue|rerun|escalate|stop`)
- If approval gate appears, set `awaiting_approval` and resume with a real tool action.

## 4) Evidence-First Delivery
- Do not claim a result without evidence from current run.
- Evidence formats:
  - command + key output summary,
  - file path(s) changed/analyzed,
  - test/check status,
  - explicit assumptions/limits.
- If evidence is partial, status must be `partial` or `blocked`.

## 5) Engineering Quality Baseline
- Prefer root-cause fixes over cosmetic patches.
- Keep changes minimal and scoped.
- Keep naming and structure consistent with repository style.
- Avoid hidden side effects.
- If a broad refactor is needed, split into reviewable increments.

## 6) Modularity and Structure
- Keep files focused; avoid overgrown god-files.
- Separate domain logic from delivery/infrastructure concerns.
- Prefer composable units over deeply nested flows.
- For scripts and tooling, prioritize readability over cleverness.

## 7) Validation Strategy
- Run narrow checks first, then broaden confidence.
- Typical order:
1. directly touched unit/component checks
2. package-level checks
3. repo-level checks for release-grade changes
- If checks are skipped, state why and identify risk area.

## 8) Documentation Strategy
- Keep docs and code aligned after meaningful changes.
- Update status artifacts when behavior/process changed:
  - `STATUS.md` for current state,
  - `DEVLOG.md` for historical context,
  - `README.md` for usage impact.
- Prefer short, actionable docs over narrative text walls.

## 9) Git Governance
- Read-only git operations are default for analysis steps.
- Git-write operations are high-impact and should be explicit per step.
- Avoid destructive history rewriting unless user explicitly requested it.
- Do not mix unrelated concerns in one change set.

## 10) Practical Performance Rules
- Prefer predictable behavior over micro-optimizations.
- Optimize only after identifying hot paths.
- Do not introduce complexity unless measurable gain exists.
- Preserve debuggability when tuning performance.

## 11) Reliability Rules
- Avoid flaky fixes based on arbitrary sleeps.
- Prefer deterministic waits and explicit state checks.
- Capture failure context for reruns.
- For repeated failures, escalate with narrowed hypothesis.

## 12) Security Rules (Balanced)
- Never hardcode secrets.
- Keep secrets out of logs and docs.
- Validate input at system boundaries.
- Do not add excessive “security theater”; keep controls practical.

## 13) Collaboration and Agent Discipline
- Coordinator owns the global plan and final synthesis.
- Specialized agents own bounded subtasks only.
- Each subtask response must include outcome + evidence + next decision.
- No silent work: visible progress updates are mandatory.

## 14) Escalation Triggers
Escalate when:
- acceptance criteria fail repeatedly,
- required tool/runtime capability is missing,
- scope ambiguity blocks safe progress,
- architecture-level tradeoff must be chosen by user.

Escalation package must include:
- blocker description,
- evidence collected,
- 1-2 viable options,
- recommended path.

## 15) Output Contract
For substantive tasks, final output should include:
- `status`
- `summary`
- `evidence`
- `changes`
- `assumptions`
- `risks`
- `next_steps`

## 16) Definition of Done
- acceptance criteria met or explicitly re-scoped,
- required checks run (or documented why not),
- evidence attached,
- residual risk listed,
- next step obvious to operator.
