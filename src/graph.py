from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END

from .fetch_evidence import get_evidence_by_topic
from .writer_node import write_article_paraphrase, write_article_quote


class WriterState(TypedDict):
    topic: str
    evidences: List[Dict]
    strategy: str
    article_markdown: str


def fetch_evidence_node(state: WriterState) -> WriterState:
    topic = state["topic"]
    state["evidences"] = get_evidence_by_topic(topic)
    return state


def decide_strategy_node(state: WriterState) -> WriterState:
    evidences = state["evidences"]
    if len(evidences) >= 3:
        state["strategy"] = "paraphrase"
    else:
        state["strategy"] = "quote"
    return state


def route_from_decide(state: WriterState) -> str:
    return state["strategy"]


def write_paraphrase_node(state: WriterState) -> WriterState:
    return write_article_paraphrase(state)


def write_quote_node(state: WriterState) -> WriterState:
    return write_article_quote(state)


def build_graph():
    graph = StateGraph(WriterState)

    graph.add_node("fetch_evidence", fetch_evidence_node)
    graph.add_node("decide_strategy", decide_strategy_node)
    graph.add_node("write_paraphrase", write_paraphrase_node)
    graph.add_node("write_quote", write_quote_node)

    graph.set_entry_point("fetch_evidence")

    graph.add_edge("fetch_evidence", "decide_strategy")

    graph.add_conditional_edges(
        "decide_strategy",
        route_from_decide,
        {
            "paraphrase": "write_paraphrase",
            "quote": "write_quote",
        },
    )

    graph.add_edge("write_paraphrase", END)
    graph.add_edge("write_quote", END)

    return graph.compile()
