# Анализ: Anthropic / Claude Code (headless-fable-5.1)

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-headless-fable-5.1.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-headless-fable-5.1
- **Объём:** ~203 000 символов

## Структура
1. **Reasoning effort settings** — таблица конфигурации усилия рассуждения (low/medium/high/xhigh/max)
2. **Role definition** — объявление ассистента: «You are a Claude agent, built on Anthropic's Claude Agent SDK»
3. **Reporting outcomes** — правила честной отчётности: сообщать факты, а не намерения; не скрывать ошибки
4. **Security guardrails** — рамки допустимых действий: авторизованный security testing, CTF; отказ от вредоносных техник
5. **Harness** — описание среды: markdown в терминале, permission mode, hooks, параллельные вызовы инструментов
6. **Communication style** — правила общения: pronouns (they/them), подтверждение перед необратимыми действиями
7. **Model identity** — идентификация модели: Claude Fable 5.1, Mythos-class, ссылка на страницу продукта
8. **Session-specific guidance** — обработка slash-команд через Skill
9. **Memory** — система файловой памяти с frontmatter (name, description, metadata), MEMORY.md-индекс
10. **Environment** — информация о моделях Claude 5 family, Claude Code CLI/desktop/web/IDE
11. **Context management** — правила summarisation при длинных разговорах
12. **Delivering work** — правила выполнения задач: не сужать/расширять scope, действовать по фактам
13. **Writing for the user** — детальные правила форматирования сообщений (длина предложений, запрет em-dash, структура)
14. **Autonomous operation** — правила работы без пользователя: не спрашивать разрешения на обратимые действия
15. **Session context** — контекст сессии: CLAUDE.md, git status, окружение
16. **Agents** — описание 5 типов агентов (claude, Explore, general-purpose, Plan, statusline-setup)
17. **Skills** — описание 15+ навыков (dataviz, code-review, loop, schedule, claude-api и др.)
18. **Tools** — полные JSON-схемы всех инструментов (Agent, Bash, CronCreate, Edit, Read, Write, Monitor и др.)

## Persona
Ассистент объявлен как «Claude agent, built on Anthropic's Claude Agent SDK» с явной идентификацией «Claude Fable 5.1» — newest model в Claude 5 family, Mythos-class. Тон деловой и технический, без разговорных элементов. Заданы строгие рамки: ассистент — инструмент для software engineering, а не собеседник. Подчёркнута автономность: пользователь не смотрит в реальном времени, вопросы блокируют работу.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are a Claude agent, built on Anthropic's Claude Agent SDK» + «Claude Fable 5.1, the newest model in Anthropic's Claude 5 family» |
| Guardrails | да | 4 | «Assist with authorized security testing, defensive security, CTF challenges… Refuse requests for destructive techniques, DoS attacks, mass targeting» |
| Few-shot | нет | 1 | отсутствует — нет примеров диалогов, образцов входа/выхода или демонстраций |
| Chain-of-thought | частично | 2 | «Before you start, say in a line what you're about to do» — планирование, но не CoT; reasoning_effort задан числом, без инструкции «думай шаг за шагом» |
| Output format | да | 5 | «Lead with the answer or outcome… One idea per sentence… No em-dashes… Keep code out of prose… Use a bulleted or numbered list for parallel items» |
| Работа с инструментами | да | 5 | Полные JSON-схемы всех инструментов; правила параллельных вызовов; «make all of the independent calls in the same block» |

**Итоговая оценка:** 3.7 / 5

## Сильные стороны
- **Исключительно детальная спецификация формата вывода** — 12+ правил, регулирующих длину предложений, структуру абзацев, использование списков, запрет на em-dash и parentheticals. Это обеспечивает предсказуемый, лаконичный и читаемый вывод.
- **Полная инструментальная документация** — каждый инструмент описан с JSON-схемой, описанием when-to-use и примерами. Это устраняет неоднозначность при выборе инструмента.
- **Система памяти с frontmatter** — структурированное хранение фактов с метаданными (type, description), индексирование через MEMORY.md и связывание через [[wiki-links]].

## Слабые места
- **Отсутствие few-shot примеров** — нет ни одного образца диалога или демонстрации ожидаемого поведения. Для промпта такого объёма это заметный пробел.
- **Chain-of-thought не реализован** — несмотря на наличие reasoning_effort, нет явной инструкции «думай шаг за шагом», «проверь себя перед ответом» или «распиши ход рассуждений». CoT заменён планированием («say what you're about to do»).
- **Огромный объём** — ~203 000 символов. Большая часть — JSON-схемы инструментов, которые могли бы быть вынесены в отдельные файлы.

## Что заимствовать
- **Правила форматирования вывода** — конкретные, проверяемые ограничения (длина предложения ~20 слов, один абзац = одна идея, запрет em-dash). Пригодны для любого промпта, генерирующего текст для пользователя.
- **Система памяти с frontmatter** — структура name/description/metadata + MEMORY.md-индекс + [[wiki-links]] — отличный паттерн для долгосрочной памяти агента.
- **Правило честной отчётности** — «Report what actually happened, not what you intended» — универсальный принцип для любого агента, работающего с инструментами.