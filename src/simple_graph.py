from typing import TypedDict, List
from langgraph.graph import StateGraph, END


# 1) 상태 정의
class SimpleState(TypedDict):
    decision: str       # "go_to_2" 또는 "go_to_3"
    log: List[str]      # 어떤 노드가 실행됐는지 기록


# 2) 노드 함수들
def node1(state: SimpleState) -> SimpleState:
    state["log"].append("Node 1 실행")

    # 여기서 어떤 조건에 따라 분기 결정
    # 지금은 예시로: log 길이가 짝수면 Node 2, 홀수면 Node 3
    if len(state["log"]) % 2 == 0:
        state["decision"] = "go_to_2"
    else:
        state["decision"] = "go_to_3"

    return state


def node2(state: SimpleState) -> SimpleState:
    state["log"].append("Node 2 실행")
    return state


def node3(state: SimpleState) -> SimpleState:
    state["log"].append("Node 3 실행")
    return state


# 3) 조건부 엣지가 참조할 라우팅 함수
def route_from_node1(state: SimpleState) -> str:
    """
    node1이 state["decision"]에 넣어둔 값을 읽어서
    어느 노드로 갈지 문자열로 반환.
    """
    return state["decision"]


# 4) 그래프 구성 함수
def build_simple_graph():
    graph = StateGraph(SimpleState)

    # 노드 등록
    graph.add_node("node1", node1)   # Node 1
    graph.add_node("node2", node2)   # Node 2
    graph.add_node("node3", node3)   # Node 3

    # 시작 지점: Start → node1
    graph.set_entry_point("node1")

    # node1 → (조건에 따라 node2 또는 node3)
    graph.add_conditional_edges(
        "node1",               # 출발 노드
        route_from_node1,      # state를 보고 분기 키를 결정하는 함수
        {
            "go_to_2": "node2",
            "go_to_3": "node3",
        },
    )

    # node2 / node3 둘 다 End로
    graph.add_edge("node2", END)
    graph.add_edge("node3", END)

    return graph.compile()


# 5) 직접 실행해 보는 코드
def main():
    app = build_simple_graph()

    # 초기 state 설정
    init_state: SimpleState = {
        "decision": "",
        "log": [],
    }

    result = app.invoke(init_state)

    print("=== Simple Graph 실행 결과 ===")
    for line in result["log"]:
        print(line)


if __name__ == "__main__":
    main()
