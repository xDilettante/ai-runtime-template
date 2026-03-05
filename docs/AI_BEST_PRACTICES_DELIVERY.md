# AI Best Practices: Delivery and Review Playbook

This playbook defines high-signal delivery practices for AI-assisted changes.

## 1) Delivery Objectives
- Ship changes that are correct, reviewable, and easy to operate.
- Keep delivery packets concise but complete.
- Minimize reviewer cognitive load.

## 2) Change Narrative
A good delivery includes:
- what changed,
- why it changed,
- how it was validated,
- what risks remain.

## 3) Diff Hygiene
- Keep each change logically cohesive.
- Avoid unrelated formatting churn.
- Keep file moves/renames justified.
- Maintain stable API contracts unless change is explicit.

## 4) Reviewer Experience
- Surface high-risk files first.
- Point reviewers to validation commands.
- Mention assumptions and tradeoffs explicitly.
- Do not bury important behavior changes.

## 5) Verification Packet
Minimum packet:
- commands run,
- outcome summary,
- failing/skipped checks with reason,
- follow-up needed.

## 6) Risk Classification
Classify risk per change:
- low: local internal behavior, tested path.
- medium: cross-component effects, partial checks.
- high: contract or runtime-critical behavior.

## 7) Rollback Readiness
- Keep rollback path obvious.
- Avoid irreversible multi-file changes without checkpoints.
- Prefer additive migrations before destructive cleanup.

## 8) Operational Readiness
- Ensure run instructions are current.
- Ensure config expectations are documented.
- Ensure troubleshooting entry points are visible.

## 9) AI-Generated Diff Review Heuristics
- Inspect for accidental dead code.
- Inspect for hidden global behavior changes.
- Inspect for inconsistent naming and ownership.
- Inspect for silent error swallowing.

## 10) Quality Triggers for Additional Review
Escalate review depth when:
- cross-module contracts changed,
- concurrency behavior changed,
- performance-sensitive path changed,
- test reliability changed.

## 11) Test Evidence Quality
Strong evidence:
- deterministic checks,
- repeated pass for flaky-sensitive areas,
- targeted regression tests for bugfixes.

Weak evidence:
- single broad run without targeted checks,
- passing status without command trace,
- assumptions presented as facts.

## 12) Communication Quality
- Report outcomes in factual language.
- Avoid speculative certainty.
- Keep summary compact, then details.

## 13) Documentation Impact Rules
Update docs when any of these changed:
- setup/launch process,
- environment variables,
- public behavior,
- troubleshooting path,
- team workflow expectations.

## 14) Release-Oriented Checklist
- [ ] behavior validated,
- [ ] risk classified,
- [ ] docs updated where needed,
- [ ] known limitations listed,
- [ ] next step proposed.

## 15) Examples of Good Final Message Shape
- status
- result summary
- evidence highlights
- changed files
- assumptions and risks
- next actions

## 16) Anti-Patterns in Delivery
- oversized summary with no evidence,
- evidence dump with no synthesis,
- hidden breaking behavior in minor change report,
- missing mention of skipped checks.

## 17) Practical Standard for “Done Enough”
A task is done enough when:
- objective and acceptance are met,
- checks are sufficient for risk level,
- residual risk is explicit,
- handoff is actionable.

## 18) Practical Standard for “Not Done”
A task is not done when:
- claim lacks evidence,
- acceptance criteria are unverified,
- result depends on unstated assumptions,
- blockers are not surfaced.
