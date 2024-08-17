from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from tools.zundoko import zundoko

tools = [zundoko]
tool_node = ToolNode(tools)

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

final_state = zundoko_agent.invoke({
    "messages": ["ズンかドコを5つ取得して"]
})

print(final_state["messages"][-1].content)
