# QWEN Daily Agent Checklist

Базовый чеклист:
- [AI_UNIFIED_CHECKLIST.md](./docs/AI_UNIFIED_CHECKLIST.md)

Qwen-specific дополнения:
- [ ] Qwen выступает как Chief Coordinator.
- [ ] Для approval шага выставлен `awaiting_approval`.
- [ ] После approval выполнен новый tool-call с `RESUME_CONTEXT`.
- [ ] Watchdog/trace артефакты обновляются в `.ai-state/qwen/orchestrator/`.
