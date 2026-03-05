# Руководство по тестированию в myVpnServices

Этот документ описывает правила написания стабильных тестов, использования параллельности и процедуры проверки качества кода.

## Содержание

1. [Как запускать тесты](#как-запускать-тесты)
2. [Как писать стабильные тесты](#как-писать-стабильные-тесты)
3. [Использование t.Parallel()](#использование-tparallel)
4. [Тесты с глобальным состоянием](#тесты-с-глобальным-состоянием)
5. [Checklist для code review](#checklist-для-code-review)
6. [Отладка падающих тестов](#отладка-падающих-тестов)

---

## Как запускать тесты

### Базовые команды

```bash
# Простой запуск тестов
make test

# С race detector (обнаружение гонок данных)
make test-race

# С отчётом о покрытии
make test-coverage
```

### Стресс-тесты

**Стресс-тесты** — это многократный прогон тестов для выявления нестабильностей и race conditions.

```bash
# Быстрые стресс-тесты (5 прогонов) — рекомендуется перед каждым коммитом
make test-quick-stress

# Полные стресс-тесты (20 прогонов) — рекомендуется перед релизом
make test-stress

# Проверка стабильности (10 прогонов с проверкой каждого)
make test-stability
```

### Проверки перед коммитом

```bash
# Быстрая проверка (lint + тесты)
make check

# Полная проверка (lint + стресс-тесты)
make check-all

# Перед релизом (полные стресс-тесты + покрытие)
make check-release

# Проверка синхронизации AI-инструкций (AGENTS/CODEX/QWEN)
make ai-policy-verify
```

### Ручной запуск с флагами

```bash
# Запуск конкретного теста
go test -v -run TestName ./pkg/xlog/...

# Запуск с race detector и таймаутом
go test -race -timeout=5m ./pkg/xlog/...

# Многократный прогон (для выявления гонок)
go test -race -count=10 ./pkg/xlog/...

# Запуск с покрытием
mkdir -p reports/coverage
go test -coverprofile=reports/coverage/coverage.out ./pkg/xlog/...
go tool cover -html=reports/coverage/coverage.out -o reports/coverage/coverage.html
```

---

## Как писать стабильные тесты

### ✅ Лучшие практики

**1. Изоляция тестов**

Каждый тест должен быть независимым:

```go
func TestSomething(t *testing.T) {
    // ✅ Создаём изолированный логгер для теста
    logger, cleanup, err := New(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup() // Очищаем ресурсы
    
    // Тест использует только свой logger
    logger.Info("тест")
}
```

**2. Использование t.TempDir()**

Для временных файлов:

```go
func TestWithFile(t *testing.T) {
    // ✅ Автоматически создаёт и удаляет временную директорию
    tmpDir := t.TempDir()
    logFile := filepath.Join(tmpDir, "test.log")
    
    // Используем logFile в тесте
}
```

**3. Детерминированные тесты**

Избегайте зависимости от времени и случайных значений:

```go
// ❌ Плохо: тест зависит от текущего времени
func TestTime(t *testing.T) {
    now := time.Now()
    // Результат зависит от когда запущен тест
}

// ✅ Хорошо: используем фиксированное время
func TestTime(t *testing.T) {
    fixedTime := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
    // Результат всегда одинаковый
}
```

**4. Адекватные таймауты**

```go
// ✅ Тест должен завершаться за разумное время
func TestAsync(t *testing.T) {
    done := make(chan struct{})
    go func() {
        // какая-то работа
        close(done)
    }()
    
    select {
    case <-done:
        // Успех
    case <-time.After(5 * time.Second):
        t.Fatal("тест превысил таймаут")
    }
}
```

### ❌ Антипаттерны

**1. Сон в тестах**

```go
// ❌ Плохо: ненадёжно и медленно
time.Sleep(100 * time.Millisecond)

// ✅ Хорошо: используем каналы для синхронизации
select {
case <-done:
    // Готово
case <-time.After(timeout):
    t.Fatal("timeout")
}
```

**2. Глобальное состояние без изоляции**

```go
// ❌ Плохо: тесты влияют друг на друга
func TestGlobal(t *testing.T) {
    SetGlobal(logger) // Другие тесты тоже это делают!
    Info("тест")      // Гонка!
}

// ✅ Хорошо: изолируем глобальное состояние
func TestGlobal(t *testing.T) {
    // t.Parallel() НЕ используется
    logger, cleanup, err := NewWithGlobal(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    Info("тест") // Безопасно
}
```

**3. Зависимость от порядка выполнения**

```go
// ❌ Плохо: тест зависит от другого теста
func TestA(t *testing.T) {
    globalVar = 42
}

func TestB(t *testing.T) {
    if globalVar != 42 { // Может не быть 42!
        t.Error()
    }
}
```

---

## Использование t.Parallel()

### ✅ МОЖНО использовать `t.Parallel()`:

1. **Тесты не используют глобальное состояние**

```go
func TestIsolated(t *testing.T) {
    t.Parallel() // ✅ Безопасно
    
    logger, cleanup, err := New(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    logger.Info("тест") // Использует локальный logger
}
```

2. **Тесты используют t.TempDir()**

```go
func TestWithTempDir(t *testing.T) {
    t.Parallel() // ✅ Безопасно
    
    tmpDir := t.TempDir() // Изолированная директория
    logFile := filepath.Join(tmpDir, "test.log")
    
    // Пишем в logFile
}
```

3. **Подтесты в таблице тестов**

```go
func TestTableDriven(t *testing.T) {
    tests := []struct {
        name string
        input int
        want int
    }{
        {"case1", 1, 2},
        {"case2", 2, 3},
    }
    
    for _, tt := range tests {
        tt := tt // capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // ✅ Безопасно для подтестов
            
            got := tt.input + 1
            if got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}
```

### ❌ НЕЛЬЗЯ использовать `t.Parallel()`:

1. **Тесты работают с глобальным логгером**

```go
func TestGlobalLogger(t *testing.T) {
    // ❌ ОПАСНО: гонка с другими тестами!
    // t.Parallel()
    
    logger, cleanup, err := New(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    SetGlobal(logger) // Модифицируем глобальное состояние
    Info("тест")      // Используем глобальные функции
}
```

2. **Тесты используют глобальные функции логирования**

```go
func TestGlobalFunctions(t *testing.T) {
    // ❌ ОПАСНО: другие тесты тоже вызывают SetGlobal!
    // t.Parallel()
    
    SetGlobal(logger)
    
    Debug("тест")  // Глобальная функция
    Info("тест")   // Глобальная функция
    Warn("тест")   // Глобальная функция
    Error("тест")  // Глобальная функция
}
```

3. **Тесты модифицируют глобальные переменные**

```go
func TestModifyGlobal(t *testing.T) {
    // ❌ ОПАСНО: гонка за глобальную переменную!
    // t.Parallel()
    
    oldGlobal := globalLogger
    globalLogger = nil // Модификация!
    defer func() {
        globalLogger = oldGlobal
    }()
    
    // Тест работает с nil globalLogger
}
```

4. **Интеграционные тесты с внешними ресурсами**

```go
func TestIntegration(t *testing.T) {
    // ❌ ОПАСНО: конфликт за файлы/порты/БД
    // t.Parallel()
    
    // Тест использует общий файл/порт/БД
}
```

---

## Тесты с глобальным состоянием

### Что такое глобальное состояние?

Глобальное состояние — это данные, которые разделяются между тестами:

- Глобальные переменные (`globalLogger`, `globalConfig`)
- Глобальные функции (`SetGlobal()`, `GetGlobal()`, `Info()`, `Debug()`)
- Общие файлы без изоляции
- Общие сетевые порты
- Базы данных без изоляции

### Правила для тестов с глобальным состоянием

**1. Не использовать `t.Parallel()`**

```go
func TestWithGlobalState(t *testing.T) {
    // ✅ Правильно: убираем t.Parallel()
    // t.Parallel() // ← Закомментировать или удалить
    
    logger, cleanup, err := NewWithGlobal(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    // Тест выполняется последовательно с другими
}
```

**2. Очищать состояние после теста**

```go
func TestWithGlobalState(t *testing.T) {
    oldState := saveState() // Сохраняем состояние
    defer restoreState(oldState) // Восстанавливаем
    
    // Модифицируем глобальное состояние
    SetGlobal(logger)
    
    // Тест
}
```

**3. Документировать почему `t.Parallel()` нельзя**

```go
func TestWithGlobalState(t *testing.T) {
    // t.Parallel() // Убрано: тест работает с глобальным состоянием (SetGlobal)
    
    // ... код теста
}
```

### Примеры из проекта

**✅ Правильно:**

```go
// integration_test.go
func TestIntegration_NewWithGlobal(t *testing.T) {
    // t.Parallel() // Убрано: тест работает с глобальным состоянием (глобальный логгер)
    
    tmpDir := t.TempDir()
    logFile := filepath.Join(tmpDir, "test_global.jsonl")
    
    cfg := Config{...}
    logger, cleanup, err := NewWithGlobal(cfg)
    if err != nil {
        t.Fatalf("не удалось создать глобальный логгер: %v", err)
    }
    defer func() {
        if err := cleanup(); err != nil {
            t.Errorf("ошибка при очистке: %v", err)
        }
    }()
    
    // Используем глобальные функции
    Info("Глобальное сообщение", "key", "value")
    Flush()
    
    // Проверяем файл логов
    content, err := os.ReadFile(logFile)
    // ...
}
```

**❌ Неправильно (исправлено):**

```go
// Было (до исправления):
func TestGlobalLogger_Functions(t *testing.T) {
    t.Parallel() // ❌ Гонка за глобальное состояние!
    
    logger, cleanup, err := New(cfg)
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    SetGlobal(logger) // ❌ Другие тесты тоже это делают!
    
    Debug("сообщение") // ❌ Гонка!
    Info("сообщение")  // ❌ Гонка!
}
```

---

## Checklist для code review

### Изоляция

- [ ] Тест не зависит от других тестов
- [ ] Тест не использует глобальное состояние (или корректно его изолирует)
- [ ] Тест использует `t.TempDir()` для временных файлов
- [ ] Тест очищает за собой ресурсы (`defer cleanup()`)

### Параллельность

- [ ] `t.Parallel()` используется только в изолированных тестах
- [ ] Тесты с глобальным состоянием **НЕ** используют `t.Parallel()`
- [ ] Подтесты в таблице тестов используют `t.Parallel()` внутри `t.Run()`
- [ ] Есть комментарий почему `t.Parallel()` нельзя использовать (если применимо)

### Надёжность

- [ ] Тест детерминированный (одинаковый результат при многократном запуске)
- [ ] Тест не зависит от времени (или использует моки времени)
- [ ] Тест не зависит от случайных значений (или использует фиксированный seed)
- [ ] Тест имеет адекватный таймаут
- [ ] Тест проходит многократный прогон (`go test -count=10`)

### Покрытие

- [ ] Тест покрывает happy path
- [ ] Тест покрывает error cases
- [ ] Тест покрывает граничные условия
- [ ] Тест имеет понятные сообщения об ошибках

### Производительность

- [ ] Тест выполняется < 1 секунды (для unit-тестов)
- [ ] Тест не делает лишних аллокаций
- [ ] Benchmark-тесты имеют `b.ResetTimer()`

---

## Отладка падающих тестов

### Шаг 1: Воспроизведение проблемы

```bash
# Запустить тест несколько раз
go test -count=10 -v ./pkg/xlog/... -run TestName

# С race detector
go test -race -count=10 -v ./pkg/xlog/... -run TestName
```

### Шаг 2: Анализ вывода

**Ищите паттерны:**

- `WARNING: DATA RACE` — гонка данных
- `panic: test timed out` — тест завис
- `failed` в разных прогонах — нестабильный тест

### Шаг 3: Изоляция проблемы

```bash
# Запустить только проблемный тест
go test -race -count=20 -timeout=5m ./pkg/xlog/... -run TestName

# Запустить все тесты кроме проблемного
go test -race ./pkg/xlog/... -skip TestName
```

### Шаг 4: Проверка на глобальное состояние

**Вопросы для анализа:**

1. Использует ли тест `SetGlobal()`, `GetGlobal()`?
2. Использует ли тест глобальные функции (`Info()`, `Debug()`, `Error()`)?
3. Модифицирует ли тест глобальные переменные?
4. Использует ли тест общие файлы/порты без изоляции?

**Если да → убрать `t.Parallel()`**

### Шаг 5: Проверка на утечку горутин

```bash
# Запустить с race detector и большим количеством прогонов
go test -race -count=50 ./pkg/xlog/... -run TestName

# Использовать goleak (если подключён)
go test -race ./pkg/xlog/... -run TestName
```

### Пример отладки

**Проблема:** Тест падает случайно при `-count=20`

```bash
# 1. Воспроизводим
go test -race -count=20 ./pkg/xlog/... -run TestGlobalLogger_Functions

# 2. Видим ошибку: DATA RACE
# WARNING: DATA RACE
# Write by goroutine 123:
#   myVpnServices/pkg/xlog.SetGlobal()
#   
# Previous write by goroutine 45:
#   myVpnServices/pkg/xlog.SetGlobal()

# 3. Анализируем код
# Находим: тест использует t.Parallel() и SetGlobal()

# 4. Исправляем
# Убираем t.Parallel() из теста

# 5. Проверяем
go test -race -count=20 ./pkg/xlog/... -run TestGlobalLogger_Functions
# ✅ PASS
```

---

## Приложения

### A. Команды для быстрой проверки

```bash
# Перед коммитом
make check-all

# Перед пулом
make check-release

# После изменений в тестах
make test-stability
```

### B. Шаблоны тестов

**Изолированный тест:**

```go
func TestSomething(t *testing.T) {
    t.Parallel() // ✅ Безопасно
    
    tmpDir := t.TempDir()
    
    logger, cleanup, err := New(Config{
        Level: "debug",
        File: FileConfig{
            Path: filepath.Join(tmpDir, "test.log"),
        },
    })
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    logger.Info("тест")
    
    // Проверяем результат
}
```

**Тест с глобальным состоянием:**

```go
func TestWithGlobal(t *testing.T) {
    // t.Parallel() // ❌ Убрано: глобальное состояние
    
    logger, cleanup, err := NewWithGlobal(Config{...})
    if err != nil {
        t.Fatal(err)
    }
    defer cleanup()
    
    // Используем глобальные функции
    Info("тест")
    
    // Проверяем результат
}
```

### C. Полезные ссылки

- [Testing package (testing)](https://pkg.go.dev/testing)
- [Go Concurrency Patterns](https://go.dev/talks/2012/concurrency.slide#1)
- [Advanced Go Testing](https://go.dev/talks/2021/advanced-testing.slide#1)
