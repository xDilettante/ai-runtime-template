# AI Prompt Catalog

Reusable prompt templates for engineering coordination and execution.

## 1) Task Clarification Prompt
Use when request is ambiguous but implementation is expected.

Template:
- Objective:
- Current state:
- Desired state:
- Constraints:
- Acceptance criteria:
- Out-of-scope:
- Evidence required:

## 2) Scoped Implementation Prompt
Template:
- Implement only in files:
- Do not touch:
- Preserve behavior for:
- Add tests for:
- Validation commands:
- Output format:

## 3) Bug Investigation Prompt
Template:
- Symptom:
- Repro command:
- Expected vs actual:
- Suspected layers:
- Required artifacts:
- Stop when:

## 4) Regression Fix Prompt
Template:
- Broken behavior:
- Known good behavior:
- Repro coverage:
- Minimal fix strategy:
- Regression test requirement:

## 5) Refactor Prompt
Template:
- Keep behavior unchanged.
- Improve only these dimensions:
- Forbidden changes:
- Validation coverage:
- Handoff summary required:

## 6) Review Prompt (Bug-focused)
Template:
- Prioritize correctness and regressions.
- Provide findings ordered by severity.
- Include file references.
- Include missing tests and risks.

## 7) Review Prompt (Release gate)
Template:
- Check contract changes.
- Check migration implications.
- Check rollback readiness.
- Check observability and docs alignment.

## 8) Multi-Agent Tasking Prompt
Template:
- Step id:
- Owner role:
- Goal:
- Constraints:
- Acceptance:
- Output schema:
- Timeout:

## 9) Coordinator Merge Prompt
Template:
- Collect all step outputs.
- Deduplicate claims.
- Map each claim to evidence.
- Resolve conflicts explicitly.
- Produce final package.

## 10) Escalation Prompt
Template:
- Blocker summary:
- Why blocked:
- Evidence:
- Options:
- Recommended option:

## 11) Validation Prompt
Template:
- Run focused checks first.
- Expand checks based on risk.
- Report pass/fail/skipped with reason.

## 12) Performance Tuning Prompt
Template:
- Baseline metric:
- Hot path candidate:
- Single optimization:
- Measure delta:
- Keep/rollback decision:

## 13) Documentation Update Prompt
Template:
- Behavior changed:
- Docs impacted:
- Update targets:
- Verification steps for docs:

## 14) Config Hygiene Prompt
Template:
- New configs introduced:
- Defaults and rationale:
- Environment-specific behavior:
- Migration note:

## 15) Reliability Prompt
Template:
- Failure mode:
- Trigger conditions:
- Detection signal:
- Mitigation strategy:
- Follow-up hardening:

## 16) Artifact Extraction Prompt
Template:
- Extract commands run.
- Extract key outputs only.
- Extract changed files.
- Extract open risks.

## 17) Decision Prompt
Template:
- Option A: pros/cons
- Option B: pros/cons
- Recommendation:
- Rejected option rationale:

## 18) Minimal Change Prompt
Template:
- Solve objective with minimal diff.
- Avoid broad refactor.
- Preserve interfaces.
- Add only critical tests.

## 19) Safety-Not-Theater Prompt
Template:
- Apply practical safeguards only.
- Avoid excessive non-functional hardening for this task.
- Keep solution maintainable.

## 20) Structured Final Output Prompt
Template:
- status:
- summary:
- evidence:
- changes:
- assumptions:
- risks:
- next_steps:

## 21) Prompt Anti-Patterns
- vague “improve everything” objective
- missing acceptance criteria
- no constraints on touched files
- no validation expectations
- no output schema

## 22) Prompt Quality Checklist
- objective is concrete
- constraints are explicit
- acceptance is testable
- evidence is required
- scope is bounded
- ownership is clear

## 23) Domain Adapters
### Backend adapter prompt snippet
- emphasize API contracts
- emphasize validation at boundaries
- emphasize observability

### CLI adapter prompt snippet
- emphasize deterministic output
- emphasize actionable errors
- emphasize compatibility

### Data pipeline adapter prompt snippet
- emphasize data quality checks
- emphasize idempotency
- emphasize retry semantics

## 24) Template for New Project Bootstrap
- establish folder structure
- create baseline checks
- add README quickstart
- add status/devlog files
- add policy/checklist files

## 25) Template for Legacy Modernization
- inventory current behavior
- lock behavior with tests
- stage migration in safe slices
- preserve rollback points

## 26) Template for Incident Stabilization
- contain blast radius
- gather evidence
- apply minimal mitigation
- validate recovery
- document follow-up

## 27) Template for Dependency Updates
- define update scope
- assess break risk
- run targeted compatibility checks
- summarize upgrade notes

## 28) Template for CI/Tooling Changes
- define pipeline impact
- verify local equivalence
- capture runtime delta
- provide fallback path

## 29) Template for Cross-team Handoff
- problem context
- exact changes
- expected outcomes
- known limitations
- owner for follow-up

## 30) Prompt Evolution Pattern
- start with minimal prompt
- run one iteration
- identify ambiguity
- tighten constraints
- rerun with improved prompt
