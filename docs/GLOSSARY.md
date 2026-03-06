# Глоссарий

**AI runtime template** — репозиторий-шаблон с инструкциями, агентскими ролями, playbook-документацией, bootstrap-скриптами и валидацией для Codex и Qwen.

**Entrypoint instructions** — локальные файлы [`AGENTS.md`](../AGENTS.md) и [`QWEN.md`](../QWEN.md), которые задают проектные правила для соответствующего runtime.

**Runtime state** — локальная директория `.ai-state/` с разделением по runtime:
- `.ai-state/codex/orchestrator`
- `.ai-state/qwen/orchestrator`

**Shared schemas/templates** — общие контракты в `.ai-state/orchestrator/schemas` и `.ai-state/orchestrator/templates`, которые используются обоими runtime.

**Chief Coordinator** — главный агент верхнего уровня, который управляет планом, вызывает инструменты оркестрации и синтезирует финальный результат.

**Specialist agent** — подагент с ограниченным scope, который решает конкретную подзадачу и возвращает evidence-backed результат.

**Stateful resume** — продолжение работы по данным из `.ai-state/<runtime>/orchestrator/`, а не по свободному текстовому “продолжай”.

**Watchdog** — журнал и правила anti-stall, фиксирующие зависания, отсутствие tool-call после approval и другие orchestration faults.

**Workspace** — локальная рабочая зона `workspace/` для AI-созданных проектов, не являющихся частью самого шаблона.
