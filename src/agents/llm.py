from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_deepseek import ChatDeepSeek
from typing import Optional

from src.config import (
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
    AZURE_API_BASE,
    AZURE_API_KEY,
    AZURE_API_VERSION,
    BASIC_AZURE_DEPLOYMENT,
    VL_AZURE_DEPLOYMENT,
    REASONING_AZURE_DEPLOYMENT,
)
from src.config.agents import LLMType


def create_openai_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance with the specified configuration
    """
    # Only include base_url in the arguments if it's not None or empty
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # This will handle None or empty string
        llm_kwargs["base_url"] = base_url

    if api_key:  # This will handle None or empty string
        llm_kwargs["api_key"] = api_key

    return ChatOpenAI(**llm_kwargs)


def create_deepseek_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatDeepSeek:
    """
    Create a ChatDeepSeek instance with the specified configuration
    """
    # Only include base_url in the arguments if it's not None or empty
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # This will handle None or empty string
        llm_kwargs["api_base"] = base_url

    if api_key:  # This will handle None or empty string
        llm_kwargs["api_key"] = api_key

    return ChatDeepSeek(**llm_kwargs)


def create_azure_llm(
    azure_deployment: str,
    azure_endpoint: str,
    api_version: str,
    api_key: str,
    temperature: float = 0.0,
) -> AzureChatOpenAI:
    """
    create azure llm instance with specified configuration
    """
    return AzureChatOpenAI(
        azure_deployment=azure_deployment,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        api_key=api_key,
        temperature=temperature,
    )


# Cache for LLM instances
_llm_cache: dict[LLMType, ChatOpenAI | ChatDeepSeek] = {}


def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI | ChatDeepSeek | AzureChatOpenAI:
    """
    Get LLM instance by type. Returns cached instance if available.
    """
    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    if llm_type == "reasoning":
        if REASONING_AZURE_DEPLOYMENT:
            llm = create_azure_llm(
                azure_deployment=REASONING_AZURE_DEPLOYMENT,
                azure_endpoint=AZURE_API_BASE,
                api_version=AZURE_API_VERSION,
                api_key=AZURE_API_KEY,
            )
        else:
            llm = create_deepseek_llm(
                model=REASONING_MODEL,
                base_url=REASONING_BASE_URL,
                api_key=REASONING_API_KEY,
            )
    elif llm_type == "basic":
        if BASIC_AZURE_DEPLOYMENT:
            llm = create_azure_llm(
                azure_deployment=BASIC_AZURE_DEPLOYMENT,
                azure_endpoint=AZURE_API_BASE,
                api_version=AZURE_API_VERSION,
                api_key=AZURE_API_KEY,
            )
        else:
            llm = create_openai_llm(
                model=BASIC_MODEL,
                base_url=BASIC_BASE_URL,
                api_key=BASIC_API_KEY,
            )
    elif llm_type == "vision":
        if VL_AZURE_DEPLOYMENT:
            llm = create_azure_llm(
                azure_deployment=BASIC_AZURE_DEPLOYMENT,
                azure_endpoint=AZURE_API_BASE,
                api_version=AZURE_API_VERSION,
                api_key=AZURE_API_KEY,
            )
        else:
            llm = create_openai_llm(
                model=VL_MODEL,
                base_url=VL_BASE_URL,
                api_key=VL_API_KEY,
            )
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")

    _llm_cache[llm_type] = llm
    return llm


# Initialize LLMs for different purposes - now these will be cached
reasoning_llm = get_llm_by_type("reasoning")
basic_llm = get_llm_by_type("basic")
vl_llm = get_llm_by_type("vision")


if __name__ == "__main__":
    stream = reasoning_llm.stream("what is mcp?")
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    print(full_response)

    basic_llm.invoke("Hello")
    vl_llm.invoke("Hello")
