# Анализ: Anthropic / claude-code-guide

## Метаданные
- **Путь:** Anthropic/claude-code/agents/claude-code-guide.md
- **Вендор:** Anthropic
- **Продукт:** claude-code-guide
- **Объём:** 9305 символов

## Структура
1. **YAML frontmatter** — метаданные агента: имя, whenToUse, список инструментов (Bash, Read, WebFetch, WebSearch), модель (haiku), permissionMode (dontAsk)
2. **Определение роли** — объявление persona: «You are the Claude guide agent» с описанием основной ответственности
3. **Пять доменов экспертизы** — детальное описание каждой области знаний (Claude Code CLI, Claude Agent SDK, Claude API, Claude Tag, Plugin eval / skill-doctor) с разграничениями между продуктами
4. **Документационные источники** — четыре URL-адреса документации (code.claude.com, platform.claude.com, claude.com/docs) с указанием, какой источник для какого домена использовать
5. **Approach (подход)** — пошаговая инструкция из 7 шагов: определить домен → WebFetch docs map → найти URL → загрузить страницы → дать ответ → WebSearch при необходимости → прочитать локальные файлы
6. **Guidelines** — правила: приоритет документации, предупреждение об устаревших данных, запрет ответов из памяти для Claude Tag, ссылка на GitHub issues

## Persona
Ассистент объявлен как «Claude guide agent» — гид-проводник по экосистеме продуктов Claude. Тон профессиональный, информативный, строго ориентированный на официальную документацию. Рамки чётко заданы пятью доменами экспертизы, выход за которые не предполагается. Ассистент позиционируется как знающий, но осторожный — он предупреждает, что его тренировочные данные могут быть устаревшими, и всегда ссылается на документацию.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are the Claude guide agent. Your primary responsibility is helping users understand and use Claude Code, the Claude Agent SDK, and the Claude API effectively.» |
| Guardrails | да | 4 | «Your training data about Claude Code commands, flags, and settings may be out of date. If WebFetch or WebSearch fail… do not silently answer from memory» |
| Few-shot | нет | 1 | Отсутствует — нет ни одного примера диалога или демонстрации входа/выхода |
| Chain-of-thought | да | 4 | «Approach: 1. Determine which domain… 2. Use WebFetch… 3. Identify… 4. Fetch… 5. Provide… 6. Use WebSearch… 7. Reference local project files» |
| Output format | нет | 2 | Есть только мягкие рекомендации: «Keep responses concise and actionable», «Include specific examples or code snippets when helpful» — без строгой структуры |
| Работа с инструментами | да | 5 | Чётко перечислены инструменты (Bash, Read, WebFetch, WebSearch) и описана последовательность их вызова в Approach |

**Итоговая оценка:** 3.5 / 5

## Сильные стороны
- **Превентивные guardrails против устаревших знаний** — явное указание, что training data может быть устаревшей, и требование не отвечать из памяти при недоступности документации. Это лучшая практика для агентов, работающих с быстро меняющимися продуктами.
- **Чёткое разграничение доменов** — каждый из пяти доменов описан с указанием, что в него входит, а что нет (например, «Do not conflate the Claude API Tool Runner with the Claude Agent SDK»). Это предотвращает путаницу.
- **Привязка доменов к конкретным URL документации** — для каждого домена указан точный URL docs map, что исключает угадывание адресов.

## Слабые места
- **Отсутствие few-shot примеров** — нет ни одного образца диалога «вопрос → ответ», что снижает предсказуемость стиля ответов.
- **Нет строгого формата вывода** — промпт не требует конкретной разметки (например, секции, заголовки, code blocks), из-за чего ответы могут быть разнородными.
- **Chain-of-thought задан как последовательность действий, а не как требование рассуждать** — CoT здесь процедурный (что делать), а не когнитивный (как думать), что менее эффективно для сложных вопросов.

## Что заимствовать
- **Приём «whenToUse» в YAML frontmatter** — чёткое описание триггеров активации агента: «Use this agent when the user asks questions about…». Позволяет маршрутизировать запросы между агентами.
- **Формулировка предупреждения об устаревших данных:** «Your training data about [тема] may be out of date. If [инструмент] fails… do not silently answer from memory: tell the user you could not reach the documentation, give the best answer you have, and explicitly note it may be out of date with a link to [URL]».
- **Структура «домены экспертизы + документационные источники»** — каждый домен описан отдельным блоком с указанием URL, что делает промпт самодостаточным и легко расширяемым.