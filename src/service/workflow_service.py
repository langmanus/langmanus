import logging

from src.config import TEAM_MEMBERS
from src.graph import build_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """Enable debug level logging for more detailed execution information."""
    logging.getLogger("src").setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

# Create the graph
graph = build_graph()


async def run_agent_workflow(user_input: str, debug: bool = False):
    """Run the agent workflow with the given user input.

    Args:
        user_input: The user's query or request
        debug: If True, enables debug level logging

    Returns:
        The final state after the workflow completes
    """
    if not user_input:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting workflow with user input: {user_input}")

    async for event in graph.astream_events(
        {
            # Constants
            "TEAM_MEMBERS": TEAM_MEMBERS,
            # Runtime Variables
            "messages": [{"role": "user", "content": user_input}],
        },
        version="v2",
    ):
        kind = event.get("event")
        data = event.get("data")
        name = event.get("name")
        node = (
            ""
            if (event.get("metadata").get("checkpoint_ns") is None)
            else event.get("metadata").get("checkpoint_ns").split(":")[0]
        )

        if kind == "on_chain_start" and name in [
            "supervisor",
            "researcher",
            "coder",
            "file_manager",
            "browser",
        ]:
            ydata = {
                "event": kind,
                "data": {"agent_name": name, "input": data.get("input")},
            }
        elif kind == "on_chain_end" and name in [
            "supervisor",
            "researcher",
            "coder",
            "file_manager",
            "browser",
        ]:
            ydata = {
                "event": kind,
                "data": {"agent_name": name, "output": data.get("output")},
            }
        elif kind == "on_chat_model_start":
            ydata = {
                "event": kind,
                "data": {"agent_name": node, "input": data.get("input")},
            }
        elif kind == "on_chat_model_end":
            ydata = {
                "event": kind,
                "data": {"agent_name": node, "output": data.get("output")},
            }
        elif kind == "on_chat_model_stream":
            content = data["chunk"].content
            if content is None or content == "":
                continue
            ydata = {"event": kind, "data": {"agent_name": node, "content": content}}
        elif kind == "on_tool_start":
            ydata = {
                "event": kind,
                "data": {
                    "agent_name": node,
                    "tool_name": name,
                    "input": data.get("input"),
                },
            }
        elif kind == "on_tool_end":
            ydata = {
                "event": kind,
                "data": {
                    "agent_name": node,
                    "name": name,
                    "output": data.get("output"),
                },
            }
        else:
            continue
        yield ydata
