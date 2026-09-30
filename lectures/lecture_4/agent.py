"""
Тут описываете своего RAG агента или RAG пайплайн (как хотите, без разницы)
Главное чтобы на каждый запрос Ваш RAG агент \ пайплайн возвращал объект
RAGAgentAnswer 
Это контракт который ожидает модуль evaluation для оценки 
"""

from pydantic import BaseModel

class Chunk(BaseModel):
    """Один найденный фрагмент из векторного хранилища."""

    text: str
    chunk_id: int
    year: int
    distance: float


class RAGAgentAnswer(BaseModel):
    """
    Контракт ответа RAG-агента для системы оценки.

    Это единый формат, который позволяет считать все метрики:
    - Retrieval-метрики (Precision@K, Recall@K, MRR, MAP, NDCG) — по retrieved_chunks
    - Generation-метрики (Faithfulness) — по answer + retrieved_chunks
    """

    dataset_row_id: str | None = None
    answer: str
    retrieved_chunks: list[Chunk] | None = None

PROMPT = """
Ответь на вопрос, используя ТОЛЬКО контекст ниже. Кратко, 1-3 предложения.
Цифры и формулировки бери из контекста. Если ответа в контексте нет — так и скажи.

КОНТЕКСТ:
{context}

ВОПРОС: {question}
"""


class RAGAgent:
    def __init__(self, client, model: str, retriver):
        self.client = client
        self.model = model
        self.retriver = retriver

    def run(self, question: str, temperature: float = 0, verbose: bool = False, dataset_row_id: str | None = None) -> RAGAgentAnswer:
        """
        """
        chunks = self.retriver.retrive(question)
        context = "\n---\n".join(chunk.text for chunk in chunks)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": PROMPT.format(question=question, context=context)}
            ],
            temperature=temperature
        )
        answer = response.choices[0].message.content

        if verbose:
            print(f"Найдено чанков: {len(chunks)}, Символов контекста: {len(context)}") 
            print(f"Ответ: {answer}")

        return RAGAgentAnswer(dataset_row_id=dataset_row_id, answer=answer, retrieved_chunks=chunks)