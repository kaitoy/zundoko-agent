from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from tools.zundoko import zundoko

tools = [zundoko]
tool_node = ToolNode(tools).with_config({"max_concurrency": 1})

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
agent_node = RunnableLambda(
    lambda state: {"messages": [llm.invoke(state["messages"])]}
)

graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    lambda state: "tools" if state["messages"][-1].tool_calls else END,
)
graph.add_edge("tools", "agent")

zundoko_agent = graph.compile()

msg = """
以下を実行してください。

1. ズンかドコを一つだけ取得する。
2. 直近で取得した5つのズンとドコを、取得した順に並べる
3. その結果を確認し、はじめに4つのズンが連続し、最後がドコになっていたら「キ・ヨ・シ！」を出力した後終了する。そうでなければ最初の手順に戻る。
"""
final_state = zundoko_agent.invoke({"messages": msg}, {"recursion_limit": 30})

print(final_state["messages"][-1].content)
