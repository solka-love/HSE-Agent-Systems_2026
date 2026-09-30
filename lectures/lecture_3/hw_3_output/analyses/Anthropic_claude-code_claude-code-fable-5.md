# Анализ: Anthropic / Claude Code (Fable 5)

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-fable-5.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-fable-5
- **Объём:** 328 167 символов

## Структура
1. **System prompt header** — заголовок и таблица соответствия effort settings значениям reasoning_effort
2. **Reasoning effort & thinking mode** — установка reasoning_effort=40, thinking_mode=auto
3. **Role definition** — объявление роли: «You are Claude Code, Anthropic's official CLI for Claude»
4. **Security guardrails** — правила безопасности: разрешённые и запрещённые сценарии использования
5. **Harness** — описание окружения: вывод в терминал, permission mode, system updates, параллельные вызовы инструментов
6. **Communicating with the user** — правила коммуникации: TLDR, читаемость, структура ответов, стиль кода, местоимения
7. **Model identity** — самоидентификация как Claude Fable 5, описание модельной линейки
8. **Session-specific guidance** — команды `!` и `/skill-name` для пользователя
9. **Memory** — система файловой памяти с frontmatter (name, description, metadata), MEMORY.md
10. **Environment** — информация о доступных моделях Claude и платформах Claude Code
11. **Context management** — summarisation контекста при длинных диалогах
12. **Autonomous operation** — правила автономной работы без подтверждения пользователя
13. **Browser automation (Claude in Chrome)** — инструкции по браузерной автоматизации, GIF-запись, консоль, диалоги
14. **Session context** — кодовая база пользователя, CLAUDE.md, git status, окружение
15. **Agents** — описание типов агентов (claude, claude-code-guide, Explore, general-purpose, Plan и др.)
16. **MCP Server Instructions** — инструкции для MCP-серверов (claude-in-chrome, computer-use)
17. **Skills** — список доступных навыков с описаниями
18. **Tools** — полные JSONSchema-определения всех инструментов (Agent, Artifact, Bash, Edit, Read, Write и др.)

## Persona
Ассистент объявлен как **Claude Code** — официальный CLI-инструмент Anthropic для работы с программной инженерией. Тон — технический, профессиональный, ориентированный на продуктивность. Рамки заданы через модель **Claude Fable 5** (первая модель семейства Claude 5, Mythos-класс). Ассистент позиционируется как автономный исполнитель, работающий без实时ного наблюдения пользователя.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are Claude Code, Anthropic's official CLI for Claude.» |
| Guardrails | да | 5 | «Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise» |
| Few-shot | нет | 1 | отсутствует — нет примеров диалогов или демонстраций входа/выхода |
| Chain-of-thought | нет | 1 | отсутствует — нет требования думать перед ответом или проверять себя |
| Output format | да | 4 | «Lead with the outcome. Your first sentence after finishing should answer 'what happened'» |
| Работа с инструментами | да | 5 | Полные JSONSchema-схемы для всех инструментов, правила параллельных вызовов |

**Итоговая оценка:** 3.5 / 5

## Сильные стороны
- **Исключительно проработанные guardrails** — чёткое разделение разрешённого (authorized security testing, CTF, education) и запрещённого (DoS, supply chain compromise, destructive techniques) с контекстными исключениями для dual-use инструментов
- **Глубокая интеграция с окружением** — файловая память с frontmatter, MEMORY.md, git status, CLAUDE.md, переменные окружения
- **Детальная спецификация инструментов** — каждый инструмент описан через полную JSONSchema, включая все параметры, ограничения и правила использования
- **Правила коммуникации** — подробные инструкции по TLDR, читаемости, стилю кода, использованию местоимений

## Слабые места
- **Отсутствие few-shot примеров** — нет ни одного примера диалога или демонстрации ожидаемого формата ответа, что снижает предсказуемость поведения
- **Отсутствие chain-of-thought** — модель не инструктируется думать перед ответом, планировать или верифицировать свои выводы, что может приводить к premature ответам
- **Чрезмерный объём** — 328K символов, большая часть которых — JSONSchema инструментов, что создаёт риск потери ключевых инструкций в шуме

## Что заимствовать
- **Система guardrails с контекстными исключениями** — формулировка «Dual-use security tools require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases» — отличный шаблон для безопасного разрешения потенциально опасных инструментов
- **Файловая память с frontmatter** — структура памяти (name, description, metadata type) и MEMORY.md как индекс — эффективный паттерн для долгосрочной памяти
- **Правило TLDR** — «Lead with the outcome. Your first sentence after finishing should answer 'what happened'» — универсальный приём для любого ассистента