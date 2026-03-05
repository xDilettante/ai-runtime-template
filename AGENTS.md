# Project AI Instructions (Native Entrypoint)

Unified native entrypoint for Codex and Qwen.
Primary operational policy is intentionally inlined here to minimize dependence on linked docs.

## 1) Scope and Priority
- Scope: entire repository rooted at this file.
- Optional temporary override: `AGENTS.override.md` for current run.
- Effective priority order:
1. runtime system/developer/user instructions
2. local native entrypoint (`AGENTS.md` or `QWEN.md`)
3. secondary helper docs/checklists/adapters

## 2) Repository Mission and Boundaries
- Repository purpose: reusable AI-template for practical engineering execution.
- `xlog` and demo artifacts are intentional and should remain as capability showcase.
- Baseline expectations:
  - deterministic execution paths,
  - evidence-backed outcomes,
  - clear orchestration contract,
  - low-friction handoff for operators.

Scope discipline:
- Change only what is required by task objective.
- Avoid side-quest refactors during focused work.
- If broad changes are needed, split into explicit incremental steps.

## 3) Shared Project Rules
- Use explicit `S1..Sn` plan for non-trivial tasks.
- Default mode: sequential (one active step).
- Parallelism only when tasks are independent and merge-safe.
- All substantial claims must be backed by current-run evidence.
- Prefer minimal, reversible, scope-safe edits.
- Prefer root-cause fixes over cosmetic-only edits.
- Preserve repository conventions unless explicit request says otherwise.
- Keep docs aligned with behavior changes.
- Keep git-write operations explicit and justified.

## 4) Task Intake and Framing
For each meaningful task, make these explicit before major execution:
- objective,
- acceptance criteria,
- constraints,
- non-goals,
- expected evidence.

Intake mini-template:
1. Problem statement
2. Desired behavior
3. Validation target
4. Non-goals

If ambiguity threatens correctness, escalate early with 1-2 concrete options.

## 5) Execution Lifecycle
Step lifecycle:
1. define acceptance for current step
2. execute focused action
3. validate with relevant checks
4. decide `continue|rerun|escalate|stop`

Rules:
- one decision per step,
- one active step in sequential mode,
- rerun only with changed hypothesis/method,
- escalate if blocked by missing capability or unresolved ambiguity.

## 6) Evidence and Validation Rules
No substantial conclusion without evidence from current run.

Evidence should include:
- command(s) executed,
- key output summary,
- touched/analyzed files,
- check/test outcome,
- assumptions and residual risk.

Validation depth guidance:
- low risk: focused checks in touched scope,
- medium risk: focused + adjacent checks,
- high risk: focused + broader checks + rollback note.

If checks are skipped:
- explain exactly why,
- classify risk,
- provide minimal next verification action.

## 7) Engineering Quality Bar
Core engineering rules:
- optimize for readability and maintainability first,
- keep module responsibilities clear,
- keep side effects explicit at boundaries,
- avoid speculative abstraction,
- prefer explicit contracts and explicit failure handling.

Implementation micro-rules:
- use guard clauses to reduce nesting,
- separate parsing/validation/transformation,
- avoid hidden global mutable behavior,
- keep error messages actionable and context-rich,
- preserve deterministic behavior under retry/restart paths.

## 8) Runtime State Isolation (Critical)
To prevent cross-engine conflicts, runtime state is split:
- Qwen runtime root: `.ai-state/qwen/orchestrator`
- Codex runtime root: `.ai-state/codex/orchestrator`

Shared contracts only:
- `.ai-state/orchestrator/schemas`
- `.ai-state/orchestrator/templates`

Write serialization:
- `./scripts/ai_state_with_lock.sh qwen <command...>`
- `./scripts/ai_state_with_lock.sh codex <command...>`

Initialization/validation:
- `make ai-state-init`
- `make ai-validate`

## 9) Multi-Agent Orchestration
Orchestration authority (hard rule):
- only the main runtime agent (top-level Codex/Qwen handling the user turn) may execute orchestration toolchain calls,
- coordinator/orchestrator subagents are advisory-only and must not run nested orchestration.
- cross-runtime bridge is one-way: main Codex may invoke external Qwen worker for delegated tasks.
- reverse bridge is forbidden: main Qwen must not invoke Codex runtime.
- no recursive chain is allowed (`Codex -> Qwen -> Codex`).
- run at most one external Qwen worker per top-level orchestration turn.

Coordinator responsibilities:
- own global objective and step queue,
- assign bounded subtasks,
- normalize evidence,
- synthesize final decision package.

Specialist responsibilities:
- execute bounded scope only,
- return evidence-backed result,
- report blockers immediately.

Orchestration anti-stall:
- avoid silent execution,
- detect stale running steps,
- if approval gate reached, resume via real tool action (not text-only ack),
- log faults and escalate when repeated reruns do not converge.

Subagent lifecycle hygiene:
- close each completed/errored subagent immediately,
- do not accumulate stale finalized agents between runs,
- treat thread-limit errors as hard blockers with explicit recovery action.
- if a coordinator/orchestrator subagent is invoked, use it only for routing output (`selected_agents`, scores, fallback), not for execution control.

## 10) Delivery and Review Rules
Review priorities:
1. correctness/regressions
2. contract compatibility
3. reliability/observability
4. maintainability

Delivery packet must be concise but complete:
- `status`
- `summary`
- `evidence`
- `changes`
- `assumptions`
- `risks`
- `next_steps`

No hidden behavior shifts:
- do not mask significant contract/flow change inside unrelated diffs.

## 11) Git Governance
- treat git-write actions as high-impact,
- no destructive history operations without explicit request,
- keep change sets logically grouped,
- avoid mixing unrelated concerns in one change packet.

## 12) Operator Quick Patterns
Base request shape:
- `Режим`
- `Цель`
- `Шаг`
- `Scope`
- `Acceptance`
- `Ограничения`
- `Действие`

Resume pattern:
- set/confirm `awaiting_approval`,
- continue with real tool call,
- record evidence and next decision.

Anti-stall pattern:
- no pending next-action without tool progress,
- no stale running step beyond watchdog threshold,
- if stalled: fault log -> narrowed rerun or escalation.

## 13) Check Matrix (Inline)
Change types and minimum checks:
- bugfix low risk: targeted tests + lint/static in touched area,
- bugfix medium risk: + adjacent package checks,
- bugfix high risk: + broader suite + rollback note,
- feature low risk: feature tests + usage-doc delta,
- feature medium/high: compatibility checks + explicit migration note,
- refactor behavior-preserving: regression coverage + no-behavior-change statement,
- runtime/config change: startup/config path verification + operator note.

Failure handling:
- clear root cause: fix + rerun focused checks,
- ambiguous failure: isolate boundary + probe + rerun,
- intermittent failure: stability reruns + timing/state investigation.

## 14) Operator Prompt Patterns (Inline)
Implementation prompt should include:
- objective,
- scope boundaries,
- forbidden changes,
- acceptance criteria,
- evidence format.

Review prompt should include:
- severity ordering,
- file references,
- regression risk,
- missing tests,
- release impact.

Escalation prompt should include:
- blocker,
- evidence,
- options,
- recommendation.

## 15) Debug and Reliability Playbook (Inline)
Debug ladder:
1. deterministic reproduction
2. isolate failing boundary
3. validate hypothesis with probe
4. implement minimal fix
5. verify regression coverage

Common root cause buckets:
- contract mismatch,
- boundary validation gap,
- state/timing race,
- environment drift,
- hidden default/config assumption.

Reliability rules:
- avoid blind sleeps as primary stabilization,
- prefer condition-based waiting and explicit state transitions,
- keep failure context rich enough for reruns.

## 16) Performance and Observability (Inline)
Performance:
- measure before tuning,
- optimize hot paths only,
- keep complexity proportional to measurable gains.

Observability:
- log milestone transitions,
- log key branch decisions,
- include operation/request identifiers,
- keep success logs concise and failures actionable.

## 17) Practical Security and Data Handling
- never hardcode secrets,
- never leak secrets in logs/docs/output,
- validate external input at boundaries,
- classify errors as retryable vs terminal where relevant,
- keep security controls practical (no unnecessary theater).

## 18) Documentation and State Hygiene
When behavior/process changes:
- update relevant docs with concrete operational deltas,
- keep quickstart and verification commands accurate,
- keep state/runtime artifacts out of template baseline (except schemas/templates/contracts).

## 19) Anti-Patterns
- broad rewrites without acceptance criteria,
- claims without command/test evidence,
- hidden breaking behavior in unrelated change sets,
- repeated reruns without updated hypothesis,
- “done” without validation for risky changes,
- dependency additions without clear justification.

## 20) Definition of Done
Task is done when:
- acceptance criteria met or explicitly re-scoped,
- relevant checks executed (or justified if skipped),
- evidence attached,
- residual risks listed,
- next action is clear and minimal.

## 21) Additional Inline Runtime Appendix
Codex orchestration mapping (main-agent only):
- `spawn_agent`: create specialist subagent
- `send_input`: assign/follow-up task
- `wait`: await status/result
- `close_agent`: close finalized subagent
- practical runtime cap: up to 6 active subagents in this environment

Coordinator/orchestrator subagent mode:
- allowed: candidate discovery, weighted scoring, routing JSON, handoff packet drafts,
- forbidden: nested `spawn_agent`/`send_input`/`wait`/`close_agent` orchestration control.

Approval-gated rule:
- after approval, continue with real tool progress (no text-only completion).

Daily checklist (combined):
- step result includes evidence (commands/paths/checks),
- no silent progress,
- approval steps transition through explicit resume,
- watchdog/trace artifacts are updated in engine-specific state root.

Watchdog anti-stall policy:
- stall conditions:
  - `next_action_required=true` without tool call,
  - running step without updates beyond threshold window,
  - approval accepted but no resume tool-call.
- recovery:
  - mark orchestration fault,
  - write watchdog event,
  - rerun same scope once,
  - escalate with narrowed scope on repeated fault.

---

## 21) Extended Inlined Reference
The following blocks are inlined intentionally to reduce dependency on external links during runtime.

### 21.1 Inlined Unified Policy Snapshot
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
- `xlog` and demo artifacts stay in place as explicit showcase of current agent capabilities.
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

### 21.2 Inlined Unified Checklist Snapshot
# AI Unified Checklist

## A) Preflight
- [ ] Goal is explicit.
- [ ] Success criteria are explicit.
- [ ] Scope boundaries are explicit.
- [ ] Entry instruction files identified.
- [ ] Risk level classified (low/medium/high).

## B) Planning
- [ ] Plan `S1..Sn` exists.
- [ ] Each step has acceptance criteria.
- [ ] Step dependencies are clear.
- [ ] Fallback exists for risky steps.
- [ ] Escalation condition is defined.

## C) Execution Discipline
- [ ] One active step at a time in sequential mode.
- [ ] Progress updates are visible.
- [ ] Each step yields evidence.
- [ ] Decision captured (`continue|rerun|escalate|stop`).
- [ ] Approval gates resume with real tool action.

## D) Change Quality
- [ ] Change is scoped and minimal.
- [ ] No unrelated edits.
- [ ] Naming/style are consistent.
- [ ] Root-cause addressed where feasible.
- [ ] Side effects reviewed.

## E) Validation
- [ ] Focused checks executed.
- [ ] Broader checks executed when required.
- [ ] Failing checks investigated, not ignored.
- [ ] Skipped checks documented with reason.

## F) Documentation
- [ ] User-facing behavior changes documented.
- [ ] `STATUS.md` updated if project state changed.
- [ ] `DEVLOG.md` updated for significant work.
- [ ] Launch/run commands remain accurate.

## G) Git and Delivery
- [ ] Git-write actions were explicit and justified.
- [ ] No destructive history operation without request.
- [ ] Diff is reviewable and logically grouped.

## H) Result Packaging
- [ ] `status` provided.
- [ ] `summary` concise and factual.
- [ ] `evidence` references concrete artifacts.
- [ ] `assumptions` and `risks` listed.
- [ ] `next_steps` actionable.

### 21.3 Inlined Operator Cheatsheet Snapshot
# AI Operator Cheatsheet

Unified operator cheatsheet for both Codex and Qwen.

## 1) Base Request Template
```text
Режим: Chief Coordinator.
Цель: <что должно быть в итоге>.
Шаг: <S# или "восстанови из .ai-state/<runtime>/orchestrator/state.json">.
Scope: <файлы/модули>.
Acceptance:
1) <критерий 1>
2) <критерий 2>
Ограничения:
- sequential only
- step_result в стандартном формате
- agent_trace обязателен
- allow_git_write=false
Действие: начни выполнение сейчас и обновляй state/checkpoint/trace.
```

## 2) Common Scenarios

### 2.1 Start New Fix Step
```text
Режим: Chief Coordinator.
Цель: исправить <проблема>.
Шаг: S3.
Scope: pkg/xlog/...
Acceptance:
1) тесты проходят
2) регрессий нет
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
Действие: доведи шаг до done или blocked.
```

### 2.2 Resume After Approval
```text
Продолжай по stateful-resume.
Шаг: S2 (awaiting_approval).
Approved: "Да, вноси правки! Используй вариант 1".
Сделай новый tool-call с RESUME_CONTEXT (не text-only).
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
```

### 2.3 Review Step
```text
Режим: Chief Coordinator.
Шаг: S4 review.
Цель: независимая проверка изменений S4.
Acceptance:
1) критичных замечаний нет
2) проверки воспроизводимы
Ограничения:
- read-only git
- step_result обязателен
- agent_trace обязателен
```

### 2.4 Verification Step
```text
Режим: Chief Coordinator.
Шаг: S5 verify.
Цель: подтвердить acceptance критерии проверками.
Команды:
1) <targeted command 1>
2) <targeted command 2>
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
```

### 2.5 Enable Git Write for One Step
```text
Разрешаю git-write только для этого шага.
Шаг: S7.
allow_git_write=true
git_writer=chief_coordinator
Сделай commit после успешных проверок и верни step_result + trace.
```

## 3) Fast Shortcuts

### 3.1 Continue from State
```text
Восстанови план из `.ai-state/<runtime>/orchestrator/state.json` и продолжай следующий незавершенный шаг.
Обязательно: step_result + agent_trace.
```

### 3.2 Force Resume
```text
RESUME S2 APPROVED.
Сделай новый tool-call по RESUME_CONTEXT и продолжай без text-only ответа.
```

### 3.3 Anti-Stall Check
```text
Проверь watchdog условия:
- нет ли шага с next_action_required=true без tool_call
- нет ли timeout > 8 минут
Если есть — выполни auto-recovery и зафиксируй в `.ai-state/<runtime>/orchestrator/watchdog.log`.
```

## 4) Runtime Mapping
- Qwen typical task tool-call: `task` + `RESUME_CONTEXT` on resume.
- Codex typical orchestration calls: `spawn_agent`, `send_input`, `wait`, `close_agent`.
- Orchestration control is main-agent only (top-level Codex/Qwen handling the user turn).
- Coordinator/orchestrator subagents are routing-only advisors (no nested orchestration control).
- Cross-runtime bridge: `Codex -> Qwen` allowed (external worker mode, one worker at a time).
- Cross-runtime bridge: `Qwen -> Codex` forbidden.
- Recursive cross-runtime chains are forbidden.
- Locked write wrapper (recommended): `./scripts/ai_state_with_lock.sh <codex|qwen> <command...>`.

## 5) Avoid These Inputs
- "просто продолжай" без `Шаг` и `Acceptance`.
- "сделай как лучше" без scope/ограничений.
- approval-сообщение без требования нового tool-call.

## 6) Minimum Required Fields
1. `Цель`
2. `Шаг`
3. `Acceptance`
4. `allow_git_write` (обычно `false`)

### 21.4 Inlined Check Matrix Snapshot
# AI Check Matrix

A matrix of recommended checks by change type and risk profile.

## 1) Change Type vs Required Checks
### Bugfix (low risk)
- run targeted unit tests
- run lint/static checks for touched package
- verify reproduction no longer fails

### Bugfix (medium risk)
- all low-risk checks
- run adjacent package tests
- run at least one integration path if affected

### Bugfix (high risk)
- all medium-risk checks
- run broader suite for impacted domain
- add rollback note and residual risk summary

### Feature (low risk)
- feature-specific tests
- docs update for usage impact
- lint/static checks

### Feature (medium risk)
- all low-risk checks
- boundary interaction tests
- compatibility note

### Feature (high risk)
- all medium-risk checks
- migration/compatibility validation
- release-readiness summary

### Refactor (behavior-preserving)
- regression suite for touched behavior
- static checks
- clear no-behavior-change statement

### Build/CI change
- run altered pipeline steps locally if possible
- verify deterministic behavior
- document changed assumptions

## 2) Check Depth Policy
- low risk: focused checks only
- medium risk: focused + adjacent checks
- high risk: focused + adjacent + broad checks

## 3) Failure Handling Matrix
### Check fails with clear root cause
- fix and rerun only affected checks first

### Check fails with ambiguous cause
- isolate failing boundary
- add probe logs/tests
- rerun focused checks

### Check fails intermittently
- run stability repeats
- inspect timing/state assumptions
- avoid sleep-based masking

## 4) Evidence Matrix
For each check capture:
- command
- outcome
- key output line(s)
- interpretation

## 5) Risk Matrix for Common Changes
### API contract change
- risk: high
- required: compatibility review, migration note, contract tests

### Config default change
- risk: medium/high
- required: startup behavior verification, docs update

### Parsing/validation change
- risk: medium
- required: boundary tests with invalid/edge inputs

### Concurrency change
- risk: high
- required: race/stability checks and deterministic assertions

### Logging-only change
- risk: low/medium
- required: lint/build; verify no secret leakage

## 6) Docs Matrix
### Behavior changed
- update user-facing docs

### Runtime command changed
- update README/how-to

### Config key changed
- update reference docs and examples

### Workflow changed
- update STATUS/DEVLOG where applicable

## 7) Delivery Matrix
### success
- include full evidence packet

### partial
- include completed scope + blocked scope + next unblock action

### blocked
- include blocker proof + options + recommendation

## 8) Merge Matrix (Multi-agent)
- verify ownership of each step output
- deduplicate overlapping claims
- resolve contradictions with reruns
- keep only evidence-backed statements

## 9) Practical Thresholds
- if no checks run, result cannot be full success for non-trivial change
- if high-risk path changed, broad validation is expected
- if assumptions are critical, mark them explicitly in final report

## 10) Minimal Check Sets by Task Class
### Documentation-only
- link/format sanity

### Small internal logic fix
- targeted tests + lint

### Cross-module behavior change
- targeted + adjacent tests + docs update

### Infrastructure/runtime behavior change
- targeted + broad checks + operator note

## 11) Operator-Facing Output Matrix
- Always provide:
  - what changed,
  - what passed,
  - what was not run,
  - why,
  - what to do next.

## 12) Escalation Matrix
Escalate when:
- validation cannot be completed due missing capability,
- risk too high for current evidence,
- conflicting acceptance criteria,
- architectural choice required.

Escalation output:
- blocker
- evidence
- options
- recommended option

### 21.5 Inlined Review Catalog Snapshot
# AI Review Catalog

A practical catalog for deep code review and release-readiness checks.

## 1) Review Entry Questions
- What behavior changes?
- What contracts change?
- What can break silently?
- What evidence exists for correctness?

## 2) Severity Model
- Critical: data loss, security break, production outage potential.
- High: functional regression on key user flow.
- Medium: correctness edge cases, partial failures.
- Low: maintainability/readability concerns.

## 3) Functional Review Checklist
- Inputs validated correctly.
- Output contract preserved.
- Error paths return useful context.
- State transitions are legal and complete.
- Retry/backoff semantics are sensible.

## 4) Boundary Review Checklist
- External API calls handle failures.
- File/network/process boundaries are validated.
- Timeouts and cancellations are respected.
- Partial failures are surfaced, not hidden.

## 5) Data Integrity Checklist
- No silent truncation or corruption paths.
- Serialization/deserialization contracts are aligned.
- Migrations preserve backward compatibility where required.
- Idempotency assumptions are documented.

## 6) Concurrency Checklist
- Shared mutable state access is controlled.
- Race-prone branches are tested where possible.
- Deadlock-prone lock ordering is avoided.
- Cancellation path does not leak resources.

## 7) Observability Checklist
- Failure logs include actionable context.
- Success logs are concise and non-noisy.
- Key operations have traceable identifiers.
- Operator can diagnose common failures quickly.

## 8) Performance Checklist
- Hot path changed? If yes, evidence included.
- Algorithmic complexity shifts are justified.
- Memory-intensive paths reviewed for allocation churn.
- Added latency sources measured or bounded.

## 9) Security Checklist (Practical)
- No hardcoded credentials.
- Sensitive values not exposed in logs.
- Input boundaries validated.
- Access checks are explicit where relevant.

## 10) Test Adequacy Checklist
- Core behavior covered by tests.
- Bugfix includes regression protection.
- Failure mode coverage exists for critical path.
- Flaky tests are identified and addressed.

## 11) Diff Hygiene Checklist
- No unrelated changes mixed in.
- Renames/moves justified and scoped.
- Generated files controlled.
- Formatting-only churn minimized.

## 12) Documentation Checklist
- Changed behavior reflected in docs.
- Run/verify instructions still accurate.
- New flags/configs documented.
- Known limits/risks explicitly noted.

## 13) Release Readiness Checklist
- Acceptance criteria met.
- Validation evidence attached.
- Risk class assigned.
- Rollback or mitigation path stated.
- Follow-up tasks identified.

## 14) Reviewer Comment Templates
### Bug-risk template
- Finding:
- Why risky:
- Evidence:
- Suggested fix:

### Regression-risk template
- Finding:
- Impacted behavior:
- Repro path:
- Suggested test:

### Test-gap template
- Gap:
- Risk:
- Minimal test needed:

### Maintainability template
- Concern:
- Long-term cost:
- Minimal refactor option:

## 15) Common Bug Patterns to Scan
- off-by-one boundaries
- nil/null unchecked branches
- stale cache invalidation gaps
- race on shared state
- swallowed errors
- mismatch between docs and behavior
- timeout not propagated
- retries without jitter/limits
- hidden global mutable state
- resource leak on early return

## 16) Regression Hotspots
- initialization sequence changes
- config parsing and defaults
- feature flag transitions
- migration scripts and adapters
- retry/circuit behavior

## 17) API Contract Review
- request/response schema changes flagged
- backward compatibility decision explicit
- versioning strategy respected
- error contract consistency maintained

## 18) CLI/Operator UX Review
- command behavior predictable
- error messaging actionable
- help text aligned with behavior
- defaults safe and documented

## 19) Infrastructure/Runtime Review
- environment assumptions explicit
- external dependencies declared
- startup/shutdown behavior deterministic
- resource limits respected

## 20) Final Review Packet Template
- Findings by severity
- Open questions
- Validation summary
- Residual risk
- Recommendation

## 21) “No Findings” Standard
If no findings:
- explicitly state no findings,
- list tested coverage scope,
- list residual blind spots.

## 22) Escalation Thresholds
Escalate when:
- critical/high finding unresolved,
- validation cannot be executed,
- contract change has unclear migration,
- cross-team dependency unresolved.

## 23) Review Exit Criteria
- Critical findings resolved or accepted with reason.
- High findings resolved or tracked with owner.
- Validation evidence sufficient for risk level.

## 24) Reviewer Timeboxing
- first pass: correctness and risk hotspots
- second pass: maintainability and docs
- third pass: polish and consistency

## 25) Practical Review Heuristics
- trust evidence more than narrative
- prioritize user-visible behavior paths
- prefer small safe fixes over large uncertain rewrites
- enforce explicit assumptions
