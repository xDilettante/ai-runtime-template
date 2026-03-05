# AI Operator Cheatsheet

Unified operator cheatsheet for both Codex and Qwen.

## 1) Base Request Template
```text
Режим: Chief Coordinator.
Цель: <что должно быть в итоге>.
Шаг: <S# или "восстанови из .ai-state/<runtime>/orchestrator/state.json">.
Scope: <файлы/модули>.
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

## 2) Common Scenarios

### 2.1 Start New Fix Step
```text
Режим: Chief Coordinator.
Цель: исправить <проблема>.
Шаг: S3.
Scope: pkg/xlog/...
Acceptance:
1) тесты проходят
2) регрессий нет
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
Действие: доведи шаг до done или blocked.
```

### 2.2 Resume After Approval
```text
Продолжай по stateful-resume.
Шаг: S2 (awaiting_approval).
Approved: "Да, вноси правки! Используй вариант 1".
Сделай новый tool-call с RESUME_CONTEXT (не text-only).
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
```

### 2.3 Review Step
```text
Режим: Chief Coordinator.
Шаг: S4 review.
Цель: независимая проверка изменений S4.
Acceptance:
1) критичных замечаний нет
2) проверки воспроизводимы
Ограничения:
- read-only git
- step_result обязателен
- agent_trace обязателен
```

### 2.4 Verification Step
```text
Режим: Chief Coordinator.
Шаг: S5 verify.
Цель: подтвердить acceptance критерии проверками.
Команды:
1) <targeted command 1>
2) <targeted command 2>
Ограничения:
- step_result обязателен
- agent_trace обязателен
- allow_git_write=false
```

### 2.5 Enable Git Write for One Step
```text
Разрешаю git-write только для этого шага.
Шаг: S7.
allow_git_write=true
git_writer=chief_coordinator
Сделай commit после успешных проверок и верни step_result + trace.
```

## 3) Fast Shortcuts

### 3.1 Continue from State
```text
Восстанови план из `.ai-state/<runtime>/orchestrator/state.json` и продолжай следующий незавершенный шаг.
Обязательно: step_result + agent_trace.
```

### 3.2 Force Resume
```text
RESUME S2 APPROVED.
Сделай новый tool-call по RESUME_CONTEXT и продолжай без text-only ответа.
```

### 3.3 Anti-Stall Check
```text
Проверь watchdog условия:
- нет ли шага с next_action_required=true без tool_call
- нет ли timeout > 8 минут
Если есть — выполни auto-recovery и зафиксируй в `.ai-state/<runtime>/orchestrator/watchdog.log`.
```

## 4) Runtime Mapping
- Qwen typical task tool-call: `task` + `RESUME_CONTEXT` on resume.
- Codex typical orchestration calls: `spawn_agent`, `send_input`, `wait`, `close_agent`.
- Orchestration control is main-agent only (top-level Codex/Qwen handling the user turn).
- Coordinator/orchestrator subagents are routing-only advisors (no nested orchestration control).
- One-way cross-runtime bridge: `Codex -> Qwen` allowed (external worker mode, one worker at a time).
- Reverse bridge is forbidden: `Qwen -> Codex`.
- Recursive cross-runtime chains are forbidden.
- Locked write wrapper (recommended): `./scripts/ai_state_with_lock.sh <codex|qwen> <command...>`.

## 5) Avoid These Inputs
- "просто продолжай" без `Шаг` и `Acceptance`.
- "сделай как лучше" без scope/ограничений.
- approval-сообщение без требования нового tool-call.

## 6) Minimum Required Fields
1. `Цель`
2. `Шаг`
3. `Acceptance`
4. `allow_git_write` (обычно `false`)
