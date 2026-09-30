"""
Тут описываете retrieve данных 
embedder -> read_from_db 
Здесь будет сконцентрирован весь основной тюнинг системы 
(реранкеры, перефразировщики, классификация и тд и тп)
"""


from agent import Chunk
from lance_db import search, get_by_ids
import json
from embedder import Embedder
# from data_preporation import get
import re

from reranking import rerank_document

MAX_CONTEXT_SIZE = 6000


EXTRACT_PROMPT = """Из вопроса извлеки год отчёта. Доступные года: 2019, 2025.
Верни Json формата: {{"year": 2019}} или {{"year": 2025}}, или {{"year": null}} если год не указан
Вопрос: {question}
"""

N_CANDIDATE = 5

WINDOW = 1

def extract_year_llm(client, model: str, question: str) -> int | None:
    """Извлечение года из вопроса с помощью запроса к llm, для более узкого поиска"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": EXTRACT_PROMPT.format(question=question)}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    year = json.loads(response.choices[0].message.content).get("year")
    return year



def extract_year_local(question: str) -> int | None:
    """Извлечение года из вопроса с помощью регулярки, для сокращения обращений к llm"""
    match = re.search(r"20\d{2}", question or "")
    return int(match.group(1)) if match else None



class Retriever:
    def __init__(self, client, model: str, top_k: int = 3, use_rerank: bool = True):
        self.client = client
        self.model = model
        self.embedder = Embedder(client)
        self.top_k = top_k
        self.use_rerank = use_rerank


    def expand(self, row: dict) -> str:
        """Добавляет окно, которое захватывает n соседей
        Найденный чанк + соседи +- окно (совмещает в один текст)"""
        cid = row["chunk_id"]
        neighbours = get_by_ids(row["year"], list(range(cid - WINDOW, cid + WINDOW + 1)))
        return "\n".join(r["text"] for r in neighbours)

    def retrive(self, question: str) -> list[Chunk]:
        """Возвращает готовый чанк
        """
        year = extract_year_llm(self.client, self.model, question)
        query_vectore = self.embedder.embed_query(question)
        rows = search(query_vectore, N_CANDIDATE if self.use_rerank else self.top_k, year=year)

        texts = [self.expand(row) for row in rows]     

        if self.use_rerank and len(rows) > 1:
            choice = rerank_document(self.client, self.model, question, texts)
            i = choice.index(len(rows))
            rows = [rows[i]] + [r for j, r in enumerate(rows) if j != i]
            texts = [texts[i]] + [t for j, t in enumerate(texts) if j != i]



        chunks: list[Chunk] = []
        total = 0

        for row, text in zip(rows[: self.top_k], texts[: self.top_k]):
            if total + len(text) > MAX_CONTEXT_SIZE:
                break
            total += len(text)
            chunks.append(Chunk(
                text=text,
                chunk_id=row["chunk_id"],
                year=row["year"],
                distance=row["_distance"],
            ))

        return chunks