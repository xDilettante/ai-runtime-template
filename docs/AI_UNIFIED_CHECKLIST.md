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
- [ ] `SUMMARY.md` updated if operator quick-start or repository orientation changed.
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
