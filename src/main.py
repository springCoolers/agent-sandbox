from .graph import build_graph


def main():
    app = build_graph()

    topic = "RAG에서 청크 중복 제거가 중요한 이유"

    result = app.invoke({"topic": topic})

    print("=== 입력 토픽 ===")
    print(topic)
    print("\n=== 생성된 글 (Markdown) ===")
    print(result["article_markdown"])


if __name__ == "__main__":
    main()
