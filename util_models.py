from dotenv import load_dotenv
import os

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI


load_dotenv()

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# ChatGPT Series
ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL")
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

QINIU_BASE_URL = os.getenv("QINIU_BASE_URL")
QINIU_API_KEY = os.getenv("QINIU_API_KEY")


# Configure model
model_instruct = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model="qwen3:4b-instruct-2507-q4_K_M-32k", 
    temperature=0.7,
    # num_ctx=32000,
)

model_thinking = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model="qwen3:4b-thinking-2507-q4_K_M", 
    temperature=0.7,
    num_ctx=32000,
)

model_mutimodal = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model="ministral-3:8b-instruct-2512-q4_K_M", 
    temperature=0.7,
    # num_ctx=32000,
)

model_universal = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model="qwen3:8b-q4_K_M", 
    temperature=0.7,
    num_ctx=32000,
)

model_online = ChatOpenAI(
    base_url=ZHIPU_BASE_URL,
    api_key=ZHIPU_API_KEY,
    model="glm-4.5-flash", 
    temperature=0.7,
)

model_embedding = OllamaEmbeddings(
    model="qwen3-embedding:0.6b-q8_0", 
    base_url=OLLAMA_BASE_URL
)