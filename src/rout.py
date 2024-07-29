from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List
load_dotenv()

'''
서브 체인간 라우팅 
RunnableLambda(권장) 조건부로 실행 파일을 반환합니다
'''
model = ChatOpenAI()
output_parser = StrOutputParser()

#서비스 분기를 결정하는 chain
service_prompt = PromptTemplate.from_template(
 '사용자 요청을 듣고 아래 기준에 따라 제공할 서비스를 선택하세요. '
 '제품추천, 배송조회, 자유대화 중 하나만 선택하세요'
 '제품추천 : 현재 피부고민에 맞는 제품을 추천하거나 특정 기능을 원하는 화장품을 추천해야할 경우'
 '배송조회 : 주문한 상품에 대해 도착 시간, 배송 상태 등 배송 정보를 원할 경우'
 '자유대화 : 화장품과 관련된 일반적인 주제 또는 트렌드 및 화장법, 주의성분 등에 대해 요청한 경우'
 '다른 단어는 말하지마세요 '
 '<고객 요청>'
 '{user_input}'
 '</고객 요청>' 
 'service:'
)

router_chain = service_prompt | model |output_parser


#서브체인 1) 화장품 카테고리 분류 runnable
category_prompt = PromptTemplate.from_template(
 'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 알맞는 화장품 카테고리를 분류하세요. '
 '스킨케어, 메이크업, 헤어/바디 중 하나만 선택해. 다른 단어는 말하지마 '
 '<고객 요청>'
 '{user_input}'
 '</고객 요청>' 
 'category:'
)

category_chain = category_prompt | model |{"category": output_parser}



#서브체인 2) 배송조회 함수, 함수를 runnable 객체로 만든다. 
def delivery_tracking(input=None):
    return "배송중"

delivery = RunnableLambda(delivery_tracking)


#서브 체인 3) : 디폴트 체인 자유대화 
prompt = PromptTemplate.from_template(
 '사용자 질문에 대해 답변하세요. '
  '<고객 요청>'
 '{user_input}'
 '</고객 요청>' 
)

conversation = prompt | model | output_parser



#사용자 정의 함수(라우팅 기준 검사)
def route(info):
    if "제품추천" in info["topic"].lower():
        return category_chain
    elif "배송조회" in info["topic"].lower():
        return delivery
    else:
        return conversation


full_chain = {"topic": router_chain, "user_input": lambda x: x["user_input"]} | RunnableLambda(route)
result = full_chain.invoke({"user_input": "퍼스널컬러가뭐야 "})
print(result)