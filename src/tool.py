from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()

model = ChatOpenAI()
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

# Let's inspect some of the attributes associated with the tool.
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)


tools = [multiply, add]

#모델에 tool를 바인드
llm_with_tools = model.bind_tools(tools)


query = "What is 3 * 12? Also, what is 11 + 49?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

#위에까지는 모델이 툴을 선택까지만하는것. 쿼리와 모델 선택결과를 대화기록에 아래와 같이 가지고있고 이 기록을 기반으로 원래 질문에 대답을 생성
# [HumanMessage(content='What is 3 * 12? Also, what is 11 + 49?'),
#  AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_loT2pliJwJe3p7nkgXYF48A1', 'function': {'arguments': '{"a": 3, "b": 12}', 'name': 'multiply'}, 'type': 'function'}, {'id': 'call_bG9tYZCXOeYDZf3W46TceoV4', 'function': {'arguments': '{"a": 11, "b": 49}', 'name': 'add'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 87, 'total_tokens': 137}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_661538dc1f', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-e3db3c46-bf9e-478e-abc1-dc9a264f4afe-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_loT2pliJwJe3p7nkgXYF48A1', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_bG9tYZCXOeYDZf3W46TceoV4', 'type': 'tool_call'}], usage_metadata={'input_tokens': 87, 'output_tokens': 50, 'total_tokens': 137}),
#  ToolMessage(content='36', name='multiply', tool_call_id='call_loT2pliJwJe3p7nkgXYF48A1'),
#  ToolMessage(content='60', name='add', tool_call_id='call_bG9tYZCXOeYDZf3W46TceoV4')]
result = llm_with_tools.invoke(messages)
print(result)
