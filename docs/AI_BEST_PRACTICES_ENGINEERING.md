# AI Best Practices: Engineering Playbook

This playbook defines practical high-signal engineering guidance for AI-driven implementation.

## 1) Task Intake and Framing
- Convert user intent into a concrete objective with measurable acceptance criteria.
- Identify explicit constraints: scope, timeline, runtime limitations, compatibility needs.
- Identify implicit constraints: existing style, toolchain, deployment assumptions.
- Rewrite ambiguous goals into testable statements.

### Intake template
1. Problem statement: what is currently wrong or missing.
2. Desired behavior: what must be true after implementation.
3. Validation target: how success is measured.
4. Non-goals: what should not be changed.

## 2) Solution Scoping
- Prefer the smallest viable change set that solves the objective.
- Separate mandatory scope from optional enhancements.
- Avoid coupling implementation to speculative future requirements.

### Scope slicing patterns
- Vertical slice: one complete user-visible scenario.
- Interface-first slice: contract + adapter + tests.
- Risk-first slice: validate highest-risk assumption first.
- Compatibility-first slice: preserve behavior; add capabilities behind flags.

## 3) Design Quality
- Keep design explicit: data flow, state transitions, failure paths.
- Choose deterministic behavior over hidden magic.
- Isolate side effects at boundaries.
- Keep interfaces narrow and intention-revealing.

### Design checklist
- Are responsibilities clearly separated?
- Can each component be tested independently?
- Are error paths explicit and observable?
- Is rollback/partial-failure behavior defined?

## 4) Implementation Strategy
- Start from existing patterns in repository.
- Prefer clarity over density.
- Avoid introducing broad abstractions too early.
- Preserve readability under time pressure.

### Implementation micro-rules
- Write code that is easy to review line-by-line.
- Prefer explicit names over short cryptic names.
- Keep conditionals shallow when possible.
- Use small helper functions for repeated logic.

## 5) State and Data Handling
- Keep mutable state localized.
- Validate external input at boundaries.
- Normalize data close to source.
- Separate parsing, validation, and domain transformation.

### Data contracts
- Define expected shapes and invariants.
- Fail fast on invalid contracts.
- Use stable defaults where appropriate.
- Keep conversion logic explicit and testable.

## 6) Error Handling
- Error messages should be actionable.
- Include context needed for diagnosis.
- Avoid swallowing errors silently.
- Distinguish retryable and terminal failures.

### Error message template
- What failed.
- In what operation/context.
- What operator/developer can do next.

## 7) Testing Philosophy
- Test behavior, not implementation details.
- Prioritize tests that protect against regressions.
- Use focused unit tests for core logic.
- Use integration tests for critical interaction boundaries.

### Test writing rules
- One main assertion intent per test.
- Arrange -> Act -> Assert structure.
- Clear test names describing behavior.
- Minimal mocking; mock only true boundaries.

### Regression policy
- Bug fix should include a regression test when practical.
- New behavior should include at least one behavior lock test.
- Flaky tests must be stabilized or quarantined with reason.

## 8) Performance and Resource Use
- Optimize after identifying bottlenecks.
- Measure before and after changes.
- Avoid complex optimizations without observed need.
- Keep memory and CPU behavior predictable.

### Performance checklist
- Is there a baseline metric?
- Is improvement measurable?
- Is complexity cost acceptable?
- Is debuggability preserved?

## 9) Observability and Diagnostics
- Log meaningful milestones and failure points.
- Include identifiers for tracing operations.
- Avoid noisy logs with low diagnostic value.
- Keep log output consistent with environment expectations.

### Good diagnostic signals
- operation id
- duration
- result status
- key branch decision
- non-sensitive input summary

## 10) Refactoring Discipline
- Refactor only with clear payoff.
- Keep behavior unchanged unless explicitly intended.
- Break large refactors into staged commits/steps.
- Validate each stage independently.

### Refactor patterns
- Extract function for repeated branch logic.
- Encapsulate boundary calls behind adapter.
- Replace condition chains with table-driven mapping.
- Reduce coupling by explicit dependency injection.

## 11) Compatibility and Migration
- Preserve existing public contracts unless change is requested.
- If contract changes are required, provide migration notes.
- Prefer additive changes to breaking changes.
- Mark transitional behavior clearly.

## 12) Documentation Quality
- Update docs only where behavior changed.
- Keep docs concise and runnable.
- Prefer examples that can be copied and executed.
- Remove stale examples quickly.

### Documentation minimum
- What changed.
- Why it changed.
- How to run/verify.
- Known limits.

## 13) Review Readiness
- Ensure diff is coherent and reviewable.
- Include intent and constraints in summary.
- Highlight risky areas.
- Provide command evidence for verification.

### Review bundle
- change summary
- key files
- checks executed
- assumptions and risks
- suggested follow-up

## 14) AI-specific Coding Guidance
- Avoid over-generation: do not produce dead code.
- Avoid broad speculative scaffolding.
- Keep generated code aligned to repository idioms.
- Prefer deterministic edits over mass rewrites.

### AI generation anti-patterns
- unnecessary framework wrappers
- giant utility files without ownership
- hidden behavior behind implicit defaults
- introducing new dependencies without justification

## 15) Practical Tradeoff Framework
When choosing between options, evaluate:
- correctness impact
- maintainability impact
- validation cost
- runtime cost
- migration cost

### Decision output format
- option chosen
- reasons
- rejected alternatives
- validation plan

## 16) Do/Don't Summary
### Do
- Keep scope small and explicit.
- Validate with evidence.
- Communicate assumptions.
- Keep architecture understandable.

### Don't
- Ship unverified claims.
- Hide risky changes in large diffs.
- Overfit to edge cases without data.
- Create complexity without measurable value.
