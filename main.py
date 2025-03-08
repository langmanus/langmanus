"""
Entry point script for the LangGraph Demo.
"""
from src.workflow import run_agent_workflow


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your query: ")
    
    result = run_agent_workflow(user_query)
    
    # Print the conversation history
    print("\n=== Conversation History ===")
    for message in result["messages"]:
        role = message.type
        print(f"\n[{role.upper()}]: {message.content}")