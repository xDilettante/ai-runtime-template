# AGENTS.override.md (Template)

Временные локальные переопределения для текущей сессии/контекста.
Этот файл должен быть короче и приоритетнее `AGENTS.md` только там, где явно указано.

## 1) Scope of override
- Applies to: `<describe current task scope>`
- Expires when: `<condition/date>`

## 2) Temporary priorities
- Primary goal: `<goal>`
- Hard constraints: `<time/safety/scope>`
- Success criteria: `<measurable conditions>`

## 3) Runtime mode override (optional)
- Execution mode: `sequential` (default) | `parallel` (only if explicitly allowed)
- If `parallel`, max threads allowed for this run: `<N>`

## 4) Role routing override (optional)
- Preferred roles: `<role1>, <role2>, ...`
- Blocked roles for this run: `<roleX>, ...`
- Escalation rule: `<when to escalate and to whom>`

## 5) Output requirements override (optional)
- Required artifacts: `<logs/tests/files>`
- Required report format: `<json/text>`

## 6) Notes
- Keep only task-specific overrides here.
- Remove this file (or clear sections) when override is no longer needed.
