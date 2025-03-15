import logging

from src.config import TEAM_MEMBERS
from src.graph import build_graph
from langchain_community.adapters.openai import convert_message_to_dict
import uuid

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


async def run_agent_workflow(user_input_messages: list, debug: bool = False):
    """Run the agent workflow with the given user input.

    Args:
        user_input_messages: The user request messages
        debug: If True, enables debug level logging

    Returns:
        The final state after the workflow completes
    """
    if not user_input_messages:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting workflow with user input: {user_input_messages}")

    workflow_id = str(uuid.uuid4())

    streamed_agents = [*TEAM_MEMBERS, "reporter"]

    yield {
        "event": "start_of_workflow",
        "data": {"workflow_id": workflow_id, "input": user_input_messages},
    }

    # TODO: extract message content from object, specifically for on_chat_model_stream
    async for event in graph.astream_events(
        {
            # Constants
            "TEAM_MEMBERS": TEAM_MEMBERS,
            # Runtime Variables
            "messages": user_input_messages,
        },
        version="v2",
    ):
        kind = event.get("event")
        data = event.get("data")
        name = event.get("name")
        metadata = event.get("metadata")
        node = (
            ""
            if (metadata.get("checkpoint_ns") is None)
            else metadata.get("checkpoint_ns").split(":")[0]
        )
        langgraph_step = (
            ""
            if (metadata.get("langgraph_step") is None)
            else str(metadata["langgraph_step"])
        )
        tool_checkpoint = (
            ""
            if (metadata.get("langgraph_checkpoint_ns") is None)
            else metadata.get("langgraph_checkpoint_ns").split(":")[-1]
        )

        if kind == "on_chain_start" and name in streamed_agents:
            ydata = {
                "event": "start_of_agent",
                "data": {
                    "agent_name": name,
                    "agent_id": f"{workflow_id}_{name}_{langgraph_step}",
                },
            }
        elif kind == "on_chain_end" and name in streamed_agents:
            ydata = {
                "event": "end_of_agent",
                "data": {
                    "agent_name": name,
                    "agent_id": f"{workflow_id}_{name}_{langgraph_step}",
                },
            }
        elif kind == "on_chat_model_start" and node in streamed_agents:
            ydata = {
                "event": "start_of_llm",
                "data": {"agent_name": node},
            }
        elif kind == "on_chat_model_end" and node in streamed_agents:
            ydata = {
                "event": "end_of_llm",
                "data": {"agent_name": node},
            }
        elif kind == "on_chat_model_stream" and node in streamed_agents:
            content = data["chunk"].content
            if content is None or content == "":
                continue
            ydata = {
                "event": "message",
                "data": {"message_id": data["chunk"].id, "delta": {"content": content}},
            }
        elif kind == "on_tool_start":
            ydata = {
                "event": "tool_call",
                "data": {
                    "tool_call_id": f"{workflow_id}_{node}_{name}_{tool_checkpoint}",
                    "tool_name": name,
                    "tool_input": data.get("input"),
                },
            }
        elif kind == "on_tool_end":
            ydata = {
                "event": "tool_call_result",
                "data": {
                    "tool_call_id": f"{workflow_id}_{node}_{name}_{tool_checkpoint}",
                    "tool_name": name,
                    "tool_result": data["output"].content if data.get("output") else "",
                },
            }
        else:
            continue
        yield ydata

    yield {
        "event": "end_of_workflow",
        "data": {
            "workflow_id": workflow_id,
            "messages": [
                convert_message_to_dict(msg)
                for msg in data["output"].get("messages", [])
            ],
        },
    }
