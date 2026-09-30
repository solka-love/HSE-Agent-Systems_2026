from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List
from pathlib import Path
from data_preporation import extract_text
from openai import OpenAI
import json


PROMPT_RERANK = """Вопрос: {question}

Ниже пронумерованные фрагменты отчёта. Выбери ОДИН, который прямо содержит ответ.
Не выбирай фрагменты с общим описанием методики опроса и выходными данными, если в них нет ответа.
Верни JSON: {{"best": <номер>}}

{fragments}
"""



class RatingScore(BaseModel):
    relevance_score: float = Field(..., description="Очки релевантности документа и запроса")
    best: int = Field(..., ge=1, description="Номер выбранного лучшего фрагмента")

    @field_validator("best", mode="before")
    @classmethod
    def _to_int(cls, v):
        return int(v)

    def index(self, n_candidats: int) -> int:
        return self.best - 1 if 1 <= self.best <= n_candidats else 0

def _response_format() -> dict:
    """Создает json схему для формата возварта в llm
    """
    schema = RatingScore.model_json_schema()
    schema['additionalProperties'] = False
    schema['required'] = list(schema['properties'])

    return {"type" : "json_schema",
            "json_schema": {"name": "raiting_score", "strict": True, "schema": schema}}



def rerank_document(client: OpenAI, model: str, question: str, texts: list[str]) -> str:
    """Ранжирует документы по релевантности, обращаясь к llm
    Возвращает в готовом формате {{"relevansed_score" : "float", "best": "int"}}
    
    Args:
        client: Клиент OpenAI для общения
        model: Модель к которой обращаешся 
        question: Ключевой вопрос
        texts: Список релевантных текстов


    Returns:
        str: в формате {"relevansed_score" - "float", "best"- "int"}
    ----
    str
        Самый релевантный текст 
    """
    fragments = "\n\n".join(f"[{i+1}] {t}" for i, t in enumerate(texts))
    messages = [{"role": "user",
                 "content": PROMPT_RERANK.format(question=question, fragments=fragments)}]

    if client is None:
        client = OpenAI(base_url="http://127.0.0.1:8080", api_key="")
    

    for response_format in (_response_format(), {"type": "json_object"}):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
                response_format=response_format
            )
            return RatingScore.model_validate_json(response.choices[0].message.content)
        except (ValidationError, json.JSONDecodeError):
            continue
        except Exception:
            continue
    return RatingScore(best=1, relevance_score=0)
