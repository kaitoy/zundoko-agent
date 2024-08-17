from langchain_core.tools import tool
from langchain_groq import ChatGroq
from output_parsers.zundoko_parser import parse_zundoko

_llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
)
_chain = _llm | parse_zundoko

@tool
def zundoko() -> str:
    """ズンかドコを取得する。"""
    return _chain.invoke([
        ("system", "ズンかドコだけで回答してください。"),
        ("human", "ズンかドコのどちらかをランダムに返してください。"),
    ])
