# AI Pattern Library

A practical pattern library for implementation, debugging, delivery, and collaboration.

## 1) Problem Translation Patterns
### P1: Bug Reproduction First
- Convert report into deterministic reproduction steps.
- Capture expected vs actual behavior.
- Identify scope of affected components.

### P2: Feature Framing
- Define user value in one sentence.
- Define acceptance criteria with observable outputs.
- Define non-goals to prevent scope drift.

### P3: Refactor Framing
- Define what remains behaviorally identical.
- Define improvement axis (readability, modularity, performance).
- Define rollback path.

## 2) Planning Patterns
### Slicing Pattern A: Interface-first
1. define interface contract
2. wire adapter stub
3. add validation checks
4. implement behavior
5. finalize tests

### Slicing Pattern B: Risk-first
1. identify highest uncertainty
2. build smallest probe
3. validate assumption
4. expand implementation

### Slicing Pattern C: Data-flow-first
1. map input sources
2. define transformations
3. define output sinks
4. add error handling at boundaries

## 3) Coding Patterns
### C1: Guard Clauses
- Prefer early exits for invalid states.
- Reduce deep nesting.

### C2: Small Pure Core + Side-effect Shell
- Move deterministic logic to pure functions.
- Keep side effects in thin wrappers.

### C3: Explicit Conversion Layer
- Parse raw input.
- Validate.
- Convert to domain type.

### C4: Result Envelope
- Return value + error context.
- Keep error surface predictable.

### C5: Dependency Surface Minimization
- Inject only what is required.
- Avoid broad global access.

## 4) Testing Patterns
### T1: Behavior Lock
- Protect intended behavior with regression tests.

### T2: Failure Matrix
- For critical logic, test success + common failure modes + edge boundaries.

### T3: Contract Tests
- Validate public input/output contracts.

### T4: Minimal Fixture Pattern
- Keep fixture setup small.
- Avoid over-mocking internals.

### T5: Stability Runs
- For flaky-sensitive areas, repeat focused runs.

## 5) Debugging Patterns
### D1: Binary Isolation
- Halve suspect area quickly.
- Confirm root boundary with focused probes.

### D2: Event Timeline
- Build event timeline from logs/traces.
- Identify first divergence point.

### D3: Contract Mismatch Scan
- Check assumptions between caller/callee.

### D4: State Snapshot Comparison
- Capture before/after snapshots around suspect operation.

### D5: Deterministic Replay
- Re-run with fixed input and controlled environment.

## 6) Observability Patterns
### O1: Milestone Logs
- Log begin/end of key operations.

### O2: Decision Logs
- Log branch decisions when they change behavior significantly.

### O3: Correlation Keys
- Include request/operation ids.

### O4: Error Context Pack
- operation + input summary + expected next action.

### O5: Quiet Success, Rich Failure
- Keep normal logs concise.
- Keep failures rich and actionable.

## 7) Performance Patterns
### F1: Baseline-then-change
- Measure baseline.
- Apply single optimization.
- Measure delta.

### F2: Hot Path Isolation
- Optimize only hot sections.

### F3: Allocation Awareness
- Avoid repeated heavy allocations in tight loops.

### F4: Cache with Bounds
- Prefer bounded caches with explicit invalidation.

### F5: I/O Batching
- Batch where latency/throughput benefits are real.

## 8) Documentation Patterns
### R1: Change Note
- what changed
- why
- how to verify

### R2: How-to Delta
- update only affected steps

### R3: Troubleshooting Snippets
- include common failure signatures and commands

### R4: Glossary for Team Terms
- define non-obvious terms in one place

### R5: Decision Record Mini-format
- context, options, decision, impact

## 9) Review Patterns
### V1: Risk-first Review
- inspect critical paths first

### V2: Contract-first Review
- verify input/output compatibility

### V3: Failure-path Review
- verify exception/error behavior

### V4: Diff-shape Review
- detect unrelated churn and hidden behavior shifts

### V5: Validation Coverage Review
- verify checks match risk level

## 10) Delivery Patterns
### L1: Small Deliverable Packet
- summary
- evidence
- changed files
- risks
- next actions

### L2: Partial Completion Packet
- completed subset
- blocked subset
- minimal unblock action

### L3: Escalation Packet
- blocker
- proof
- options
- recommendation

### L4: Verification Matrix
- list each check and outcome

### L5: Operational Impact Note
- mention runtime or deployment implications

## 11) Collaboration Patterns
### A1: Ownership-first Tasking
- every subtask has explicit owner

### A2: Output-schema-first Assignment
- define expected result schema before execution

### A3: Evidence-first Merge
- merge subtask outputs only with evidence

### A4: Conflict-Resolution Handshake
- compare facts, rerun focused checks, decide explicitly

### A5: Anti-silent-progress Rule
- periodic visible updates mandatory

## 12) Prompting Patterns for Engineering Agents
### PR1: Bounded Objective Prompt
- objective
- constraints
- acceptance
- output schema

### PR2: Investigation Prompt
- hypothesis list
- evidence required
- stop condition

### PR3: Implementation Prompt
- touched files scope
- forbidden changes
- validation commands

### PR4: Review Prompt
- prioritize bugs/regressions
- require file references
- require risk grading

### PR5: Cleanup Prompt
- remove dead paths
- preserve behavior
- keep diff minimal

## 13) Anti-pattern Catalog
- broad rewrites without acceptance criteria
- hidden breaking changes in unrelated diffs
- overuse of abstractions that hide behavior
- no verification for risky changes
- repeated reruns without updated hypothesis
- shipping undocumented behavior changes
- logging noise without diagnostics
- dead code generated “for future use”
- introducing dependencies without reason
- inconsistent naming within same module

## 14) Decision Matrix Templates
### DM1: Option Compare (short)
- option A: pros/cons
- option B: pros/cons
- recommendation and rationale

### DM2: Risk-weighted Compare
- correctness impact
- maintainability impact
- migration cost
- validation effort

### DM3: Fast-path Compare
- fastest safe route
- robust route
- selected route + fallback

## 15) Quality Bar Templates
### QB1: Low-risk change
- focused checks + concise evidence

### QB2: Medium-risk change
- focused + package checks + risk note

### QB3: High-risk change
- focused + broad checks + rollback note + escalation path

## 16) Incident Response Templates
### IR1: Active failure response
1. contain impact
2. verify current state
3. identify failing boundary
4. propose mitigation
5. run focused validation

### IR2: Post-fix report
- root cause
- fix summary
- validation evidence
- residual risk
- prevention action

## 17) Migration Templates
### MG1: Additive migration
- add new path
- keep old path functional
- migrate callers
- remove old path

### MG2: Flagged migration
- ship behind flag
- shadow validation
- switch default
- cleanup

## 18) Repository Hygiene Templates
### RH1: Template repo hygiene
- remove temp artifacts
- keep demos intentionally documented
- preserve onboarding flow

### RH2: Script hygiene
- deterministic outputs
- clear exit codes
- explicit input requirements

### RH3: Config hygiene
- stable defaults
- environment overrides documented

## 19) Quality Escalation Triggers
- repeated failing checks with same signature
- no reproducible path for claimed fix
- unclear ownership of critical subsystem
- missing runtime capability for required validation
- conflicting evidence across agents

## 20) Compact Decision Examples
- if acceptance met + evidence complete -> continue
- if acceptance failed + clear corrective path -> rerun
- if acceptance blocked by missing data -> escalate
- if objective reached and stable -> stop

## 21) Reusable Check Commands Catalog (generic)
- format checks
- lint/static analysis
- unit tests targeted
- integration tests critical path
- race/stability runs when relevant

## 22) Final Message Pattern Examples
### FM1: Success
- status
- summary
- evidence
- changed files
- residual risks

### FM2: Partial
- completed scope
- blocked scope
- unblock action

### FM3: Blocked
- blocker
- evidence
- options
- recommended decision

## 23) Multi-Agent Merge Checklist
- all subtasks mapped to plan steps
- each claim has artifact reference
- conflicting claims resolved
- duplicate tasks collapsed
- final risk summary consolidated

## 24) Practical Default Heuristics
- choose simpler design unless measurable reason otherwise
- prefer explicit over implicit behavior
- prioritize correctness over speed of typing
- prioritize maintainability over micro-optimizations
- always keep operator handoff actionable

## 25) Appendix: Micro-templates
### Task brief template
- Objective:
- Constraints:
- Acceptance:
- Evidence required:
- Stop condition:

### Debug brief template
- Symptom:
- Reproduction path:
- Suspected boundary:
- Probe commands:
- Confirm/deny criteria:

### Delivery brief template
- What changed:
- Why:
- Validation:
- Risks:
- Next:
