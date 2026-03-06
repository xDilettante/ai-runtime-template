# Agent Orchestration Playbook (Sequential Mode)

This playbook defines how Qwen must orchestrate agents when parallel execution is unavailable.

## 1) Execution model
- Execution mode is **strictly sequential**: one active agent at a time.
- Never assume concurrent progress from multiple agent invocations.
- Every step must produce explicit artifacts for the next step.

## 1.1) Orchestration authority boundary (mandatory)
- Only the main Qwen agent may execute orchestration control calls.
- Coordinator/orchestrator agents (for example `multi-agent-coordinator`, `workflow-orchestrator`, `it-ops-orchestrator`, `agent-organizer`, `task-distributor`) are advisory-only when run as subagents.
- Advisory-only means: candidate discovery, scoring, routing JSON, handoff packet drafting.
- Advisory-only roles must not perform nested orchestration control.

## 1.2) Cross-runtime bridge boundary (mandatory)
- Qwen must not invoke Codex runtime (reverse bridge forbidden).
- Cross-runtime recursion is forbidden (`Codex -> Qwen -> Codex`).
- If cross-runtime delegation is required, return routing/handoff for main Codex to execute.

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
  "evidence": ["..."],
  "changes": ["..."],
  "assumptions": ["..."],
  "risks": ["..."],
  "checks": [
    {"name": "python3 scripts/validate_ai_state_schema.py", "status": "passed", "details": "runtime contracts validated"}
  ],
  "next_decision": "continue|rerun|escalate|stop",
  "next_action_required": false,
  "next_action": "",
  "notes": ""
}
```

## 8) Stateful resume protocol (mandatory)
When an agent asks for confirmation (for example: "Apply fix?", "Вношу правки?"),
the coordinator must NOT stop on plain text approval.

Required runtime artifacts:
- `.ai-state/qwen/orchestrator/state.json` — global queue and per-step status.
- `.ai-state/qwen/orchestrator/agents/<agent>.md` — rolling memory per agent.
- `.ai-state/qwen/orchestrator/checkpoints/<step_id>.json` — latest step checkpoint.

Allowed step status lifecycle:
- `planned -> running -> awaiting_approval -> resumed -> done`
- `planned -> running -> blocked`

Mandatory behavior:
1. If step result contains an approval question:
   - write checkpoint for the step,
   - set status to `awaiting_approval`,
   - wait for user decision.
2. If user approved:
   - set status to `resumed`,
   - immediately issue a NEW task call to the SAME agent,
   - include explicit `RESUME_CONTEXT` block (see template below),
   - do not treat plain assistant text as execution.
3. If user rejected/changed approach:
   - update checkpoint with new decision,
   - rerun current step with updated scope or escalate.

Auto-heal guardrail:
- After any approval message (`approve`, `да`, `вноси`, `go ahead`) the next assistant turn
  must contain a task tool call.
- If no tool call happened, treat as orchestration fault and immediately re-issue the task.

### 8.1 Checkpoint template
```json
{
  "step_id": "S1",
  "agent": "golang-pro",
  "status": "awaiting_approval",
  "goal": "Fix the current step scope",
  "files_touched": ["path/to/file.ext", "path/to/test.ext"],
  "decisions": ["Preferred variant: A"],
  "open_questions": ["Apply changes now?"],
  "approved": false,
  "next_action": "On approval, rerun same agent with RESUME_CONTEXT",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### 8.2 Resume task template
```text
You are continuing the same step. Do not restart from scratch.

RESUME_CONTEXT:
- step_id: S1
- previous_status: awaiting_approval
- prior_summary: <brief accepted summary from previous run>
- approved_decision: <approved option, exact wording>
- files_in_scope:
  - path/to/file.ext
  - path/to/test.ext
- required_actions:
  1) apply approved implementation
  2) show diffs
  3) run required tests/benchmarks
- acceptance_criteria:
  - behavior intent preserved
  - contract unchanged unless approved
  - tests pass

Work on implementation now, not analysis.
```

## 9) Structured outputs + watchdog (mandatory)
To avoid parser drift and stalled chains:

1. Every implementer/verifier response must follow
   `.ai-state/orchestrator/schemas/step_result.schema.json`.
2. Coordinator validates response format before deciding next step.
3. Set `next_action_required=true` whenever the next turn must execute a tool call.
4. If `next_action_required=true` and no tool call was made in next turn:
   - mark step `orchestration_fault`,
   - re-issue the same task with `RESUME_CONTEXT`,
   - append incident to `.ai-state/qwen/orchestrator/watchdog.log`.
5. Watchdog timeout:
   - if no state/checkpoint update for 8 minutes while step is `running`,
     set status `timeout` and decide `rerun|escalate`.

Reference:
- `.ai-state/orchestrator/WATCHDOG_PROTOCOL.md`
- `.ai-state/orchestrator/templates/task_prompt_fix.md`
- `.ai-state/orchestrator/templates/task_prompt_review.md`
- `.ai-state/orchestrator/templates/task_prompt_verify.md`

## 10) Agent trace logging (mandatory)
Every agent must write execution trace events during work, not only final result.

Trace file:
- `.ai-state/qwen/orchestrator/agent_trace.log` (append-only JSONL)

Schema:
- `.ai-state/orchestrator/schemas/agent_trace.schema.json`

Required events (minimum):
1. `received_task`
2. `parsed_context`
3. `reading_files`
4. `running_command`
5. `editing_file`
6. `validation_started`
7. `validation_finished`
8. `blocked` or `completed`

Required fields per event:
- `ts`, `run_id`, `step_id`, `agent`, `event`, `source_actor`, `request_id`, `summary`, `status`

Validation rules:
- Coordinator does not accept step completion without at least:
  - one `received_task` event
  - one terminal event (`completed` or `blocked`)
- Secrets/tokens must never be written to trace log.

## 11) Git write control (mandatory)
Step contract must include:
- `allow_git_write`: `true|false` (default `false`)
- `git_writer`: `chief_coordinator|git-workflow-manager|none`

Rules:
1. If `allow_git_write=false`, subagents must not run git-write commands.
2. If git-write is required, route operation to:
   - Qwen (Chief Coordinator), or
   - `git-workflow-manager` agent.
3. If a non-authorized agent attempts git-write:
   - mark step status `orchestration_fault`,
   - log event `policy_violation` to `.ai-state/qwen/orchestrator/watchdog.log`,
   - rerun step without git-write, or escalate to authorized git writer.
