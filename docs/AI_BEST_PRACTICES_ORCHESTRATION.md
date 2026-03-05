# AI Best Practices: Orchestration Playbook

This playbook defines practical orchestration rules for coordinator + specialist agents.

## 1) Coordinator Responsibilities
- Own global objective and success criteria.
- Own step plan `S1..Sn` and transitions.
- Assign bounded subtasks to specialists.
- Collect and normalize evidence into final answer.

### Coordinator must ensure
- no silent progress gaps,
- no undefined ownership,
- no ambiguous completion claims.

## 2) Specialist Responsibilities
- Execute only assigned bounded scope.
- Return concrete evidence.
- Report blockers immediately.
- Avoid hidden side work outside assigned task.

## 3) Task Decomposition
Use decomposition when:
- work spans distinct skill domains,
- independent subtasks can run safely,
- verification paths are separable.

Avoid decomposition when:
- task is small and tightly coupled,
- merge overhead exceeds implementation cost,
- context transfer risk is high.

## 4) Step Contract
Each step should include:
- objective,
- acceptance criteria,
- constraints,
- owner,
- evidence requirement,
- fallback path.

### Example
- objective: stabilize test flake in package X
- acceptance: test suite passes 5/5 runs
- constraints: no API contract changes
- owner: verifier agent
- evidence: command outputs + changed files

## 5) Progress Cadence
- For long tasks, publish short periodic updates.
- Update after major transition: discovery -> edit -> validate -> report.
- Highlight blockers immediately.

## 6) Decision Discipline
Only one decision per step:
- `continue`
- `rerun`
- `escalate`
- `stop`

### Decision criteria
- continue: acceptance met.
- rerun: acceptance not met but path is clear.
- escalate: blocked by ambiguity/capability/scope conflict.
- stop: objective complete or intentionally paused.

## 7) Parallel Work Rules
- Use parallelism only for independent subtasks.
- Define merge owner before starting.
- Ensure each branch has independent validation.
- Resolve conflicts with explicit precedence rules.

## 8) Evidence Normalization
Evidence should be normalized by coordinator:
- deduplicate repeated claims,
- remove contradictory statements,
- mark uncertain findings,
- map each claim to artifact.

## 9) Failure Handling
When a step fails:
1. capture failure signature,
2. classify probable root cause,
3. decide rerun vs escalate,
4. narrow scope for retry.

## 10) Re-run Policy
A rerun should include a changed hypothesis or changed method.
- Avoid repeating the same failed command sequence without new reasoning.
- Cap repeated reruns and escalate early.

## 11) Escalation Package
Escalation should include:
- what is blocked,
- why current tools/path cannot resolve,
- what data is missing,
- recommended options with tradeoffs.

## 12) Coordinator Reporting Format
- status
- summary
- evidence
- changes
- assumptions
- risks
- next steps

## 13) Quality Gates by Phase
### Discovery gate
- scope clarity confirmed,
- relevant files identified,
- risk hotspots listed.

### Implementation gate
- changes scoped,
- no unrelated modifications,
- style consistency preserved.

### Validation gate
- focused checks executed,
- evidence captured,
- failures triaged.

### Delivery gate
- concise result summary,
- risks explicit,
- actionable next step.

## 14) Anti-Stall Rules
- If no progress signal for 120s on active step, force checkpoint update.
- If repeated ambiguous failures, escalate rather than looping.
- Keep decision state explicit at all times.

## 15) Multi-Agent Communication Style
- Be explicit, not verbose.
- State ownership and expected output schema.
- Prefer actionable requests over open-ended asks.

## 16) Hand-off Template
- step id
- goal
- acceptance
- constraints
- artifacts expected
- deadline/timeout
- fallback if blocked

## 17) Conflict Resolution
If agents disagree:
- compare evidence quality,
- favor reproducible findings,
- rerun focused validation when needed,
- choose lowest-risk path that meets objective.

## 18) Cost and Latency Control
- Do not spawn specialists for trivial tasks.
- Prefer one high-signal specialist over many noisy agents.
- Close completed agents to reduce coordination overhead.

## 19) Practical Governance
- Keep runtime adapters thin.
- Keep policy centralized.
- Keep checklists operational.
- Keep validation scripts deterministic.

## 20) Orchestration Do/Don't
### Do
- Assign clear ownership.
- Maintain visible progress.
- Validate before merge.
- Escalate with options.

### Don't
- Hide blockers.
- Merge unverified claims.
- Run parallel tasks with coupled write paths.
- Let plans drift from actual execution.
