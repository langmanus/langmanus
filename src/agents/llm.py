from langchain_openai import ChatOpenAI

from src.config import OPENAI_MODEL, OPENAI_BASE_URL

# Initialize LLM
llm = ChatOpenAI(model=OPENAI_MODEL, base_url=OPENAI_BASE_URL)
