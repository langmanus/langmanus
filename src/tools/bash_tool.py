import logging
import subprocess
from typing import Annotated
from langchain_core.tools import tool

# Initialize logger
logger = logging.getLogger(__name__)

@tool
def bash_tool(
    cmd: Annotated[str, "The bash command to be executed."],
):
    """Use this to execute bash command and do necessary operations."""
    logger.info(f"Executing Bash Command: {cmd}")
    try:
        # Execute the command and capture output
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        # Return stdout as the result
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If command fails, return error information
        error_message = f"Command failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        # Catch any other exceptions
        error_message = f"Error executing command: {str(e)}"
        logger.error(error_message)
        return error_message

if __name__ == "__main__":
    print(bash_tool.invoke("ls -all"))
