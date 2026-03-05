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
