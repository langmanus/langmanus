from langgraph.prebuilt import create_react_agent

from src.prompts import apply_prompt_template
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    python_repl_tool,
    tavily_tool,
    write_file_tool,
)

from .llm import agent_llm as llm

# Create specialized agents
research_agent = create_react_agent(
    llm,
    tools=[tavily_tool, crawl_tool],
    prompt=lambda state: apply_prompt_template("researcher", state),
)

coder_agent = create_react_agent(
    llm,
    tools=[python_repl_tool, bash_tool],
    prompt=lambda state: apply_prompt_template("coder", state),
)

file_manager_agent = create_react_agent(
    llm,
    tools=[write_file_tool],
    prompt=lambda state: apply_prompt_template("file_manager", state),
)

browser_agent = create_react_agent(
    llm,
    tools=[browser_tool],
    prompt=lambda state: apply_prompt_template("browser", state),
)
