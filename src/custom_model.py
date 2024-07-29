import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import json
import requests
from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
#from langchain.llms.base import LLM
from langchain_core.language_models.llms import LLM

class CustomLLM(LLM):
    llm_host = "http://10.10.50.2:1110"
    llm_url = f'{llm_host}/v3/completions' # or whatever your REST path is...

    @property
    def _llm_type(self) -> str:
        return "Llama2 70B"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        r = requests.post(self.llm_url, json.dumps({    
                "model": "WizardLM2-141B",
                "max_tokens": 4096,
                "temperature": 0.8,
                "top_p": 0.75,
                "frequency_penalty": 1.05,
                "seed": -1,
                "stream": False,
                "prompt": prompt,
                "completion": ""
        }))
        r.raise_for_status()

        return r.json()['choices'][0]['text'] # get the response from the API

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"llmUrl": self.llm_url}

#api_url = "http://10.10.50.2:1110/v3/complete"
custom_llm = CustomLLM()

category_prompt = PromptTemplate.from_template(
 'JSON 포맷으로 화장품을 사려는 고객의 요청을 듣고 알맞는 화장품 카테고리를 분류하세요. '
 '스킨케어, 메이크업, 헤어/바디 중 하나만 선택해. 다른 단어는 말하지마 '
 '<고객 요청>'
 '{user_input}'
 '</고객 요청>' 
 'category:'
)

output_parser = StrOutputParser()
category_chain = category_prompt | custom_llm |{"category": output_parser}

print(category_chain.invoke({'user_input': '얼굴이 넘 건조해 기초추천좀'}))
#{'category': '스킨케어'}
