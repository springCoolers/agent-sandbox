from typing import Dict
import ollama

from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

MODEL_NAME = "llama3.1"  # ollama pull llama3.1


def _call_llm(topic: str, evidences_text: str, extra_instruction: str) -> str:
    system_prompt = SYSTEM_PROMPT + "\n\n" + extra_instruction

    user_prompt = USER_PROMPT_TEMPLATE.format(
        topic=topic,
        evidences=evidences_text,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
    )
    return response["message"]["content"]


def write_article_paraphrase(state: Dict) -> Dict:
    topic = state["topic"]
    evidences = state["evidences"]

    evidence_text = "\n".join(
        f"- ({e.get('source', 'unknown')}) {e['content']}" for e in evidences
    )

    extra_instruction = (
        "가능한 한 직접 인용은 줄이고, 내용을 통합·요약해서 재작성하라. "
        "중복되는 설명은 하나로 합치고, 구조를 깔끔하게 정리하라."
    )

    article = _call_llm(topic, evidence_text, extra_instruction)
    state["article_markdown"] = article
    return state


def write_article_quote(state: Dict) -> Dict:
    topic = state["topic"]
    evidences = state["evidences"]

    evidence_text = "\n".join(
        f"- ({e.get('source', 'unknown')}) {e['content']}" for e in evidences
    )

    extra_instruction = (
        "Evidence가 많지 않으므로, 중요한 문장은 인용 형태로 그대로 보여줘도 좋다. "
        '단, 인용은 Markdown 블록 인용("> ...") 형태로 표시하라.'
    )

    article = _call_llm(topic, evidence_text, extra_instruction)
    state["article_markdown"] = article
    return state
