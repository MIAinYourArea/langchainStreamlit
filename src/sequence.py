from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
load_dotenv()

'''
langChain Expression Language (LCEL)문법으로 체인 구성
체인 기본 구성 : 일자식 구성(순차적 구성)
프롬프트 + 모델 + 출력 파서
'''
model = ChatOpenAI()

#제품의 카테고리를 분류요청 
category_prompt = PromptTemplate.from_template(
 'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 알맞는 화장품 카테고리를 분류하세요. '
 '스킨케어, 메이크업, 헤어/바디 중 하나만 선택해. 다른 단어는 말하지마 '
 '<고객 요청>'
 '{user_input}'
 '</고객 요청>' 
 'category:'
)

output_parser = StrOutputParser()
category_chain = category_prompt | model |{"category": output_parser}

#print(category_chain.invoke({'user_input': '얼굴이 넘 건조해 기초추천좀'}))
#{'category': '스킨케어'}

##
keyword_prompt = PromptTemplate.from_template(
 'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 {category} 제품 중 추천할 화장품의 특징, 기능, 성분들의 키워드들을 추천하세요.'
 '쉼표(,)로 키워드들을 구분해줘 '
 '<고객 요청>'
 '{user_input}'
 '</고객 요청>'
 'keyword:'
)

keyword_chain = keyword_prompt | model | {"keyword": output_parser}
#print(keyword_chain.invoke({'category': '스킨케어', 'user_input': '얼굴이 넘 건조해 기초추천좀'}))
#{'keyword': '수분공급, 보습, 촉촉함, 피부재생, 히알루론산, 세라마이드, 글리세린, 알로에베라, 판테놀'}

full_chain =  {"category": category_chain, "user_input": RunnablePassthrough()} | keyword_chain
print(full_chain.invoke('얼굴 건조해 기초 추천좀'))




#더 단순한 예제 
#제품의 카테고리와 사용자 요청 내용을 정리 요청 req 라는 값으로 응답내용을 받는다.
# first_prompt = PromptTemplate.from_template(
#  '화장품을 사려는 고객 요청을 듣고 사용자의 요청 내용과 추천 화장품 카테고리를 정리하세요.'
#  '카테고리는 스킨케어, 메이크업, 헤어/바디 중 한개만 선택하세요 '
#  '<고객 요청>'
#  '{user_input}'
#  '</고객 요청>' 
# )

# output_parser = StrOutputParser()


# seconde_prompt = PromptTemplate.from_template(
#  'JSON 포맷으로 화장품을 사려는 고객의 요청과 화장품 카테고리를 듣고 추천할 화장품의 특징, 기능, 성분들의 키워드들을 추천하세요.'
#  '쉼표(,)로 키워드들을 구분해줘 '
#  '<고객 요청>'
#  '{req}'
#  '</고객 요청>'
#  'keyword:'
# )

# first_chain = category_prompt | model |{"req": output_parser}
# chain = (
#     {"req": first_chain}
#     | seconde_prompt
#     | model
#     | output_parser
# )

# print(chain.invoke({"user_input":'얼굴이 건조해 기초추천좀'}))