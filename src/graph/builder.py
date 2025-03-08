from langgraph.graph import StateGraph, START

from .types import State
from .nodes import supervisor_node, research_node, code_node, file_manager_node

def build_graph():
    """Build and return the agent workflow graph."""
    builder = StateGraph(State)
    builder.add_edge(START, "supervisor")
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", research_node)
    builder.add_node("coder", code_node)
    builder.add_node("file_manager", file_manager_node)
    return builder.compile()