"""
Тут описываете флоу подготовки данных перед заливкой в БД (очистка + чанкикнг).
Так же сюда можете закинуть код по извлечению текста из pdf (docling и тп)
"""

import re
from pathlib import Path
from chunking import semantic_chunking
# from docling.Document_converter import DocumentConverter
from docling.document_converter import DocumentConverter


DATASET_DIR = Path(__file__).parent / "dataset"

DOCUMENTS = {
    2019: DATASET_DIR / "Potrebitelskie_ozhidaniya_2_2019.pdf",
    2025: DATASET_DIR / "Consumer_sentiment_2Q2025.pdf",
}


def fix_text(text: str) -> str:
    def fix(match):
        try:
            return match.group(0).encode("latin1").decode("cp1251")
        except UnicodeError:
            return match.group(0)
        
    return re.sub(r"[À-ÿ][À-ÿ\s,.:;()\d-]*", fix, text)


def extract_text(pdf_path: Path, converter: DocumentConverter) -> str:
    """ PDF to markdown"""
    result = converter.convert(str(pdf_path))
    return result.document.export_to_markdown()


def clean_text(text: str) -> str:
    """Убрать артефакты извлечения, не трогая смысл."""
    text = fix_text(text)
    text = re.sub(r"-\n(?=[а-яёa-z])", "", text)        # переносы слов: "потреби-\nтельской"
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # служебные комментарии docling (картинки)
    text = re.sub(r"[ \t]+", " ", text)                 # множественные пробелы
    text = re.sub(r"\n{3,}", "\n\n", text)              # множественные пустые строки
    return text.strip()


def prepare_documents(chunk_size: int = 1000, chunk_overlap: int = 200) -> list[dict]:
    """Полный флоу подготовки: на выходе список словарей, готовых к эмбеддингу."""
    converter = DocumentConverter()
    records: list[dict] = []
    for year, path in DOCUMENTS.items():
        text = clean_text(extract_text(pdf_path=path, converter=converter))
        docs = semantic_chunking(
            text=text, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            metadata={"year": year, "source": path.name}
        )

        for d in docs:
            records.append({
                "text": d.page_content,
                "chunk_id": len(records),
                "year": d.metadata["year"],
                "section": d.metadata.get("section", ""),
                "source": d.metadata["source"]

            })
    return records



if __name__ == "__main__":

    """
    Запуск предобработки данных и занесения их в lance_db
    """
    from dotenv import load_dotenv
    from openai import OpenAI
    import os

    from embedder import Embedder
    from lance_db import read_all, write_records

    load_dotenv()
    client = OpenAI(base_url="https://polza.ai/api/v1", api_key=os.getenv("POLZA_AI_API_KEY"))

    records = prepare_documents(chunk_size=500, chunk_overlap=100)
    lengths = [len(r["text"]) for r in records]
    print(f"Чанков: {len(records)}, длина: min {min(lengths)}, max {max(lengths)}")

    vectors = Embedder(client).embed([r["text"] for r in records])
    write_records(records, vectors)
    print(read_all().head())
