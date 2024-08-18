from langchain_core.tools import tool
from langchain_groq import ChatGroq
from output_parsers.zundoko_parser import parse_zundoko

_llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=1,
)
_chain = _llm | parse_zundoko

zundoko_history = []

@tool
def zundoko() -> str:
    """ズンかドコを取得する。"""
    response = _chain.invoke([
        ("system", "ズンかドコだけで回答してください。"),
        ("human", "ズンかドコのどちらかをランダムに返してください。以前の結果をもとに、ややズン多めでお願いします。"),
        ("human", f"以前の結果: {zundoko_history}"),
    ])
    zundoko_history.append(response)
    return response
