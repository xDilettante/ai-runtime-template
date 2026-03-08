# ai-runtime-template

Шаблон AI-инфраструктуры для Codex и Qwen.

Репозиторий содержит только инфраструктуру оркестрации: инструкции, роли/агенты, policy/playbook, валидацию и bootstrap для новых машин. Runtime-код приложения сюда не входит.

AI-created project code should be placed in `workspace/`, not in the repository root. Contents of `workspace/` are local working material and are git-ignored by default, except for the workspace instructions.

## 1) Возможности

- Единый baseline инструкций для Codex и Qwen.
- Каталоги специализированных агентов (roles/agents).
- Правила оркестрации S1..Sn (sequential-first).
- Stateful resume через `.ai-state`.
- Watchdog/anti-stall протокол.
- Скрипты проверки лимитов и синхронизации инструкций.
- Переносимые глобальные инструкции для новых ПК.

## 2) Как это работает

Слои инструкций (по приоритету):
1. runtime system/developer/user instructions
2. project-local entrypoint (`AGENTS.md` / `QWEN.md`)
3. global entrypoint (`~/.codex/AGENTS.md` / `~/.qwen/QWEN.md`)

Оркестрация:
- главный Codex/Qwen = единственный исполнитель control-вызовов,
- coordinator-агенты = advisory-only (подбор/маршрутизация, без nested orchestration),
- default режим = sequential,
- parallel только для независимых merge-safe задач.

Cross-runtime:
- разрешен только `Codex -> Qwen` (не более 1 внешнего Qwen worker на top-level turn),
- `Qwen -> Codex` запрещен,
- рекурсивные цепочки запрещены.

## 3) Структура

```text
ai-runtime-template/
  .codex/
  .qwen/
  bootstrap/
    global-instructions/
  docs/
  scripts/
  workspace/
  AGENTS.md
  QWEN.md
  CODEX.md
```

## 4) Быстрый старт (новая машина)

```bash
cd ai-runtime-template

# 1) Посмотреть, что bootstrap изменит в HOME
bash scripts/bootstrap_global_instructions.sh --dry-run

# 2) Применить global instruction snapshots осознанно
bash scripts/bootstrap_global_instructions.sh --yes

# 3) Валидация лимитов инструкций
python3 scripts/check_instruction_limits.py

# 4) Проверка синхронизации AGENTS/CODEX/QWEN с unified policy
python3 scripts/verify_ai_policy_sync.py

# 5) Инициализация runtime-state (shared schemas/templates уже versioned в repo)
python3 scripts/init_ai_state_runtime.py

# 6) Проверка схемы runtime-state
python3 scripts/validate_ai_state_schema.py
```

Versioned contracts for runtime-state are stored separately from generated `.ai-state` under:
- `contracts/orchestrator/schemas/`
- `contracts/orchestrator/templates/`

## 5) Запуск агентов (кратко)

Ниже команды для оператора в виде готовых запросов (вставляются в диалог с Codex/Qwen).

### 5.1 Один агент (кратко)

```text
Режим: Chief Coordinator.
Шаг: S1.
Цель: <задача>.
Scope: <файлы/модули>.
Назначь одного профильного агента и доведи шаг до done/blocked.
Ограничения: sequential only, step_result обязателен, agent_trace обязателен, allow_git_write=false.
```

### 5.2 Команда агентов (кратко)

```text
Режим: Chief Coordinator.
Собери план S1..Sn и команду из 3-6 агентов.
Запускай по шагам до результата, не более 2 активных одновременно.
Ограничения: sequential по умолчанию, coordinator-агенты advisory-only, step_result + agent_trace обязательны.
```

## 6) Запуск агентов (полный шаблон)

### 6.1 Полный шаблон для 1 шага

```text
Режим: Chief Coordinator.
Цель: <что должно быть в итоге>.
Шаг: S#.
Scope: <пути/модули>.
Acceptance:
1) <критерий 1>
2) <критерий 2>
Ограничения:
- sequential only
- step_result в стандартном формате
- agent_trace обязателен
- allow_git_write=false
Действие: начни выполнение сейчас и обновляй state/checkpoint/trace.
```

### 6.2 Полный шаблон для multi-step команды

```text
Режим: Chief Coordinator.
Цель: <цель проекта/итерации>.
Собери план S1..Sn.
Для каждого шага укажи: агент, scope, acceptance, fallback.
Запускай шаги последовательно, после каждого шага: validate -> decision (continue|rerun|escalate|stop).
Ограничения:
- coordinator/orchestrator subagents = advisory-only
- nested orchestration запрещена
- step_result + agent_trace обязательны
- allow_git_write=false (если не разрешено отдельно)
```

## 7) Codex/Qwen runtime команды (инструментальный уровень)

### Codex
Типичные orchestration-вызовы:
- `spawn_agent`
- `send_input`
- `wait`
- `close_agent`

Практический лимит среды: до 6 активных subagents.

### Qwen
Типичный режим:
- task tool-call,
- при approval-resume обязателен новый task call с `RESUME_CONTEXT` (не text-only).

## 8) Stateful resume и anti-stall

Если шаг остановлен на approval:
1. статус шага -> `awaiting_approval`,
2. после `approve/да/вноси` немедленно новый tool-call,
3. статус -> `resumed`, затем выполнение.

Watchdog проверки:
- нет ли `next_action_required=true` без tool-call,
- нет ли timeout шага > 8 минут.

Артефакты:
- `.ai-state/<runtime>/orchestrator/state.json`
- `.ai-state/<runtime>/orchestrator/checkpoints/*.json`
- `.ai-state/<runtime>/orchestrator/agent_trace.log`
- `.ai-state/<runtime>/orchestrator/watchdog.log`

## 9) Разрешение git-write

По умолчанию: `allow_git_write=false`.

Если нужен git-write на шаг:
```text
allow_git_write=true
git_writer=chief_coordinator
```

Нельзя делать git-write неавторизованными subagents.

## 10) Глобальные инструкции для переноса

Снапшоты лежат в:
- `bootstrap/global-instructions/GLOBAL_CODEX_AGENTS.md`
- `bootstrap/global-instructions/GLOBAL_QWEN_QWEN.md`

Автоустановка:

```bash
bash scripts/bootstrap_global_instructions.sh --dry-run
bash scripts/bootstrap_global_instructions.sh --yes
```

Скрипт ставит их в:
- `~/.codex/AGENTS.md`
- `~/.qwen/QWEN.md`

Поддерживаются:
- `--dry-run` для preview без записи
- `--dest-home <path>` для безопасного тестового прогона
- `--restore [--stamp <timestamp>]` для отката из backup

Codex safety profiles:
- default profile lives in `.codex/config.toml` and uses `approval_policy = "on-request"` with `multi_agent = false`
- optional fast local profile example lives in `.codex/config.fast.toml.example`

## 11) Ежедневный operator workflow

Перед началом:

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
python3 scripts/init_ai_state_runtime.py
```

После изменения инструкций/политик:

```bash
python3 scripts/check_instruction_limits.py
python3 scripts/verify_ai_policy_sync.py
python3 scripts/validate_ai_state_schema.py
```

## 12) Основные документы

- `AGENTS.md` / `QWEN.md` — проектные entrypoint-файлы.
- `CODEX.md` — Codex runtime adapter и bridge policy.
- `docs/AI_UNIFIED_POLICY.md` — единая политика.
- `docs/AI_OPERATOR_CHEATSHEET.md` — операторские шаблоны.
- `.codex/CODEX_ORCHESTRATION.md` и `.qwen/AGENT_ORCHESTRATION.md` — playbook оркестрации.

## 13) Статус и лицензия

- `STATUS.md` — текущее состояние и readiness source of truth.
- `DEVLOG.md` — журнал значимых изменений, проверок и долгов.
- `SUMMARY.md` — краткая операторская сводка и быстрый вход в репозиторий.
- `LICENSE` — MIT.
