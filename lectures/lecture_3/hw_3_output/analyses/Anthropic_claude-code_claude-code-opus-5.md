# Анализ: Anthropic / claude-code-opus-5

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-opus-5.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-opus-5
- **Объём:** 138 750 символов

## Структура
1. **System prompt / Role definition** — объявление ассистента как Claude Code, CLI для Claude, интерактивный агент для задач software engineering
2. **Guardrails / Security policy** — правила безопасности: разрешённое и запрещённое использование, контекст авторизации для dual-use инструментов
3. **Harness** — правила работы: вывод в markdown, обработка отклонённых вызовов инструментов, системные обновления, приоритет dedicated-инструментов, стиль кода, местоимения, подтверждения для необратимых действий
4. **Session-specific guidance** — инструкции по shell-командам через `!` и вызову skills через `/skill-name`
5. **Memory** — система файловой памяти с frontmatter (name, description, metadata), типами памяти (user/feedback/project/reference), правилами дедупликации и MEMORY.md-индексом
6. **Environment** — информация о среде: ОС, shell, модель (Opus 5, 1M контекст), версии Claude-моделей
7. **Scratchpad Directory** — указание использовать `<scratchpad-dir>` вместо `/tmp`
8. **Context management** — правила работы при summarisation контекста
9. **Delivering work** — философия выполнения работы: действовать по запросу, не сужать/расширять scope, разрешать неоднозначности, завершать полностью
10. **Corrections** — правила исправления ошибок: только если ошибка влияет на код/выводы, без извинений и самокритики
11. **Session context** — git status, CLAUDE.md, userEmail, currentDate
12. **Agents** — описание доступных типов агентов (claude, claude-code-guide, Explore, general-purpose, Plan и др.)
13. **Skills** — список доступных навыков (dataviz, artifact-design, artifact-capabilities, update-config и др.)
14. **Tools** — полные JSON-схемы всех инструментов (Agent, Artifact, AskUserQuestion, Bash, CronCreate, Edit, Monitor, Read, Write и др.)

## Persona
Ассистент объявлен как **Claude Code** — официальный CLI-инструмент Anthropic для Claude. Это интерактивный агент для задач software engineering. Тон — профессиональный, технический, без излишней эмоциональности. Рамки заданы строго: ассистент — инструмент для разработки, а не универсальный собеседник. Присутствуют правила инклюзивности (нейтральные местоимения they/them по умолчанию).

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | "You are Claude Code, Anthropic's official CLI for Claude. You are an interactive agent that helps users with software engineering tasks." |
| Guardrails | да | 5 | "Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes." |
| Few-shot | нет | 1 | Отсутствуют — нет демонстраций входа/выхода, образцов диалогов или примеров использования |
| Chain-of-thought | частично | 2 | "When you have enough information to act, act. Do not re-derive facts already established" — скорее анти-CoT, требование действовать, а не размышлять вслух |
| Output format | да | 4 | "Text you output outside of tool use is displayed to the user as Github-flavored markdown in a terminal" + формат памяти с frontmatter |
| Работа с инструментами | да | 5 | Полные JSON-схемы 20+ инструментов с правилами использования, приоритетами и примерами |

**Итоговая оценка:** 3.7 / 5

## Сильные стороны
- **Исключительно детальная работа с инструментами** — каждый инструмент описан полной JSON-схемой с правилами использования, триггерами и примерами. Это задаёт чёткие границы и предотвращает неверные вызовы.
- **Продуманная система памяти** — файловая память с frontmatter, типами (user/feedback/project/reference), дедупликацией и индексом MEMORY.md — лучшая реализация долгосрочной памяти среди виденных промптов.
- **Чёткие guardrails** — конкретные запреты с контекстными исключениями (пентесты, CTF, исследования), а не расплывчатые "будь этичным".

## Слабые места
- **Отсутствие few-shot примеров** — нет ни одного образца диалога или демонстрации входа/выхода. Для CLI-инструмента это упущение: примеры могли бы задать ожидаемый паттерн взаимодействия.
- **Chain-of-thought не поощряется** — промпт явно требует действовать, а не размышлять ("When you have enough information to act, act"). Для сложных задач software engineering это может приводить к преждевременным решениям.
- **Огромный объём** — 138К символов делает промпт дорогим в использовании и сложным для поддержки.

## Что заимствовать
- **Система файловой памяти** — формат frontmatter (name, description, metadata), типизация памяти (user/feedback/project/reference), дедупликация и индексный файл — зрелая архитектура, пригодная для любого агента с долгосрочной памятью.
- **Правило нейтральных местоимений** — "A name doesn't tell you someone's pronouns; a wrong guess misgenders a real person in a way the neutral default never does" — элегантная формулировка инклюзивного поведения.
- **Философия delivering work** — "Interpret ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work" — задаёт правильный баланс автономии и осторожности.