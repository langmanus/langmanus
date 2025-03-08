import logging
from src.graph import build_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the graph
graph = build_graph() 

def run_agent_workflow(user_input: str):
    """Run the agent workflow with the given user input.
    
    Args:
        user_input: The user's query or request
        
    Returns:
        The final state after the workflow completes
    """
    logger.info(f"Starting workflow with user input: {user_input}")
    result = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    logger.info("Workflow completed successfully")
    return result