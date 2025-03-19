import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reasoning LLM configuration (for complex reasoning tasks)
REASONING_MODEL = os.getenv("REASONING_MODEL", "o1-mini")
REASONING_BASE_URL = os.getenv("REASONING_BASE_URL")
REASONING_API_KEY = os.getenv("REASONING_API_KEY")

# Non-reasoning LLM configuration (for straightforward tasks)
BASIC_MODEL = os.getenv("BASIC_MODEL", "gpt-4o")
BASIC_BASE_URL = os.getenv("BASIC_BASE_URL")
BASIC_API_KEY = os.getenv("BASIC_API_KEY")

# Azure OpenAI配置（按LLM类型区分）
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
# 各类型专用部署名称
BASIC_AZURE_DEPLOYMENT = os.getenv("BASIC_AZURE_DEPLOYMENT")
VL_AZURE_DEPLOYMENT = os.getenv("VL_AZURE_DEPLOYMENT")
REASONING_AZURE_DEPLOYMENT = os.getenv("REASONING_AZURE_DEPLOYMENT")

# Vision-language LLM configuration (for tasks requiring visual understanding)
VL_MODEL = os.getenv("VL_MODEL", "gpt-4o")
VL_BASE_URL = os.getenv("VL_BASE_URL")
VL_API_KEY = os.getenv("VL_API_KEY")

# Chrome Instance configuration
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH")
CHROME_HEADLESS = os.getenv("CHROME_HEADLESS", "False") == "True"
CHROME_PROXY_SERVER = os.getenv("CHROME_PROXY_SERVER")
CHROME_PROXY_USERNAME = os.getenv("CHROME_PROXY_USERNAME")
CHROME_PROXY_PASSWORD = os.getenv("CHROME_PROXY_PASSWORD")
