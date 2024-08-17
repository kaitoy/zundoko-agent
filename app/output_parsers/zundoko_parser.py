from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage


def parse_zundoko(ai_message: AIMessage) -> str:
    content = ai_message.content
    if isinstance(content, str):
        if content.find("ズン") >= 0:
            print("ズン")
            return "ズン"
        if content.find("ドコ") >= 0:
            print("ドコ")
            return "ドコ"
        raise OutputParserException(f"Can't parse AIMessage with non-zundoko content: {ai_message}")
    else:
        raise OutputParserException(f"Can't parse AIMessage with content the type of which is not str: {ai_message}")
