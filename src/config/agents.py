# Team configuration
TEAM_MEMBERS = ["researcher", "coder"]

# System prompts
SUPERVISOR_PROMPT = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {TEAM_MEMBERS}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

RESEARCHER_PROMPT = "You are a researcher. DO NOT do any math."
CODER_PROMPT = "You are a coder who can execute Python code to solve problems." 