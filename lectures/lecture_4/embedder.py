"""
Embedder: Переводит текст в вектор  

для чанков и запросов один и тот же эмбеддер, иначе неправильные пространства у векторов
"""


from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
# ENBEDDING_MODEL = "openai/text-embedding-3-large"
BATCH_SIZE = 64


class Embedder:
    def __init__(self, client: OpenAI, model: str = EMBEDDING_MODEL):
        self.client = client
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = [t.replace("\n", " ") for t in texts[i: i + BATCH_SIZE]]
            response = self.client.embeddings.create(model = self.model, input=batch)
            vectors.extend(item.embedding for item in response.data)
        return vectors

    def embed_query(self, query: str) -> list[float]:
        return self.embed([query])[0] 