from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()


# Define the OpenAI LLM model
model = OpenAI(model="gpt-4")



