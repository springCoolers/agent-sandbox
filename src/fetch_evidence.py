# src/fetch_evidence.py
from typing import List, Dict

import chromadb

from .embeddings import embed_text


DB_PATH = "chroma_db"
COLLECTION_NAME = "evidences"


# Chroma 클라이언트 / 컬렉션은 모듈 로드 시 한 번만 생성
_client = chromadb.PersistentClient(path=DB_PATH)
_collection = _client.get_or_create_collection(name=COLLECTION_NAME)


def get_evidence_by_topic(topic: str) -> List[Dict]:
    """
    주어진 topic 문자열을 임베딩 → 벡터 DB에서 유사도 검색 → Evidence 리스트 반환.
    """
    query_embedding = embed_text(topic)

    result = _collection.query(
        query_embeddings=[query_embedding],
        n_results=3,   # 가져오고 싶은 개수
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    ids = result.get("ids", [[]])[0]

    evidences: List[Dict] = []
    for doc, meta, _id in zip(documents, metadatas, ids):
        evidences.append(
            {
                "id": _id,
                "content": doc,
                "topic": meta.get("topic"),
                "source": "vector_db",
            }
        )

    print("🔎 [VectorDB] query:", topic)
    for e in evidences:
        print("  -", e["id"], "|", e["content"][:60], "...")

    return evidences
