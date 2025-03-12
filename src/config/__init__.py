from .env import (
    SUPERVISOR_BASE_URL,
    SUPERVISOR_MODEL,
    SUPERVISOR_API_KEY,
    AGENT_BASE_URL,
    AGENT_MODEL,
    AGENT_API_KEY,
    CHROME_INSTANCE_PATH,
)
from .tools import TAVILY_MAX_RESULTS

# Team configuration
TEAM_MEMBERS = ["researcher", "coder", "file_manager", "browser"]

__all__ = [
    "SUPERVISOR_BASE_URL",
    "SUPERVISOR_MODEL",
    "SUPERVISOR_API_KEY",
    "AGENT_BASE_URL",
    "AGENT_MODEL",
    "AGENT_API_KEY",
    "TEAM_MEMBERS",
    "TAVILY_MAX_RESULTS",
    "CHROME_INSTANCE_PATH",
]
