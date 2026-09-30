# Анализ: Anthropic / claude-code-opus-4.8

## Метаданные
- **Путь:** Anthropic/claude-code/claude-code-opus-4.8.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-opus-4.8
- **Объём:** 132 695 символов

## Структура
1. **System prompt / Определение роли** — объявление ассистента как Claude Code, интерактивного агента для задач разработки ПО
2. **Guardrails / Правила безопасности** — разграничение разрешённого и запрещённого использования инструментов безопасности
3. **Harness / Техническая обвязка** — описание вывода, разрешений, системных напоминаний, параллельных вызовов инструментов
4. **Communicating with the user / Стиль общения** — правила написания ответов: TLDR-структура, читаемость, тон, согласование, местоимения
5. **Session-specific guidance / Сессионные инструкции** — подсказки по shell-командам и вызову навыков
6. **Memory / Система памяти** — формат файлов памяти, типы (user/feedback/project/reference), индексация
7. **Environment / Окружение** — информация о системе, модели, версиях Claude
8. **Scratchpad Directory / Временная директория** — указание использовать `<scratchpad-dir>` вместо `/tmp`
9. **Context management / Управление контекстом** — правила summarisation и принятия решений
10. **Session context / Контекст сессии** — git-статус, CLAUDE.md, email, дата
11. **Agents / Типы агентов** — описание 8 типов агентов (claude, claude-code-guide, Explore, Plan и др.)
12. **Skills / Навыки** — перечень 20+ навыков с описанием триггеров
13. **Tools / Инструменты** — полные JSON-схемы всех инструментов (Agent, Artifact, Bash, Edit, Read, Write и др.)

## Persona
Ассистент объявлен как **Claude Code** — официальный CLI-инструмент Anthropic для Claude. Это интерактивный агент для задач программной инженерии. Тон — профессиональный, технический, ориентированный на сотрудничество с разработчиком. Заданы чёткие рамки: ассистент пишет для «коллеги, который отошёл и навёрстывает», а не для лог-файла. Используются нейтральные местоимения (they/them) по умолчанию.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are Claude Code, Anthropic's official CLI for Claude. You are an interactive agent that helps users with software engineering tasks.» |
| Guardrails | да | 5 | «IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques…» |
| Few-shot | нет | 1 | Отсутствует — нет демонстраций входа/выхода или образцов диалогов |
| Chain-of-thought | да | 4 | «Before your first tool call, say in a sentence what you're about to do» + «Lead with the outcome» — поощряет структурированное мышление, но не требует явного CoT |
| Output format | да | 5 | «Your text output is what the user reads between tool calls… Lead with the outcome… Write code that reads like the surrounding code…» — детальные правила форматирования |
| Работа с инструментами | да | 5 | Полные JSON-схемы для 20+ инструментов с правилами выбора, параллелизма, обработки ошибок |

**Итоговая оценка:** 4.2 / 5

## Сильные стороны
- **Исключительно детальная спецификация инструментов** — каждый инструмент описан с полной JSON-схемой, примерами использования и правилами выбора. Это задаёт жёсткий контракт, исключающий неоднозначность.
- **Многоуровневая система guardrails** — не просто запреты, а разграничение контекстов (пентест vs вредоносная атака) с конкретными примерами.
- **Коммуникационные правила** — подробные инструкции по стилю (TLDR, читаемость, местоимения, тон под эксперта/новичка) делают промпт образцовым по части UX.

## Слабые места
- **Отсутствие few-shot примеров** — ни одного образца диалога или демонстрации «вход → выход». Для столь сложного промпта few-shot могли бы улучшить консистентность ответов.
- **Избыточный объём** — 132К символов. Часть содержимого (полные JSON-схемы инструментов, списки агентов/скиллов) могла бы быть вынесена в отдельные файлы и подгружаться по необходимости.

## Что заимствовать
- **Формат guardrails с контекстной квалификацией**: «Assist with authorized security testing… Dual-use security tools require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases» — вместо плоского запрета используется условное разрешение.
- **Правило TLDR**: «Lead with the outcome. Your first sentence after finishing should answer 'what happened' or 'what did you find'» — универсальный приём для любого ассистента.
- **Система памяти с фронтматером**: структурированное хранение фактов с типизацией (user/feedback/project/reference) и перекрёстными ссылками `[[name]]`.