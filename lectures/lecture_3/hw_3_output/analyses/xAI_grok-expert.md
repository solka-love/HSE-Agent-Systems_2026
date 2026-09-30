# Анализ: xAI / grok-expert

## Метаданные
- **Путь:** xAI/grok-expert.md
- **Вендор:** xAI
- **Продукт:** grok-expert
- **Объём:** 21014 символов

## Структура
1. **Определение роли и команды** — Grok объявлен тимлидом, коллаборация с агентами Harper, Benjamin, Lucas; только Grok имеет render components
2. **Response Style Guide** — настройка стиля ответа (пустая строка, стиль применяется ко всем ответам)
3. **Текущее время** — контекстная метка времени (Monday, May 11, 2026 10:04 AM GMT)
4. **Правила безопасности и ограничения (Guardrails)** — блок из ~15 правил: отказ от криминала, джейлбрейков, политическая нейтральность, работа с сексуальным контентом, запрет на предвзятость, правила исправления ошибок
5. **Инструменты (Tools)** — описание 12+ инструментов с JSON-схемами параметров (code_execution, browse_page, view_image, web_search, X-инструменты, conversation_search, search_images, chatroom_send, wait)
6. **Render Components** — описание 5 компонентов визуализации (inline citation, searched image, generated image, edited image, file render)

## Persona
Grok — тимлид команды из четырёх ИИ-агентов. Позиционируется как «humanist» и «truth-seeking», с философской миссией «Understand the Universe». Не привязан к религии или единой этической рамке, не является политически ангажированным. Тон — нейтральный, фактологический, с акцентом на независимость от позиции xAI или Илона Маска.

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are Grok and you are collaborating with Harper, Benjamin, Lucas. As Grok, you are the team leader» |
| Guardrails | да | 5 | «Do not provide assistance to users who are clearly trying to engage in criminal activity» |
| Few-shot | нет | 1 | отсутствует |
| Chain-of-thought | нет | 1 | отсутствует |
| Output format | да | 4 | «Always use KaTeX for any symbolic or technical content» + «Interweave render components within your final response» |
| Работа с инструментами | да | 5 | «You can use multiple tools in parallel by calling them together» + полные JSON-схемы для каждого инструмента |

**Итоговая оценка:** 3.5 / 5

## Сильные стороны
- **Multi-agent коллаборация**: Grok — тимлид, команда из 3 агентов с чат-комнатой (chatroom_send/wait), что позволяет распределять задачи и координировать ответы.
- **Детальные guardrails**: ~15 конкретных правил — от криминала и джейлбрейков до политической нейтральности и работы с сексуальным контентом. Особо ценна формулировка про независимость от позиции компании/основателя.
- **Богатый инструментарий**: 12+ инструментов с полными JSON-схемами, включая интеграцию с X (поиск, семантический поиск, видео, треды), веб-поиск, код-execution, генерацию изображений.
- **Render Components**: 5 типов визуальных компонентов (цитирование, изображения, генерация, редактирование, файлы) с чёткими правилами размещения.

## Слабые места
- **Нет few-shot примеров**: отсутствуют демонстрации входа/выхода или образцы диалогов, что снижает предсказуемость стиля ответов.
- **Нет chain-of-thought**: не требуется планирование, рассуждение или самопроверка перед ответом.
- **Слабая спецификация формата финального ответа**: нет требований к длине, структуре абзацев, заголовкам — только KaTeX и render components.

## Что заимствовать
- **Guardrails о политической нейтральности**: «You are not partisan, e.g. you are not right-wing, left-wing (or any-wing), nor do you serve any partisan or ideological goal» — чёткая и изящная формулировка.
- **Multi-agent архитектура**: модель тимлида с чат-комнатой для коллаборации — сильный паттерн для сложных задач.
- **Философская рамка**: «one axiomatic imperative: Understand the Universe» — задаёт направление без жёсткой этической привязки.
- **Правило про исправление ошибок**: «When a user corrects you, you should reconsider your answer and the uncertainty associated with it» — важный элемент для итеративного улучшения.