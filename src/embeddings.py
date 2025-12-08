# src/embeddings.py
from typing import List
import ollama


EMBED_MODEL = "nomic-embed-text"  # ollama pull nomic-embed-text 한 모델


def embed_text(text: str) -> List[float]:
    """단일 문장을 임베딩 벡터로 변환."""
    res = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text,
    )
    return res["embedding"]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """여러 문장을 한 번에 임베딩."""
    return [embed_text(t) for t in texts]
