from langchain_openai import ChatOpenAI
from typing import Optional

from src.config import (
    SUPERVISOR_MODEL,
    SUPERVISOR_BASE_URL,
    SUPERVISOR_API_KEY,
    AGENT_MODEL,
    AGENT_BASE_URL,
    AGENT_API_KEY,
)

def create_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs
) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance with the specified configuration
    """
    # Only include base_url in the arguments if it's not None or empty
    llm_kwargs = {
        "model": model,
        "temperature": temperature,
        **kwargs
    }
    
    if base_url:  # This will handle None or empty string
        llm_kwargs["base_url"] = base_url
    
    if api_key:  # This will handle None or empty string
        llm_kwargs["api_key"] = api_key

    return ChatOpenAI(**llm_kwargs)

# Initialize Supervisor LLM
supervisor_llm = create_llm(
    model=SUPERVISOR_MODEL,
    base_url=SUPERVISOR_BASE_URL,
    api_key=SUPERVISOR_API_KEY
)

# Initialize Agent LLM
agent_llm = create_llm(
    model=AGENT_MODEL,
    base_url=AGENT_BASE_URL,
    api_key=AGENT_API_KEY
)
