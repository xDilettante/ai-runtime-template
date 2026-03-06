# Watchdog Protocol

Purpose:
- detect stalled orchestration steps
- detect missing tool progress after approval
- produce explicit recovery actions

Default stall conditions:
- `next_action_required=true` without the required tool call in the next turn
- active step remains `running` without state/checkpoint updates beyond the watchdog window
- approval was granted but execution did not resume with a real tool action

Default recovery sequence:
1. record watchdog event in `.ai-state/<runtime>/orchestrator/watchdog.log`
2. mark the step as `timeout` or `orchestration_fault`
3. rerun once with narrowed scope or explicit `RESUME_CONTEXT`
4. escalate if the same failure pattern repeats

Operator note:
- watchdog output is evidence, not silent auto-magic
- repeated watchdog incidents should trigger scope reduction or manual intervention
