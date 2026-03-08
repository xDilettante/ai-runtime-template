# SUMMARY

`ai-runtime-template` — шаблон AI-инфраструктуры для Codex и Qwen. Репозиторий хранит инструкции, policy/playbook, contracts и bootstrap-скрипты; прикладной runtime-код размещается в `workspace/`.

## Быстрый старт

```bash
cd /run/media/user/xSSD-500Gb/xProg/AI/go/ai-runtime-template
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
python3 scripts/init_ai_state_runtime.py
python3 scripts/validate_ai_state_schema.py
```

## Статусные артефакты

- `STATUS.md` — текущее состояние и readiness source of truth.
- `DEVLOG.md` — журнал значимых изменений, проверок и долгов.
- `SUMMARY.md` — краткий операторский обзор и стартовые команды.

## Ключевые документы

- `AGENTS.md` / `QWEN.md` — локальные entrypoint-инструкции для агентов.
- `CODEX.md` — адаптер Codex runtime и bridge policy.
- `docs/AI_UNIFIED_POLICY.md` — каноническая единая политика.
- `docs/AI_UNIFIED_CHECKLIST.md` — короткий checklist выполнения.
- `docs/AI_OPERATOR_CHEATSHEET.md` — операторские prompt-шаблоны.

## Ключевые пути

- `contracts/orchestrator/schemas/` — versioned JSON schemas runtime-state.
- `contracts/orchestrator/templates/` — versioned templates/checkpoint prompts.
- `scripts/` — bootstrap, lock-helpers и проверки согласованности.
- `workspace/` — место для AI-generated project code, не корень репозитория.
