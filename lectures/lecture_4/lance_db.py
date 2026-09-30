"""
Тут описываете методы\функции для работы с БД. Заливка данных, чтение (Полный CRUD при необходимости)
Не забудьте сделать метод\функцию read_all это для проверки
"""

from pathlib import Path

import lancedb
import pandas as pd
from typing import List, Tuple, Dict, Optional


VECTORESTORE_DIR = Path(__file__).parent / "lance_db" / "vectorestore"
TABLE_NAME = "chunks"

def get_table():
    return lancedb.connect(str(VECTORESTORE_DIR)).open_table(str(TABLE_NAME))


def write_records(records: list[dict], vectors: list[list[float]]):
    rows = [{**r, "vector": v} for r, v in zip(records, vectors)]
    db = lancedb.connect(str(VECTORESTORE_DIR))
    return db.create_table(TABLE_NAME, data=rows, mode="overwrite")


def read_all():
    table = get_table()
    return table.search().limit(table.count_rows()).to_pandas().drop(columns=["vector"])


def search(vectore: list[float], top_k: int = 3, metric_search: str = "cosine", year: int | None = None) -> list[dict]:
    table = get_table()
    query = table.search(vectore).metric(metric_search)
    if year is not None:
        query = query.where(f"year = {int(year)}", prefilter=True)
    return query.limit(top_k).to_list()



# def get_by_ids(year: int, chunk_ids: list[int]) -> list[dict]:

#     ids = ", ".join(str(int(i)) for i in chunk_ids)
#     rows = (
#         get_table().search().where(f"year = {int(year)}").limit(len(chunk_ids)).to_list()
#     )
#     return sorted(rows, key=lambda r: r["chunk_id"])


def get_by_ids(year: int, chunk_ids: list[int]) -> list[dict]:
    """Чанки с указанными chunk_id внутри одного года, по порядку."""
    ids = ", ".join(str(int(i)) for i in chunk_ids)
    rows = (
        get_table().search()
        .where(f"year = {int(year)} AND chunk_id IN ({ids})")
        .limit(len(chunk_ids))
        .to_list()
    )
    return sorted(rows, key=lambda r: r["chunk_id"])