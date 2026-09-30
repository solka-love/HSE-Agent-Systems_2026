# Анализ: Anthropic / claude-code-fable-5.1

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-fable-5.1.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-fable-5.1
- **Объём:** 331 019 символов

## Структура
1. **System prompt header / Effort settings** — таблица уровней reasoning_effort (low→max)
2. **Role definition** — «You are Claude Code, Anthropic's official CLI for Claude»
3. **Reporting outcomes** — правила честной отчётности о результатах работы
4. **Security guardrails** — разрешённые и запрещённые сценарии безопасности
5. **Harness** — описание среды выполнения, tool use, permission mode
6. **Model identity** — идентификация как Claude Fable 5.1, Mythos-class tier
7. **Session-specific guidance** — инструкции по `!`-префиксу и `/skill-name`
8. **Memory system** — файловая система памяти с frontmatter и MEMORY.md-индексом
9. **Environment** — информация о моделях Claude и платформах Claude Code
10. **Context management** — правила summarisation контекста
11. **Delivering work** — правила объёма работы, обработки неопределённостей, отказов
12. **Writing for the user** — строгие правила форматирования сообщений пользователю
13. **Autonomous operation** — правила автономной работы без вопросов пользователю
14. **Claude in Chrome browser automation** — инструкции по браузерной автоматизации
15. **Session context** — контекст сессии (CLAUDE.md, memory, git status, userEmail)
16. **Agents** — описание доступных типов агентов (claude, Explore, Plan и др.)
17. **MCP Server Instructions** — инструкции для claude-in-chrome и computer-use MCP
18. **Skills** — описание доступных навыков (design, dataviz, code-review и др.)
19. **Tools** — полные JSONSchema всех доступных инструментов

## Persona
Ассистент объявлен как «Claude Code, Anthropic's official CLI for Claude» — это не просто модель, а конкретный продукт (CLI-интерфейс). Дополнительно идентифицируется как «Claude Fable 5.1, the newest model in Anthropic's Claude 5 family and part of the Mythos-class model tier that sits above Claude Opus in capability». Тон — технический, деловой, с акцентом на точность, честность и автономность. Рамки заданы строго: ассистент — инструмент для software engineering задач, работающий в терминале.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are Claude Code, Anthropic's official CLI for Claude» |
| Guardrails | да | 5 | «Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise» |
| Few-shot | нет | 1 | отсутствует |
| Chain-of-thought | да | 3 | «Before you start, say in a line what you're about to do» — частичное, без явного CoT |
| Output format | да | 5 | «Lead with the answer or outcome. One idea per sentence, about 20 words, with a verb. No em-dashes, no parentheticals» |
| Работа с инструментами | да | 5 | Полные JSONSchema всех инструментов, правила выбора и последовательности вызовов |

**Итоговая оценка:** 4.0 / 5

## Сильные стороны
- **Исключительно детальная спецификация формата вывода** — правила для сообщений пользователю прописаны до уровня «одна идея на предложение, ~20 слов, без тире и скобок». Это обеспечивает консистентность ответов.
- **Мощная система guardrails** — чёткое разделение разрешённого (authorized security testing, CTF, education) и запрещённого (DoS, supply chain compromise, destructive techniques).
- **Полная инструментальная документация** — все инструменты описаны с JSONSchema прямо в промпте, что исключает неоднозначность.
- **Система памяти с frontmatter и индексацией** — продуманная файловая память с типами (user/feedback/project/reference) и перекрёстными ссылками.

## Слабые места
- **Отсутствие few-shot примеров** — нет ни одного примера диалога или демонстрации входа/выхода, что могло бы улучшить консистентность в сложных сценариях.
- **CoT реализован лишь частично** — нет явного требования «думать перед ответом» или «планировать шаги». Указание «Before you start, say in a line what you're about to do» — это скорее коммуникация, чем reasoning.
- **Чрезмерный объём** — 331 КБ делает промпт сложным для восприятия и поддержки. Многие секции (полные JSONSchema инструментов) могли бы быть вынесены в отдельные файлы.

## Что заимствовать
- **Формат памяти с frontmatter** — `name`, `description`, `metadata.type` и перекрёстные ссылки `[[name]]` — отличный паттерн для структурированного долговременного хранения.
- **Правила форматирования сообщений** — конкретные, измеримые правила (длина предложений, запрет на em-dash, структура списков) могут быть адаптированы для любого агента, работающего с пользователем.
- **Система guardrails с примерами** — перечисление конкретных запрещённых техник (DoS, C2 frameworks, credential testing без контекста) вместо абстрактных запретов.