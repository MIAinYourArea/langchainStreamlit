from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import json
import requests
load_dotenv()
import traceback
from langchain_core.runnables import chain
from copy import deepcopy


@tool
def search(query: str) -> str:
    """화장품을 사려는 고객에게 추천할 화장품의 특징, 기능, 성분들로 자연어 검색""" 
    engine_url = "http://10.10.50.2:5411/search?"
    vol =  "vol.tab"
    params = {
    'select': 'category,product,review',
    'from': vol,
    'where': f'review=\"{query}\" NATURAL',
    'default-hilite':'off',
    'limit': 10
    }
   # LLM이 만들어준 키워드로 검색됨
    print(f'query:::::::::::::::{query}')
    try :
        response = requests.get(engine_url, params = params)
        if response.status_code != 200:
            print(f"HTTP 응답 코드 에러: {response.status_code}")
            print(f"응답 내용: {response.text}")
            return f"HTTP 응답 코드 에러: {response.status_code}"
    except Exception as e:
        print(f"HTTP 요청 에러: {str(e)}")
        print(traceback.format_exc())

    try:
        res = response.json()
    except json.JSONDecodeError as e:
            print(f"JSON 디코딩 에러: {str(e)}")
            print(traceback.format_exc())
            return "JSON 디코딩 에러: 응답이 올바른 JSON 형식이 아닙니다."
    list = [{'category': row['fields']['category'], 'product':  row['fields']['product'], 'review':  row['fields']['review']} for row in res["result"]["rows"]]
    return json.dumps(list)

@tool
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱하기"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더하기"""
    return a + b

tools = [search, multiply, add]
model = ChatOpenAI()
llm_with_tools = model.bind_tools(tools)

# query = "얼굴이 너무 건조해 보습크림 찾아줘"
# messages = [HumanMessage(query)]
# ai_msg = llm_with_tools.invoke(messages)
# messages.append(ai_msg)

@chain
def tool_invoke(ai_msg):
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"add": add, "multiply": multiply, 'search':search }[tool_call["name"].lower()]
        #print(selected_tool)
        tool_msg = selected_tool.invoke(tool_call)
        #print(tool_msg)
        messages.append(tool_msg)
    return messages

# result = llm_with_tools.invoke(messages)
# print(result)


#체인으로 구현하면
query = "3더하기 3은 뭐야"
messages = [HumanMessage(query)]

chain = llm_with_tools | tool_invoke | llm_with_tools
print(chain.invoke(messages))