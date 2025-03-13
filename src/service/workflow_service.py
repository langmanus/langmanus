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

    async for event in graph.astream_events({
        # Constants
        "TEAM_MEMBERS": TEAM_MEMBERS,
        # Runtime Variables
        "messages": [{"role": "user", "content": user_input}],
    }, version="v2"):
        kind = event.get("event")
        data = event.get("data")
        name = event.get("name")
        node = "" if (event.get("metadata").get("checkpoint_ns")
                      is None) else event.get("metadata").get("checkpoint_ns").split(":")[0]

        print()
        if name == "_write":
            continue
        # if kind in ("on_chat_model_start", "on_chat_model_end", "on_llm_start",
        #             "on_llm_stream", "on_llm_end", "on_chain_start", "on_chain_stream", "on_chain_end", "on_tool_start", "on_tool_end", "on_retriever_start", "on_retriever_end", "on_prompt_start", "on_prompt_end"):
        #
        # elif kind == "on_chat_model_stream":
        #     ydata = {
        #         "kind": kind,
        #         "name": name,
        #         "node": event.get("metadata").get("langgraph_node"),
        #         "data": event["data"]["chunk"].content
        #     }
        ydata = {
            "kind": kind,
            "name": name,
            "data": data,
            "node": node,
        }

        yield ydata



    # logger.debug(f"Final workflow state: {result}")
    # logger.info("Workflow completed successfully")
    # return result
