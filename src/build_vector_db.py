# src/build_vector_db.py
from typing import List, Dict
import chromadb

from .embeddings import embed_texts


DB_PATH = "chroma_db"          # ./chroma_db 폴더에 데이터 저장
COLLECTION_NAME = "evidences"  # 컬렉션 이름


def get_source_documents() -> List[Dict]:
    """
    실제로는 여기에서 DB나 파일에서 문서를 가져오면 됨.
    지금은 테스트용 더미 데이터를 넣어둘게.
    """
    docs = [
        {
            "id": "doc1",
            "topic": "RAG에서 청크 중복 제거",
            "content": "RAG 파이프라인에서 청크 중복 제거는 검색 품질과 토큰 비용을 최적화하는 핵심 단계이다.",
        },
        {
            "id": "doc2",
            "topic": "RAG에서 청크 중복 제거",
            "content": "🚨 이것은 벡터디비 연결 테스트 문장입니다. 이 문장이 결과 리포트에 보이면 Chroma 벡터 DB가 제대로 연결된 것입니다.",
        },
        {
            "id": "doc3",
            "topic": "RAG에서 청크 중복 제거",
            "content": "중복 제거를 하면 LLM 입력 토큰 수를 줄여 비용을 절감하고, 요약과 생성 품질을 높일 수 있다.",
        },
        {
            "id": "doc4",
            "topic": "RAG 파이프라인 설계",
            "content": "RAG 파이프라인은 인덱싱, 검색, 후처리 세 단계로 구성되며 각 단계가 응답 품질에 영향을 준다.",
        },
    ]
    return docs


def build_vector_db():
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # 기존 데이터 있으면 싹 비우고 새로 구축
    try:
        existing = collection.count()
        if existing > 0:
            collection.delete(where={})
    except Exception:
        pass

    docs = get_source_documents()
    texts = [d["content"] for d in docs]
    ids = [d["id"] for d in docs]
    metadatas = [{"topic": d["topic"]} for d in docs]

    embeddings = embed_texts(texts)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"✅ Vector DB built: {len(docs)} documents inserted.")


if __name__ == "__main__":
    build_vector_db()
