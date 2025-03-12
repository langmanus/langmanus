import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supervisor LLM configuration
SUPERVISOR_MODEL = os.getenv(
    "SUPERVISOR_MODEL", "gpt-4"
)  # You might want to use a more capable model for supervision
SUPERVISOR_BASE_URL = os.getenv(
    "SUPERVISOR_BASE_URL"
)  # Can be configured separately if needed
SUPERVISOR_API_KEY = os.getenv(
    "SUPERVISOR_API_KEY"
)  # Can be configured separately if needed

# Agent LLM configuration
AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4o")  # Can be a different model for agents
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL")  # Can be configured separately if needed
AGENT_API_KEY = os.getenv("AGENT_API_KEY")  # Can be configured separately if needed


# Chrome Instance configuration
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH")
