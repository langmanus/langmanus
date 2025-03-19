from .env import (
    # AZURE Config
    AZURE_API_BASE,
    AZURE_API_KEY,
    AZURE_API_VERSION,
    # Reasoning LLM
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    REASONING_AZURE_DEPLOYMENT,
    # Basic LLM
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    BASIC_AZURE_DEPLOYMENT,
    # Vision-language LLM
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
    VL_AZURE_DEPLOYMENT,
    # Other configurations
    CHROME_INSTANCE_PATH,
    CHROME_HEADLESS,
    CHROME_PROXY_SERVER,
    CHROME_PROXY_USERNAME,
    CHROME_PROXY_PASSWORD,
)
from .tools import TAVILY_MAX_RESULTS

# Team configuration
TEAM_MEMBERS = ["researcher", "coder", "browser", "reporter"]

__all__ = [
    # Reasoning LLM
    "REASONING_MODEL",
    "REASONING_BASE_URL",
    "REASONING_API_KEY",
    # Basic LLM
    "BASIC_MODEL",
    "BASIC_BASE_URL",
    "BASIC_API_KEY",
    # Vision-language LLM
    "VL_MODEL",
    "VL_BASE_URL",
    "VL_API_KEY",
    # Other configurations
    "TEAM_MEMBERS",
    "TAVILY_MAX_RESULTS",
    "CHROME_INSTANCE_PATH",
    "CHROME_HEADLESS",
    "CHROME_PROXY_SERVER",
    "CHROME_PROXY_USERNAME",
    "CHROME_PROXY_PASSWORD",
]
