# Анализ: Anthropic / claude-code-opus-4.6

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-opus-4.6.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-opus-4.6
- **Объём:** 170 561 символ

## Структура
1. **System prompt / Определение роли** — объявление ассистента как Claude Code, официального CLI Anthropic для задач разработки ПО
2. **Guardrails / Безопасность** — правила разрешённого/запрещённого использования, отказа от вредоносных запросов
3. **System** — общие правила работы: форматирование, permission mode, обработка system-reminder, hooks, сжатие контекста
4. **Doing tasks** — инструкции по выполнению задач: приоритеты, стиль кода, комментирование, тестирование UI
5. **Executing actions with care** — правила осторожного выполнения: оценка обратимости, blast radius, примеры рискованных действий
6. **Using your tools** — правила использования инструментов: предпочтение Read/Edit/Write над Bash, TaskCreate, параллельные вызовы
7. **Tone and style** — стиль общения: без эмодзи, кратко, ссылки на файлы с line_number
8. **Text output** — правила текстового вывода: краткие обновления, без нарратива внутренних размышлений, end-of-turn summary
9. **Session-specific guidance** — специфические инструкции: Agent tool, Explore, Skills, scratchpad
10. **auto memory** — система персистентной памяти: типы (user/feedback/project/reference), правила сохранения, MEMORY.md индекс
11. **Environment** — информация об окружении (ОС, shell, модель, дата)
12. **Scratchpad Directory** — указание директории для временных файлов
13. **Context management** — управление контекстом при длинных разговорах
14. **Session context** — контекст сессии: git status, CLAUDE.md, email пользователя, текущая дата
15. **Agents** — описание доступных типов агентов с их возможностями
16. **Skills** — описание доступных навыков (deep-research, dataviz, code-review и др.)
17. **Tools** — полное описание всех инструментов с JSON-схемами параметров

## Persona
Ассистент объявлен как «Claude Code, Anthropic's official CLI for Claude» — официальный CLI-инструмент Anthropic для задач разработки ПО. Тон деловой, технический, без эмодзи. Рамки: интерактивный агент для software engineering задач с акцентом на безопасность, осторожность и эффективность. Ассистент позиционируется как высококомпетентный помощник, способный выполнять амбициозные задачи («You are highly capable and often allow users to complete ambitious tasks»).

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are Claude Code, Anthropic's official CLI for Claude. You are an interactive agent that helps users with software engineering tasks.» |
| Guardrails | да | 5 | «Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes.» |
| Few-shot | да | 3 | Примеры memory entries (user/feedback/project/reference), примеры рискованных действий, примеры Agent tool — но нет полноценных диалогов «вход → выход» |
| Chain-of-thought | да | 4 | «Carefully consider the reversibility and blast radius of actions», «measure twice, cut once», «think about why the user has denied the tool call» |
| Output format | да | 5 | «Github-flavored markdown for formatting», «responses should be short and concise», «end-of-turn summary: one or two sentences», «default to writing no comments» |
| Работа с инструментами | да | 5 | Полные JSON-схемы для каждого инструмента, правила выбора («Prefer dedicated tools over Bash»), правила параллельных вызовов, git-протокол |

**Итоговая оценка:** 4.5 / 5

## Сильные стороны
- **Исключительно детальная система guardrails** — категоризация рискованных действий по обратимости и blast radius с конкретными примерами (destructive operations, hard-to-reverse operations, actions visible to others)
- **Система персистентной памяти (auto memory)** — типизированные записи (user/feedback/project/reference) с frontmatter, MEMORY.md индексом, правилами что/когда сохранять и примерами для каждого типа
- **Полное описание инструментов с JSON-схемами** — каждый инструмент документирован со схемой параметров, что исключает неоднозначность при вызове
- **Чёткие правила стиля и формата** — конкретные требования к длине ответов, использованию emoji, формату ссылок на код

## Слабые места
- **Мало few-shot примеров** — отсутствуют полноценные примеры диалогов «запрос пользователя → ответ ассистента». Есть только примеры memory entries и примеры рискованных действий, но не примеры решения задач
- **Огромный объём (170K символов)** — может быть избыточным; часть информации (полные JSON-схемы всех инструментов) могла бы быть вынесена в отдельные файлы
- **Нет явного chain-of-thought** — нет требования «think step by step» или «reason before answering»; рассуждение подразумевается, но не формализовано

## Что заимствовать
- **Систему типизированной памяти** — формат frontmatter (name/description/metadata.type), MEMORY.md как индекс, правила «что не сохранять» (код, git-история, ephemeral task details)
- **Подход к guardrails** — категоризация по обратимости (reversible vs hard-to-reverse vs actions visible to others) с конкретными примерами в каждой категории
- **Формат описания инструментов** — JSON Schema для параметров каждого инструмента с required полями и описаниями