# Agent Orchestration Playbook (Sequential Mode)

This playbook defines how Codex must orchestrate agents when parallel execution is unavailable.

## 1) Execution model
- Execution mode is **strictly sequential**: one active agent at a time.
- Never assume concurrent progress from multiple agent invocations.
- Every step must produce explicit artifacts for the next step.

## 1.1) Orchestration authority boundary (mandatory)
- Only the main Codex agent may execute orchestration control calls (`spawn_agent`, `send_input`, `wait`, `close_agent`).
- Coordinator/orchestrator roles (for example `multi-agent-coordinator`, `workflow-orchestrator`, `it-ops-orchestrator`, `agent-organizer`, `task-distributor`) are advisory-only when run as subagents.
- Advisory-only means: candidate discovery, scoring, routing JSON, handoff packet drafting.
- Advisory-only roles must not perform nested orchestration control.

## 1.2) Cross-runtime bridge boundary (mandatory)
- One-way bridge allowed: main Codex may invoke external Qwen worker for delegated sub-task execution.
- Reverse bridge is forbidden: Qwen must not invoke Codex runtime.
- Recursive bridge chains are forbidden (`Codex -> Qwen -> Codex`).
- Run at most one external Qwen worker per top-level orchestration turn.

## 2) Standard phases

### Phase A: Plan
- Clarify goal, scope, constraints, and success criteria.
- Select primary and backup agents using routing contract.
- Build ordered execution queue.

### Phase B: Execute sequentially
For each step in queue:
1. Send task to exactly one agent.
2. Wait for completion result.
3. Validate output against acceptance criteria.
4. Decide next action:
   - continue to next planned step,
   - re-run with narrower scope,
   - escalate to backup agent,
   - return blocked state.

### Phase C: Synthesize
- Merge validated outputs.
- Mark assumptions and unresolved risks.
- Produce final evidence-backed result.

## 3) Handoff packet (required between steps)
Use this structure for every transfer:

```json
{
  "from_agent": "...",
  "to_agent": "...",
  "step_id": "S1|S2|...",
  "goal": "...",
  "inputs": ["paths, logs, artifacts"],
  "constraints": ["scope/time/safety constraints"],
  "expected_output": "format + acceptance criteria",
  "fallback": "what to do on failure"
}
```

## 4) Escalation policy
Escalate to another agent only if at least one condition is true:
- capability mismatch discovered,
- output failed acceptance criteria,
- blocker cannot be resolved inside current scope,
- risk level increased (security/reliability/compliance).

Every escalation must include:
- reason,
- evidence,
- changed scope,
- new acceptance criteria.

## 5) Replanning triggers
Rebuild queue when:
- requirements changed,
- key assumption was invalidated,
- output quality is insufficient,
- runtime constraints changed.

## 6) Prohibited patterns
- Fire-and-forget multi-agent calls.
- Claims of parallel execution.
- Skipping validation between steps.
- KPI claims without run evidence.

## 7) Minimal sequential templates

### Sequential plan template
```json
{
  "queue": [
    {"step_id":"S1","agent":"...","goal":"..."},
    {"step_id":"S2","agent":"...","goal":"..."}
  ],
  "success_criteria": ["..."],
  "fallbacks": ["..."]
}
```

### Step result template (schema-aligned)
```json
{
  "step_id": "S1",
  "agent": "golang-pro",
  "status": "success|partial|blocked|awaiting_approval|timeout|orchestration_fault",
  "summary": "...",
  "files": ["path/to/file1", "path/to/file2"],
  "evidence": ["..."],
  "changes": ["..."],
  "assumptions": ["..."],
  "risks": ["..."],
  "checks": [
    {"name": "python3 scripts/validate_ai_state_schema.py", "status": "passed", "details": "runtime schemas validated"}
  ],
  "next_decision": "continue|rerun|escalate|stop",
  "next_action_required": false,
  "next_action": "",
  "notes": ""
}
```
