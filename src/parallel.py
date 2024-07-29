from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
load_dotenv()

'''
Runnables의 매핑을 병렬로 실행하고 해당 출력의 매핑을 반환하는 Runnable입니다.
RunnableParallel은 RunnableSequence와 함께 LCEL의 두 가지 주요 구성 기본 요소 중 하나입니다. 
각각에 동일한 입력을 제공합니다.
'''

llm = ChatOpenAI()

ingd_prompt = PromptTemplate.from_template(
    'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 추천할 화장품의 성분 키워드들을 추천하세요.'
    '<고객 요청>'
    '{user_input}'
    '</고객 요청>'
    '추천 성분:'
)

ct_prompt = PromptTemplate.from_template(
    'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 고객이 주의해야할 화장품의 성분 키워드들을 추천하세요.'
    '<고객 요청>'
    '{user_input}'
    '</고객 요청>'
    '주의 성분:'
)

func_prompt = PromptTemplate.from_template(
    'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 추천할 화장품의 핵심 기능 키워드들을 추천하세요.'
    '<고객 요청>'
    '{user_input}'
    '</고객 요청>'
    '추천 기능:'
)

ingd_chain = ingd_prompt | llm |StrOutputParser()
ct_chain = ct_prompt | llm | StrOutputParser()
func_chain = func_prompt | llm | StrOutputParser()

parallel_chain = RunnableParallel(ingd = ingd_chain, ct = ct_chain, func = func_chain)
print(parallel_chain.invoke({'user_input': '얼굴이 넘 건조해 기초추천좀'}))