import json
import requests


def request_llm_qa(prompt):
    data = {
                "model": "WizardLM2-141B",
                "max_tokens": 4096,
                "temperature": 0.8,
                "top_p": 0.75,
                "frequency_penalty": 1.05,
                "seed": -1,
                "stream": False,
                "prompt": prompt,
                "completion": ""
    }
     
    json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    llm_url = "http://10.10.50.2:1110/v3/complete"
    response = requests.post(llm_url, data=json_data, headers=config.REQ_HEADERS)

    return response.json()

def category_prompt(user_input):
    prompt =  f'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 알맞는 화장품 카테고리를 분류하세요. \
                스킨케어, 메이크업, 헤어/바디 중 하나만 선택해. 다른 단어는 말하지마 \
                <고객 요청>\
                {user_input}\
                </고객 요청>\
                category:" "'
    return prompt

def keyword_prompt(user_input):
    prompt =  f'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 {category} 제품 중 추천할 화장품의 특징, 기능, 성분들의 키워드들을 추천하세요. \
                <고객 요청>\
                {user_input}\
                </고객 요청>\
                keyword:" "'
    return prompt

input = '얼굴 넘 건조해'

def prompt_chaining(input):
    c_prompt = category_prompt(input)
    c_llm_answer = request_llm_qa(c_prompt)
    category = llm_answer1["choices"][0]['text']

    k_prompt = keyword_prompt(category, input)
    K_llm_answer = request_llm_qa(k_prompt)
    keyword = llm_answer2["choices"][0]['text']
    return keyword

#비교
full_chain =  {"category": category_chain, "user_input": RunnablePassthrough()} | keyword_chain