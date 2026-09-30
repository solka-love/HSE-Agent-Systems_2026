"""Модуль оценки качества RAG-агента.

Retrieval-метрики (Precision@K, Recall@K, F1@K, MRR, MAP, NDCG@K):
    Стандартные IR-формулы на базе бинарного вектора релевантности.
    Релевантность определяется через token overlap (recall-oriented).

Generation-метрика (Faithfulness):
    Через библиотеку RAGAS (ragas.metrics.Faithfulness).
    Fallback: LLM-as-judge через OpenAI-совместимый клиент.

Использование::

    from evaluation import evaluate
    from agent import RAGAgentAnswer

    df_metrics = evaluate(
        answers=agent_answers,           # list[RAGAgentAnswer]
        dataset=df_test,                 # pd.DataFrame (id, question, ground_truth_chunks, document)
        client=openai_client,            # OpenAI client (для faithfulness)
        model="openai/gpt-4o",
    )
"""

from __future__ import annotations

import ast
import json
import logging
import math
import re
from typing import Any

import numpy as np
import pandas as pd
from agent import Chunk, RAGAgentAnswer
from tqdm.auto import tqdm

logger = logging.getLogger(__name__)

# ============================================================
# 1. Token Overlap Matching
# ============================================================


def _tokenize(text: str) -> set[str]:
    """Простая токенизация: lowercase + split по не-буквенным символам."""
    return set(re.findall(r"[\w]+", text.lower()))


def _token_overlap_recall(retrieved_text: str, ground_truth_text: str) -> float:
    """Доля токенов ground_truth, которые встречаются в retrieved_text."""
    gt_tokens = _tokenize(ground_truth_text)
    if not gt_tokens:
        return 0.0
    ret_tokens = _tokenize(retrieved_text)
    return len(gt_tokens & ret_tokens) / len(gt_tokens)


def _is_chunk_relevant(
    retrieved_text: str,
    ground_truth_chunks: list[str],
    threshold: float = 0.3,
) -> bool:
    """Проверяет, релевантен ли retrieved chunk хотя бы одному ground truth чанку."""
    return any(_token_overlap_recall(retrieved_text, gt) >= threshold for gt in ground_truth_chunks)


def _get_relevance_vector(
    retrieved_chunks: list[Chunk],
    ground_truth_chunks: list[str],
    threshold: float = 0.3,
    expected_year: int | None = None,
) -> list[int]:
    """Бинарный вектор релевантности: 1 если чанк релевантен, 0 иначе.

    Используется жадное one-to-one сопоставление: каждый ground-truth чанк
    может быть «использован» только одним retrieved чанком.  Это гарантирует,
    что recall, MAP, NDCG ≤ 1.
    """
    matched_gt: set[int] = set()  # индексы уже сопоставленных gt-чанков
    result = []
    for chunk in retrieved_chunks:
        if expected_year is not None and chunk.year != expected_year:
            result.append(0)
            continue
        found = False
        for gi, gt in enumerate(ground_truth_chunks):
            if gi in matched_gt:
                continue
            if _token_overlap_recall(chunk.text, gt) >= threshold:
                matched_gt.add(gi)
                found = True
                break
        result.append(int(found))
    return result


# ============================================================
# 2. Retrieval Metrics
# ============================================================


def _precision_at_k(relevance_vector: list[int], k: int | None = None) -> float:
    """Precision@K — доля релевантных среди top-K."""
    if not relevance_vector:
        return 0.0
    vec = relevance_vector[:k] if k else relevance_vector
    return sum(vec) / len(vec)


def _recall_at_k(
    relevance_vector: list[int],
    total_relevant: int,
    k: int | None = None,
) -> float:
    """Recall@K — доля найденных релевантных от общего числа релевантных."""
    if total_relevant == 0:
        return 0.0
    vec = relevance_vector[:k] if k else relevance_vector
    return sum(vec) / total_relevant


def _f1_at_k(
    relevance_vector: list[int],
    total_relevant: int,
    k: int | None = None,
) -> float:
    """F1@K — гармоническое среднее Precision@K и Recall@K."""
    p = _precision_at_k(relevance_vector, k)
    r = _recall_at_k(relevance_vector, total_relevant, k)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def _reciprocal_rank(relevance_vector: list[int]) -> float:
    """Reciprocal Rank — 1/позиция первого релевантного результата."""
    for i, rel in enumerate(relevance_vector):
        if rel == 1:
            return 1.0 / (i + 1)
    return 0.0


def _average_precision(relevance_vector: list[int], total_relevant: int) -> float:
    """Average Precision для одного запроса."""
    if total_relevant == 0:
        return 0.0
    cumsum = 0
    ap = 0.0
    for i, rel in enumerate(relevance_vector):
        cumsum += rel
        if rel == 1:
            ap += cumsum / (i + 1)
    return ap / total_relevant


def _dcg(relevance_vector: list[int], k: int | None = None) -> float:
    """Discounted Cumulative Gain."""
    vec = relevance_vector[:k] if k else relevance_vector
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(vec))


def _ndcg_at_k(
    relevance_vector: list[int],
    total_relevant: int,
    k: int | None = None,
) -> float:
    """NDCG@K — нормализованный DCG."""
    ideal_vector = [1] * total_relevant + [0] * max(0, len(relevance_vector) - total_relevant)
    ideal = _dcg(ideal_vector, k)
    if ideal == 0:
        return 0.0
    return _dcg(relevance_vector, k) / ideal


# ============================================================
# 3. Faithfulness
# ============================================================

_RAGAS_AVAILABLE: bool | None = None


def _check_ragas() -> bool:
    """Проверить доступность RAGAS."""
    global _RAGAS_AVAILABLE
    if _RAGAS_AVAILABLE is not None:
        return _RAGAS_AVAILABLE
    try:
        from langchain_openai import ChatOpenAI as _C  # noqa: F401
        from ragas.llms import LangchainLLMWrapper as _W  # noqa: F401
        from ragas.metrics import Faithfulness as _F  # noqa: F401

        _RAGAS_AVAILABLE = True
    except Exception:
        _RAGAS_AVAILABLE = False
    return _RAGAS_AVAILABLE


def _compute_faithfulness_ragas(
    questions: list[str],
    answers: list[str],
    contexts: list[list[str]],
    client: Any,
    model: str,
    max_concurrent: int = 4,
) -> list[float]:
    """Вычислить faithfulness через RAGAS (async concurrent)."""
    import asyncio

    try:
        import nest_asyncio

        nest_asyncio.apply()
    except ImportError:
        pass

    from langchain_openai import ChatOpenAI
    from ragas.dataset_schema import SingleTurnSample
    from ragas.llms import LangchainLLMWrapper
    from ragas.metrics import Faithfulness

    base_url = str(client.base_url).rstrip("/")
    api_key = client.api_key

    langchain_llm = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=0,
    )
    ragas_llm = LangchainLLMWrapper(langchain_llm)
    faithfulness_metric = Faithfulness(llm=ragas_llm)

    scores: list[float] = [np.nan] * len(questions)
    semaphore = asyncio.Semaphore(max_concurrent)
    pbar = tqdm(total=len(questions), desc="Faithfulness (RAGAS)")

    async def _score_one(i: int) -> None:
        async with semaphore:
            sample = SingleTurnSample(
                user_input=questions[i],
                response=answers[i],
                retrieved_contexts=contexts[i],
            )
            try:
                score = await faithfulness_metric.single_turn_ascore(sample)
                scores[i] = float(score) if not np.isnan(score) else 1.0
            except Exception as exc:
                logger.warning("RAGAS faithfulness failed for sample %d: %s", i, exc)
                scores[i] = np.nan
            finally:
                pbar.update(1)

    async def _run_all() -> None:
        await asyncio.gather(*[_score_one(i) for i in range(len(questions))])

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.run_until_complete(_run_all())
        else:
            asyncio.run(_run_all())
    except RuntimeError:
        asyncio.run(_run_all())
    finally:
        pbar.close()

    return scores


_FAITHFULNESS_PROMPT = """Ты — строгий эксперт по проверке фактов.

Тебе дан ОТВЕТ агента и КОНТЕКСТ (извлечённые фрагменты документов).

Задача:
1. Выдели из ОТВЕТА все отдельные фактические утверждения (claims).
2. Для каждого утверждения определи, подтверждается ли оно КОНТЕКСТОМ.
3. Верни JSON (и ничего больше) в формате:

{{
  "claims": [
    {{"claim": "текст утверждения", "supported": true/false}},
    ...
  ]
}}

Правила:
- supported=true ТОЛЬКО если утверждение прямо следует из КОНТЕКСТА
- Общие фразы без конкретных фактов — НЕ считаются утверждениями, пропускай их
- Если в ОТВЕТЕ нет фактических утверждений — верни пустой список claims

КОНТЕКСТ:
{context}

ОТВЕТ:
{answer}"""


def _compute_faithfulness_manual(
    answer: str,
    chunks: list[Chunk],
    client: Any,
    model: str,
) -> float:
    """Fallback: вычислить faithfulness через LLM-as-judge."""
    context = "\n\n---\n\n".join(c.text for c in chunks)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": _FAITHFULNESS_PROMPT.format(context=context, answer=answer),
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content or "{}"
    data = json.loads(raw)
    claims = data.get("claims", [])

    if not claims:
        return 1.0

    supported = sum(1 for c in claims if c.get("supported", False))
    return supported / len(claims)


# ============================================================
# 4. Вспомогательные функции
# ============================================================


def _parse_ground_truth_chunks(value: Any) -> list[str]:
    """Распарсить ground_truth_chunks из DataFrame (может быть строкой-списком)."""
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except (ValueError, SyntaxError):
            return [value]
    return []


def _zero_row(row_id: str, question: str) -> dict:
    """Строка с нулевыми метриками."""
    return {
        "id": row_id,
        "question": question,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
        "mrr": 0.0,
        "map": 0.0,
        "ndcg": 0.0,
        "faithfulness": 0.0,
    }


# ============================================================
# 5. Главная функция оценки
# ============================================================


def evaluate(
    answers: list[RAGAgentAnswer],
    dataset: pd.DataFrame,
    client: Any = None,
    model: str = "openai/gpt-4o",
    overlap_threshold: float = 0.3,
    compute_faithfulness: bool = True,
    gt_column: str = "relevant_text",
    max_workers: int = 4,
) -> pd.DataFrame:
    """Оценить качество RAG-агента.

    Parameters
    ----------
    answers:
        Список ответов агента (RAGAgentAnswer).
    dataset:
        DataFrame с колонками: ``id``, ``question``, ``<gt_column>``, ``document``.
    client:
        OpenAI-совместимый клиент (нужен для faithfulness).
    model:
        Модель для faithfulness-оценки.
    overlap_threshold:
        Порог token overlap для определения релевантности чанка (по умолчанию 0.3).
    compute_faithfulness:
        Считать ли faithfulness (требует LLM-вызовов).
    gt_column:
        Название колонки с ground truth чанками (по умолчанию ``relevant_text``).
    max_workers:
        Количество потоков для параллельного вычисления faithfulness.

    Returns
    -------
    pd.DataFrame
        Таблица с колонками: ``id``, ``question``, ``precision``, ``recall``,
        ``f1``, ``mrr``, ``map``, ``ndcg``, ``faithfulness``.
    """
    # Индекс: dataset_row_id -> RAGAgentAnswer
    answer_map: dict[str, RAGAgentAnswer] = {}
    for ans in answers:
        if ans.dataset_row_id is not None:
            answer_map[str(ans.dataset_row_id)] = ans

    rows: list[dict] = []

    # Для batch-вычисления faithfulness
    faith_indices: list[int] = []
    faith_questions: list[str] = []
    faith_answers: list[str] = []
    faith_contexts: list[list[str]] = []
    faith_chunks: list[list[Chunk]] = []

    for _, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Retrieval metrics"):
        row_id = str(row["id"])
        question = str(row["question"])
        gt_chunks = _parse_ground_truth_chunks(row[gt_column])
        expected_year = int(row["document"]) if "document" in row.index else None
        total_relevant = len(gt_chunks)

        ans = answer_map.get(row_id)

        # Нет ответа или нет чанков → нули
        if ans is None or not ans.retrieved_chunks:
            rows.append(_zero_row(row_id, question))
            continue

        # Вектор релевантности
        rel_vec = _get_relevance_vector(ans.retrieved_chunks, gt_chunks, overlap_threshold, expected_year)

        metrics_row = {
            "id": row_id,
            "question": question,
            "precision": _precision_at_k(rel_vec),
            "recall": _recall_at_k(rel_vec, total_relevant),
            "f1": _f1_at_k(rel_vec, total_relevant),
            "mrr": _reciprocal_rank(rel_vec),
            "map": _average_precision(rel_vec, total_relevant),
            "ndcg": _ndcg_at_k(rel_vec, total_relevant),
            "faithfulness": np.nan,
        }
        rows.append(metrics_row)

        # Собираем данные для faithfulness
        if compute_faithfulness and ans.retrieved_chunks:
            faith_indices.append(len(rows) - 1)
            faith_questions.append(question)
            faith_answers.append(ans.answer)
            faith_contexts.append([c.text for c in ans.retrieved_chunks])
            faith_chunks.append(ans.retrieved_chunks)

    # --- Faithfulness ---
    # if compute_faithfulness and faith_indices and client is not None:
    #     use_ragas = _check_ragas()

    #     if use_ragas:
    #         try:
    #             scores = _compute_faithfulness_ragas(
    #                 faith_questions, faith_answers, faith_contexts, client, model, max_workers
    #             )
    #             for idx, score in zip(faith_indices, scores):
    #                 rows[idx]["faithfulness"] = score if not np.isnan(score) else 0.0
    #         except Exception as exc:
    #             logger.warning("RAGAS faithfulness failed (%s), falling back to manual", exc)
    #             use_ragas = False

    #     if not use_ragas:
    #         from concurrent.futures import ThreadPoolExecutor, as_completed

    #         def _faith_task(i: int) -> tuple[int, float]:
    #             try:
    #                 score = _compute_faithfulness_manual(faith_answers[i], faith_chunks[i], client, model)
    #                 return faith_indices[i], score
    #             except Exception as exc:
    #                 logger.warning("Faithfulness failed for index %d: %s", faith_indices[i], exc)
    #                 return faith_indices[i], 0.0

    #         with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #             futures = [executor.submit(_faith_task, i) for i in range(len(faith_indices))]
    #             for future in tqdm(as_completed(futures), total=len(futures), desc="Faithfulness"):
    #                 idx, score = future.result()
    #                 rows[idx]["faithfulness"] = score

    # Заполняем NaN → 0.0
    df_result = pd.DataFrame(rows)
    df_result["faithfulness"] = df_result["faithfulness"].fillna(0.0)

    return df_result
