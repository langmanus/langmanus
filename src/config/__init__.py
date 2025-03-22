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
from .tools import TAVILY_MAX_RESULTS, BROWSER_HISTORY_DIR
from .loader import load_yaml_config

# Team configuration
TEAM_MEMBER_CONFIGRATIONS = {
    "researcher": {
        "name": "researcher",
        "desc": (
            "Responsible for searching and collecting relevant information, understanding user needs and conducting research analysis"
        ),
        "is_optional": False,
    },
    "coder": {
        "name": "coder",
        "desc": (
            "Responsible for code implementation, debugging and optimization, handling technical programming tasks"
        ),
        "is_optional": True,
    },
    "browser": {
        "name": "browser",
        "desc": "Responsible for web browsing, content extraction and interaction",
        "is_optional": True,
    },
    "reporter": {
        "name": "reporter",
        "desc": (
            "Responsible for summarizing analysis results, generating reports and presenting final outcomes to users"
        ),
        "is_optional": False,
    },
}

TEAM_MEMBERS = list(TEAM_MEMBER_CONFIGRATIONS.keys())

__all__ = [
    # Reasoning LLM
    "REASONING_MODEL",
    "REASONING_BASE_URL",
    "REASONING_API_KEY",
    "REASONING_AZURE_DEPLOYMENT",
    # Basic LLM
    "BASIC_MODEL",
    "BASIC_BASE_URL",
    "BASIC_API_KEY",
    "BASIC_AZURE_DEPLOYMENT",
    # Vision-language LLM
    "VL_MODEL",
    "VL_BASE_URL",
    "VL_API_KEY",
    "VL_AZURE_DEPLOYMENT",
    # Other configurations
    "TEAM_MEMBERS",
    "TEAM_MEMBER_CONFIGRATIONS" "TAVILY_MAX_RESULTS",
    "CHROME_INSTANCE_PATH",
    "CHROME_HEADLESS",
    "CHROME_PROXY_SERVER",
    "CHROME_PROXY_USERNAME",
    "CHROME_PROXY_PASSWORD",
    "BROWSER_HISTORY_DIR",
    # Azure configurations
    "AZURE_API_BASE",
    "AZURE_API_KEY",
    "AZURE_API_VERSION",
]
