from langgraph.prebuilt import create_react_agent

from src.config import RESEARCHER_PROMPT, CODER_PROMPT, FILE_MANAGER_PROMPT
from src.tools import tavily_tool, python_repl_tool, write_file_tool
from .llm import llm

# Create specialized agents
research_agent = create_react_agent(
    llm, tools=[tavily_tool], prompt=RESEARCHER_PROMPT
)

code_agent = create_react_agent(
    llm, tools=[python_repl_tool], prompt=CODER_PROMPT
)

file_manager_agent = create_react_agent(
    llm, tools=[write_file_tool], prompt=FILE_MANAGER_PROMPT
) 