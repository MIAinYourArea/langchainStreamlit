import streamlit as st
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
st.title('🦜🔗 Quickstart App')

#openai_api_key = st.sidebar.text_input('')

def generate_response(input_text):
  load_dotenv()
  #llm = OpenAI(temperature=0.7, model_name='gpt-3.5-turbo')
  llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter :', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  generate_response(text)