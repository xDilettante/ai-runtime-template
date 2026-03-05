# CODEX.md

Codex runtime adapter for this repository.

## 1) Purpose
- Keep this file Codex-specific and concise.
- Keep shared rules in `AGENTS.md` and `docs/AI_UNIFIED_POLICY.md`.

## 2) Canonical Links
- [AGENTS.md](./AGENTS.md)
- [AI_UNIFIED_POLICY.md](./docs/AI_UNIFIED_POLICY.md)
- [AI_UNIFIED_CHECKLIST.md](./docs/AI_UNIFIED_CHECKLIST.md)
- [CODEX_CHECKLIST.md](./CODEX_CHECKLIST.md)
- [CODEX_OPERATOR_CHEATSHEET.md](./CODEX_OPERATOR_CHEATSHEET.md)
- [QWEN_OPERATOR_CHEATSHEET.md](./QWEN_OPERATOR_CHEATSHEET.md)
- [AI_OPERATOR_CHEATSHEET.md](./docs/AI_OPERATOR_CHEATSHEET.md)

## 3) Tool Mapping
- `spawn_agent` -> create a specialist agent.
- `send_input` -> tasking/follow-up for an existing agent.
- `wait` -> await status.
- `close_agent` -> close finalized agent.
- Practical runtime cap: up to 6 active subagents in this environment.

## 4) Practical Runtime Rules
- Prefer sequential orchestration unless parallelism clearly improves latency without adding coordination risk.
- Keep subagent tasks narrow and independently verifiable.
- Merge subagent outcomes only after evidence review.
- Close completed/errored subagents immediately to avoid thread-limit stalls.
- Main Codex is the only orchestrator for execution control.
- `multi-agent-coordinator`, `workflow-orchestrator`, `it-ops-orchestrator`, `agent-organizer`, and `task-distributor` are advisory-only here (routing/selection output, no nested orchestration calls).
- Codex may invoke external Qwen worker as one-way bridge (`Codex -> Qwen`) for delegated analysis/implementation batches.
- Qwen-to-Codex reverse bridge is forbidden; cross-runtime recursion is forbidden.
- Run at most one external Qwen worker per top-level turn.

## 5) Approval and Resume
- For approval-gated flow, continue with an actual tool call.
- Do not finish an approval gate with text-only confirmation.

## 6) Qwen Invocation Modes (Codex -> Qwen)
- Codex may run external Qwen only as a one-way delegated worker.
- Keep one Qwen run per top-level turn.

Allowed modes:
1. `advisory-routing`
- Purpose: ask Qwen to propose agent set, scoring, and execution queue.
- Use for: team composition, routing alternatives, fallback plans.
- Output expected: structured routing JSON only.

2. `focused-analysis`
- Purpose: deep read-only analysis of bounded scope.
- Use for: architecture audit, docs/policy audit, risk inventory, cross-check of findings.
- Output expected: severity-first findings with file evidence.

3. `implementation-batch`
- Purpose: implement clearly bounded change set when Codex needs parallel external execution lane.
- Use for: isolated feature/fix with explicit acceptance and tests.
- Output expected: diff summary + executed checks + residual risks.

4. `verification-batch`
- Purpose: independent verification/review of already prepared changes.
- Use for: regression checks, policy compliance, test-gap analysis.
- Output expected: pass/fail verdict with reproducible evidence.

Disallowed delegation:
- global orchestration control,
- recursive cross-runtime chains,
- unbounded “analyze everything and decide everything” ownership.

Required handoff packet to Qwen:
- `mode`, `objective`, `scope`, `constraints`, `acceptance`, `required evidence`, `stop conditions`.

Trust model:
- Treat Qwen output as evidence candidate, not final truth.
- Codex must validate critical claims locally before final user synthesis.

## 7) Qwen Completion Policy (Mandatory)
- If Codex starts a Qwen run for a delegated task, Codex must wait for terminal completion of that run.
- Do not interrupt/terminate Qwen early just because partial output is already available.
- Do not send stop signals (`Ctrl-C`/forced terminate) unless one of these conditions is true:
  - explicit user request to stop,
  - safety/compliance risk detected,
  - hard technical fault (hung process with no progress beyond configured timeout window).

Waiting behavior:
1. Keep polling/streaming Qwen progress until final result is produced.
2. During long runs, provide periodic user updates with concrete progress.
3. If timeout/fault is suspected, report evidence first and ask whether to continue waiting or stop.

Result handling:
- Capture both interim progress and final Qwen synthesis.
- Compare and report only after Qwen final status is known (or explicit user stop).
