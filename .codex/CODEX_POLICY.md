# Global Agent Policy (Mandatory)

This policy applies to all roles in `.codex/roles/`.

## 1) Truthfulness and evidence
- Never claim success metrics, KPI improvements, coverage gains, reliability rates, or business impact unless backed by explicit evidence from the current run.
- If evidence is missing, state uncertainty clearly and provide a concrete verification step.
- Distinguish facts, assumptions, and recommendations.

## 2) Output quality contract
- Prefer concise, decision-useful outputs.
- Include exact commands/paths/artifacts when reporting technical results.
- For failures, include reproducible steps.
- For implementation/review/verification steps, return machine-parseable JSON
  matching `.ai-state/orchestrator/schemas/step_result.schema.json`.
- If free text is needed, put it under `summary` and `notes` fields only.

## 3) Routing and delegation
- For agent selection/routing tasks, follow mandatory routing contract in coordinator agents.
- Do not select candidates without comparison.
- Validate tool availability and scope fit before assignment.
- Orchestration authority is reserved to the main Codex agent (Chief Coordinator).
- Coordinator/orchestrator roles used as subagents are routing-only advisors; they must not perform nested orchestration control calls.
- One-way cross-runtime bridge is allowed: main Codex may invoke external Qwen worker.
- Reverse bridge is forbidden: Qwen must not invoke Codex runtime.
- Cross-runtime recursion is forbidden (`Codex -> Qwen -> Codex`).
- Run at most one external Qwen worker per top-level turn.

## 4) Safety and scope discipline
- Avoid scope drift; explicitly state in/out of scope.
- Do not mask flaky behavior with sleeps as primary fix.
- Prefer deterministic synchronization and state isolation.

## 5) Completion rules
- A task is not complete if required verification steps were skipped.
- If blocked, return blocker + minimal unblocking action.

## 6) Sequential orchestration (Codex constraint)
- Codex operates agents in sequential mode unless runtime explicitly supports parallelism.
- Main Codex agent builds ordered queues and executes one agent at a time.
- Coordinator/orchestrator subagents may propose queue/routing plans, but execution control remains with main Codex.
- Every step must validate output before handoff.
- Use `CODEX_ORCHESTRATION.md` as mandatory execution playbook.

## 7) Git governance (mandatory)
- By default, roles are NOT allowed to perform git-write operations.
- Git-write operations include: `git commit`, `git push`, `git rebase`,
  `git reset`, `git checkout` (branch/file rewrite), `git cherry-pick`, `git merge`.
- Only `Chief Coordinator` (Codex main agent) or `git-workflow-manager`
  may execute git-write operations.
- Any other role may perform read-only git commands (`git status`, `git diff`, `git log`) when needed.
- Step-level override is allowed only with explicit flag:
  - `allow_git_write=true`
  - default is `allow_git_write=false`
