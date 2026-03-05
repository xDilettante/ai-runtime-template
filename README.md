# ai-runtime-template

Шаблон репозитория для AI-инфраструктуры (Codex + Qwen) без runtime-кода приложения.

## 1. Назначение

`ai-runtime-template` нужен как переносимая база для новых проектов и новых компьютеров:
- единые инструкции для Codex и Qwen,
- каталоги ролей/агентов,
- orchestration/policy документы,
- скрипты валидации и bootstrap.

Репозиторий специально **не** содержит `cmd/pkg` и служебные runtime-артефакты продукта.

## 2. Что внутри

- `.codex/` — инфраструктура Codex (roles, policy, orchestration, config, scripts).
- `.qwen/` — инфраструктура Qwen (agents, policy, orchestration).
- `AGENTS.md` — проектный entrypoint для Codex.
- `QWEN.md` — проектный entrypoint для Qwen.
- `CODEX.md` — доп. проектные правила Codex.
- `docs/` — практики, чеклисты, playbooks, аудитные документы.
- `scripts/` — утилиты проверки/инициализации.
- `bootstrap/global-instructions/` — снапшоты глобальных инструкций для нового ПК.

## 3. Что исключено намеренно

- runtime-код приложения (`cmd/`, `pkg/`, `configs/`),
- `.ai-state/` (генерируется локально),
- бинарники, логи, coverage/report артефакты,
- `.git` исходного проекта.

## 4. Требования

- Linux/macOS shell (bash)
- Python 3.10+
- (опционально) Codex/Qwen CLI, если запускаете локально

## 5. Быстрый старт

```bash
cd ai-runtime-template

# 1) Установить глобальные инструкции в домашнюю директорию
bash scripts/bootstrap_global_instructions.sh

# 2) Проверить лимиты инструкций
python3 scripts/check_instruction_limits.py

# 3) Проверить синхронизацию проектных инструкций
python3 scripts/verify_ai_policy_sync.py

# 4) Инициализировать runtime-state (локально, не в git)
python3 scripts/init_ai_state_runtime.py

# 5) Проверить схему runtime-state
python3 scripts/validate_ai_state_schema.py
```

## 6. Глобальные инструкции для новых компьютеров

Снапшоты лежат в:
- `bootstrap/global-instructions/GLOBAL_CODEX_AGENTS.md`
- `bootstrap/global-instructions/GLOBAL_QWEN_QWEN.md`

Автоустановка:

```bash
bash scripts/bootstrap_global_instructions.sh
```

Скрипт:
- копирует файлы в `~/.codex/AGENTS.md` и `~/.qwen/QWEN.md`,
- создает backup текущих файлов (`.bak.<timestamp>`), если они уже есть.

## 7. Модель приоритетов инструкций

Приоритет выполнения:
1. system/developer/user runtime instructions
2. project-local entrypoint (`AGENTS.md` / `QWEN.md`)
3. global entrypoint (`~/.codex/AGENTS.md` / `~/.qwen/QWEN.md`)

Практика:
- глобальные файлы держим стабильными (fallback baseline),
- проектные файлы — конкретика проекта и текущие нюансы.

## 8. Типовой рабочий цикл

Перед сессией:

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
```

После правок инструкций:

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
python3 scripts/validate_ai_state_schema.py
```

Если работаете и в Codex, и в Qwen одновременно:
- используйте split runtime-state,
- сериализуйте записи через `scripts/ai_state_with_lock.sh`.

## 9. Структура каталогов (кратко)

```text
ai-runtime-template/
  .codex/
  .qwen/
  bootstrap/
    global-instructions/
  docs/
  scripts/
  AGENTS.md
  QWEN.md
  CODEX.md
```

## 10. Рекомендации по переносу в новый проект

1. Скопировать `ai-runtime-template` как основу.
2. Подставить проектные нюансы в `AGENTS.md` и `QWEN.md`.
3. Не менять глобальные файлы под конкретный проект.
4. Проверить лимиты/синхронизацию скриптами.
5. Зафиксировать baseline в первом коммите нового репозитория.

## 11. Файлы состояния

- `STATUS.md` — оперативный статус шаблона.
- `LICENSE` — лицензия шаблона (MIT).

