# Анализ: Anthropic / general-purpose (Claude Code Agent)

## Метаданные
- **Путь:** Anthropic/claude-code/agents/general-purpose.md
- **Вендор:** Anthropic
- **Продукт:** general-purpose (агент для Claude Code CLI)
- **Объём:** 1784 символов

## Структура
1. **Frontmatter (YAML)** — метаданные агента: имя (`general-purpose`), условие применения (`whenToUse`), модель (`inherit`)
2. **Определение роли** — «You are an agent for Claude Code» — объявление идентичности ассистента
3. **Инструкция по выполнению** — «Complete the task fully — don't gold-plate, but don't leave it half-done» — принцип полноты без избыточности
4. **Формат отчёта** — требование ответить кратким отчётом по завершении задачи
5. **Список сильных сторон** — 4 пункта: поиск кода, анализ архитектуры, исследование вопросов, многошаговые задачи
6. **Guidelines (правила работы)** — 6 правил: стратегия поиска, сужение анализа, тщательность, запрет на создание файлов без необходимости, запрет на документацию без запроса, запрет на ре-делегирование

## Persona
Ассистент объявлен как специализированный агент для Claude Code — CLI-инструмента Anthropic. Тон сугубо деловой и инструктивный, без эмоциональной окраски. Рамки идентичности узкие: это не универсальный помощник, а целенаправленный инструмент для поиска кода, анализа и многошаговых исследований. Persona скорее функциональная, чем характерная — нет имени, голоса или стиля общения.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 4 | «You are an agent for Claude Code, Anthropic's official CLI for Claude» |
| Guardrails | да | 4 | «NEVER create files unless they're absolutely necessary for achieving your goal» |
| Few-shot | нет | 1 | отсутствует |
| Chain-of-thought | частично | 2 | «Start broad and narrow down. Use multiple search strategies if the first doesn't yield results» |
| Output format | да | 3 | «respond with a concise report covering what was done and any key findings» |
| Работа с инструментами | да | 3 | «Use `Read` when you know the specific file path» / «search broadly when you don't know where something lives» |

**Итоговая оценка:** 2.8 / 5

## Сильные стороны
- **Чёткие guardrails**: запрет на создание лишних файлов и документации без явного запроса — предотвращает «мусорные» артефакты.
- **Конкретная стратегия поиска**: различие между broad search (когда не знаешь путь) и Read (когда знаешь путь) — практичная эвристика.
- **Принцип «не золотить, но и не бросать»**: баланс между полнотой и минимализмом.

## Слабые места
- **Отсутствие few-shot примеров**: нет ни одного образца диалога или демонстрации входа/выхода, что снижает предсказуемость поведения.
- **Слабая Chain-of-thought**: нет явного требования рассуждать пошагово, проверять гипотезы или фиксировать промежуточные выводы.
- **Формат вывода описан слишком обще**: «concise report» — без указания разметки, длины, структуры отчёта.
- **Нет обработки ошибок**: не описано, что делать, если инструменты не дали результата или поиск провалился.

## Что заимствовать
- Формулировка guardrails: **«NEVER create files unless they're absolutely necessary for achieving your goal. ALWAYS prefer editing an existing file to creating a new one.»** — универсальное правило для агентов, работающих с файловой системой.
- Стратегия поиска: **«search broadly when you don't know where something lives. Use `Read` when you know the specific file path»** — чёткое разделение стратегий в зависимости от уровня неопределённости.