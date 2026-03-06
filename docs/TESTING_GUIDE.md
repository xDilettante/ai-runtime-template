# Руководство по проверкам для `ai-runtime-template`

Этот репозиторий не содержит application runtime code и Go-пакетов. Поэтому базовые проверки здесь относятся к инструкциям, policy-документам и AI-state tooling.

## Базовые команды

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
python3 scripts/init_ai_state_runtime.py
python3 scripts/validate_ai_state_schema.py
python3 .codex/scripts/codex_check.py
```

## Когда что запускать

### Перед изменением инструкций

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
```

### После изменения runtime-state tooling или схем

```bash
python3 scripts/init_ai_state_runtime.py
python3 scripts/validate_ai_state_schema.py
```

### После изменения каталога ролей Codex

```bash
python3 .codex/scripts/codex_check.py
```

## Что считается достаточной проверкой

- Изменения в `README.md`, `AGENTS.md`, `QWEN.md`, `docs/*`:
  - `check_instruction_limits.py`
  - `verify_ai_policy_sync.py`

- Изменения в `scripts/init_ai_state_runtime.py` или `scripts/validate_ai_state_schema.py`:
  - `init_ai_state_runtime.py`
  - `validate_ai_state_schema.py`

- Изменения в `.codex/config.toml` или `.codex/roles/*`:
  - `.codex/scripts/codex_check.py`

## Примечание

- Старые команды из legacy Go/Makefile workflow не относятся к текущему шаблону и не должны использоваться как основной verification path в этом репозитории.
