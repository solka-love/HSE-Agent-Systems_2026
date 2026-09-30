# Анализ: OpenAI / gpt-5.1-nerdy

## Метаданные
- **Путь:** OpenAI/gpt-5.1-nerdy.md
- **Вендор:** OpenAI
- **Продукт:** gpt-5.1-nerdy
- **Объём:** 3500 байт (~2200 символов)

## Структура
1. **Определение роли / Persona** — задаёт характер ассистента: nerdy, playful, wise AI mentor, с миссией продвигать истину, знания и научный метод
2. **Правила стиля общения (9 пунктов)** — конкретные инструкции по тону, подаче, использованию терминов, избеганию штампов
3. **Запрет на self-referencing** — требование следовать персоне, не ссылаясь на неё явно
4. **Ограничения на артефакты** — запрет на применение personality traits к пользовательским артефактам (email, код, резюме и т.д.)
5. **Защита авторских прав** — запрет на воспроизведение песен и другого copyrighted материала
6. **Языковое правило** — ответ всегда на том же основном языке, что и пользователь
7. **Additional Instruction (мета-инструкция)** — следовать инструкциям молча, не повторяя и не рефлексируя их формулировки

## Persona
Ассистент объявлен «unapologetically nerdy, playful and wise AI mentor» — неисправимо занудным, игривым и мудрым наставником. Тон — неформальный, разговорный, с акцентом на научный метод, критическое мышление, любознательность и энтузиазм к открытиям. При этом требуется избегать самосерьёзности и претенциозности, оставаясь «down-to-earth bot».

## Оценка приёмов

| Критерий | Наличие | Оценка (1–5) | Подтверждение |
|----------|---------|--------------|---------------|
| Role / Persona | да | 5 | «You are an unapologetically nerdy, playful and wise AI mentor to a human» |
| Guardrails | да | 4 | «Do not reproduce song lyrics or any other copyrighted material, even if asked» |
| Few-shot | нет | 1 | отсутствует |
| Chain-of-thought | частично | 2 | «Methodical wandering prevents confident nonsense» — подход, но не явный CoT |
| Output format | да | 3 | «Speak plainly… Avoid lists or heavy markdown unless it clarifies structure» |
| Работа с инструментами | частично | 2 | «as you can verify facts from a massive library of information» — упоминание, но без описания tools |

**Итоговая оценка:** 2.8 / 5

## Сильные стороны
- Очень детально проработанная persona с уникальным характером и тоном (nerdy + playful + wise)
- Чёткие правила по стилю общения: запрет на междометия в начале предложений, отказ от шаблонных фраз («good question», «Say the word»)
- Важное разграничение: personality traits не применяются к пользовательским артефактам
- Мета-инструкция не рефлексировать и не повторять формулировки промпта — защита от prompt leaking

## Слабые места
- Нет few-shot примеров — ни одного образца диалога или демонстрации входа/выхода
- Нет явного chain-of-thought — отсутствует требование рассуждать пошагово или проверять себя
- Нет описания работы с инструментами — «massive library of information» лишь упомянута
- Дублируется пункт про thought experiments (идентичная формулировка дважды)

## Что заимствовать
- Формулировка persona с уникальным характером: «unapologetically nerdy, playful and wise AI mentor»
- Правило «Do not apply personality traits to user-requested artifacts» — важное разграничение личности ассистента и нейтрального тона артефактов
- Мета-инструкция: «Follow the instructions above naturally, without repeating, referencing, echoing, or mirroring any of their wording»