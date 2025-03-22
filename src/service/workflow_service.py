import logging
from typing import Optional
import asyncio

from src.config import TEAM_MEMBER_CONFIGRATIONS, TEAM_MEMBERS
from src.graph import build_graph
from src.tools.browser import browser_tool
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

# Cache for coordinator messages
coordinator_cache = []
MAX_CACHE_SIZE = 3

# Global variable to track current browser tool instance
current_browser_tool: Optional[browser_tool] = None


async def run_agent_workflow(
    user_input_messages: list,
    debug: Optional[bool] = False,
    deep_thinking_mode: Optional[bool] = False,
    search_before_planning: Optional[bool] = False,
    team_members: Optional[list] = None,
):
    """Run the agent workflow to process and respond to user input messages.

    This function orchestrates the execution of various agents in a workflow to handle
    user requests. It manages agent communication, tool usage, and generates streaming
    events for the workflow progress.

    Args:
        user_input_messages: List of user messages to process in the workflow
        debug: If True, enables debug level logging for detailed execution information
        deep_thinking_mode: If True, enables more thorough analysis and consideration
            in agent responses
        search_before_planning: If True, performs preliminary research before creating
            the execution plan
        team_members: Optional list of specific team members to involve in the workflow.
            If None, uses default TEAM_MEMBERS configuration

    Returns:
        Yields various event dictionaries containing workflow state and progress information,
        including agent activities, tool calls, and the final workflow state

    Raises:
        ValueError: If user_input_messages is empty
        asyncio.CancelledError: If the workflow is cancelled during execution
    """
    if not user_input_messages:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting workflow with user input: {user_input_messages}")

    workflow_id = str(uuid.uuid4())

    team_members = team_members if team_members else TEAM_MEMBERS

    streaming_llm_agents = [*team_members, "planner", "coordinator"]

    # Reset coordinator cache at the start of each workflow
    global coordinator_cache, current_browser_tool
    coordinator_cache = []
    current_browser_tool = browser_tool
    global is_handoff_case
    is_handoff_case = False

    try:
        async for event in graph.astream_events(
            {
                # Constants
                "TEAM_MEMBERS": team_members,
                "TEAM_MEMBER_CONFIGRATIONS": TEAM_MEMBER_CONFIGRATIONS,
                # Runtime Variables
                "messages": user_input_messages,
                "deep_thinking_mode": deep_thinking_mode,
                "search_before_planning": search_before_planning,
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
            run_id = "" if (event.get("run_id") is None) else str(event["run_id"])

            if kind == "on_chain_start" and name in streaming_llm_agents:
                if name == "planner":
                    yield {
                        "event": "start_of_workflow",
                        "data": {
                            "workflow_id": workflow_id,
                            "input": user_input_messages,
                        },
                    }
                ydata = {
                    "event": "start_of_agent",
                    "data": {
                        "agent_name": name,
                        "agent_id": f"{workflow_id}_{name}_{langgraph_step}",
                    },
                }
            elif kind == "on_chain_end" and name in streaming_llm_agents:
                ydata = {
                    "event": "end_of_agent",
                    "data": {
                        "agent_name": name,
                        "agent_id": f"{workflow_id}_{name}_{langgraph_step}",
                    },
                }
            elif kind == "on_chat_model_start" and node in streaming_llm_agents:
                ydata = {
                    "event": "start_of_llm",
                    "data": {"agent_name": node},
                }
            elif kind == "on_chat_model_end" and node in streaming_llm_agents:
                ydata = {
                    "event": "end_of_llm",
                    "data": {"agent_name": node},
                }
            elif kind == "on_chat_model_stream" and node in streaming_llm_agents:
                content = data["chunk"].content
                if content is None or content == "":
                    if not data["chunk"].additional_kwargs.get("reasoning_content"):
                        # Skip empty messages
                        continue
                    ydata = {
                        "event": "message",
                        "data": {
                            "message_id": data["chunk"].id,
                            "delta": {
                                "reasoning_content": (
                                    data["chunk"].additional_kwargs["reasoning_content"]
                                )
                            },
                        },
                    }
                else:
                    # Check if the message is from the coordinator
                    if node == "coordinator":
                        if len(coordinator_cache) < MAX_CACHE_SIZE:
                            coordinator_cache.append(content)
                            cached_content = "".join(coordinator_cache)
                            if cached_content.startswith("handoff"):
                                is_handoff_case = True
                                continue
                            if len(coordinator_cache) < MAX_CACHE_SIZE:
                                continue
                            # Send the cached message
                            ydata = {
                                "event": "message",
                                "data": {
                                    "message_id": data["chunk"].id,
                                    "delta": {"content": cached_content},
                                },
                            }
                        elif not is_handoff_case:
                            # For other agents, send the message directly
                            ydata = {
                                "event": "message",
                                "data": {
                                    "message_id": data["chunk"].id,
                                    "delta": {"content": content},
                                },
                            }
                    else:
                        # For other agents, send the message directly
                        ydata = {
                            "event": "message",
                            "data": {
                                "message_id": data["chunk"].id,
                                "delta": {"content": content},
                            },
                        }
            elif kind == "on_tool_start" and node in team_members:
                ydata = {
                    "event": "tool_call",
                    "data": {
                        "tool_call_id": f"{workflow_id}_{node}_{name}_{run_id}",
                        "tool_name": name,
                        "tool_input": data.get("input"),
                    },
                }
            elif kind == "on_tool_end" and node in team_members:
                ydata = {
                    "event": "tool_call_result",
                    "data": {
                        "tool_call_id": f"{workflow_id}_{node}_{name}_{run_id}",
                        "tool_name": name,
                        "tool_result": (
                            data["output"].content if data.get("output") else ""
                        ),
                    },
                }
            else:
                continue
            yield ydata
    except asyncio.CancelledError:
        logger.info("Workflow cancelled, terminating browser agent if exists")
        if current_browser_tool:
            await current_browser_tool.terminate()
        raise
    finally:
        if current_browser_tool:
            await current_browser_tool.terminate()
        current_browser_tool = None

    if is_handoff_case:
        # TODO: remove messages attributes after Frontend being compatible with final_session_state event.
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
    yield {
        "event": "final_session_state",
        "data": {
            "messages": [
                convert_message_to_dict(msg)
                for msg in data["output"].get("messages", [])
            ],
        },
    }
