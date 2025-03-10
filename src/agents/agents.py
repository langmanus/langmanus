from langgraph.prebuilt import create_react_agent

from src.config import CODER_PROMPT, FILE_MANAGER_PROMPT, RESEARCHER_PROMPT
from src.tools import crawl_tool, python_repl_tool, tavily_tool, write_file_tool, bash_tool

from .llm import agent_llm as llm

# Create specialized agents
research_agent = create_react_agent(
    llm, tools=[tavily_tool, crawl_tool], prompt=RESEARCHER_PROMPT
)

coder_agent = create_react_agent(llm, tools=[python_repl_tool, bash_tool], prompt=CODER_PROMPT)

file_manager_agent = create_react_agent(
    llm, tools=[write_file_tool], prompt=FILE_MANAGER_PROMPT
)
