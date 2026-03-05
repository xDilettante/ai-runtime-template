# Global Instructions Snapshot

Эти файлы — переносимый снапшот глобальных инструкций для новых компьютеров.

- `GLOBAL_CODEX_AGENTS.md` -> `~/.codex/AGENTS.md`
- `GLOBAL_QWEN_QWEN.md` -> `~/.qwen/QWEN.md`

Применение вручную:

```bash
mkdir -p ~/.codex ~/.qwen
cp bootstrap/global-instructions/GLOBAL_CODEX_AGENTS.md ~/.codex/AGENTS.md
cp bootstrap/global-instructions/GLOBAL_QWEN_QWEN.md ~/.qwen/QWEN.md
```

Или используйте автоматический скрипт:

```bash
bash scripts/bootstrap_global_instructions.sh
```
