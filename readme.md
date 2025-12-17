# 🧠 LangGraph 기반 Writer Agent (Vector DB 연동)

- **LLM**: Ollama + Llama 3.1 (로컬)
- **Embedding**: nomic-embed-text (로컬)
- **Vector DB**: ChromaDB (로컬 파일 기반)
- **Graph Orchestration**: LangGraph

---

## 1️⃣ 설치 & 실행 방법

### 1. 프로젝트 클론

```bash
git clone <YOUR_REPO_URL>
cd agent-sandbox-main
```

---

### 2. 가상환경 생성 및 활성화 (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

성공 시 터미널 앞에 `( .venv )` 표시가 나타납니다.

---

### 3. 의존성 설치

```powershell
pip install -r requirements.txt
```

주요 패키지:
- langgraph
- chromadb
- ollama

---

### 4. Ollama 설치 및 모델 다운로드

Ollama 설치: https://ollama.com/download  

설치 후 아래 명령 실행:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

---

### 5. 벡터 DB 생성 (초기 1회)

```powershell
python -m src.build_vector_db
```

정상 실행 시:

```text
✅ Vector DB built: X documents inserted.
```

프로젝트 루트에 `chroma_db/` 폴더가 생성됩니다.

---

### 6. Writer Agent 실행

```powershell
python -m src.main
```

실행 시 콘솔에 다음과 같이 **벡터 DB 검색 로그가 출력**됩니다:

```text
🔎 [VectorDB] query: RAG에서 청크 중복 제거가 중요한 이유
  - doc1 | ...
  - doc2 | ...
  - doc3 | ...
```

이는 Writer Agent가 **실제로 벡터 DB에서 Evidence를 조회**하고 있음을 의미합니다.

---

## 2️⃣ 프롬프트 수정 방법

프롬프트는 **역할 / 출력 구조 / 전략별 지시**로 분리되어 있으며,  
아래 파일들에서 수정할 수 있습니다.

---

### ① 에이전트 전체 톤 & 역할 설정

📄 파일 위치:

```text
src/prompts.py
```

```python
SYSTEM_PROMPT = """
너는 데이터 기반 브랜드 콘텐츠를 만드는 작가 에이전트(MELT)다.
주어진 토픽과 Evidence를 바탕으로,
브랜드 인사이트 리포트 같은 형식의 글을 작성한다.
"""
```

---

### ② 출력 포맷 (Markdown 구조)

같은 파일(`src/prompts.py`)의:

```python
USER_PROMPT_TEMPLATE = """
# {topic} 인사이트 리포트

## 1. Summary
## 2. 토픽 중심 정리
## 3. 시사점 및 활용 아이디어
"""
```

---

### ③ 전략별 프롬프트 (paraphrase / quote)

📄 파일 위치:

```text
src/writer_node.py
```

#### paraphrase 전략

```python
extra_instruction = (
    "직접 인용을 최소화하고, 내용을 통합·재서술하여 작성하라."
)
```

#### quote 전략

```python
extra_instruction = (
    "중요한 문장은 Markdown 인용 블록 형태로 그대로 인용하라."
)
```

Evidence 개수에 따라 **글 생성 스타일을 다르게 주고 싶을 때 수정**합니다.

---

## 📌 전체 처리 흐름

```text
토픽 입력
   ↓
Vector DB 검색 (Chroma + nomic-embed-text)
   ↓
전략 결정 (Evidence 개수 기반)
   ↓
paraphrase 또는 quote 전략
   ↓
Markdown 리포트 생성
```

LangGraph 조건부 그래프 구조:

```text
Start → decide_strategy → write_paraphrase / write_quote → End
```

---
