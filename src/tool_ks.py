from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()


@tool
def search(keyword: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b