import logging
from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

# Initialize REPL and logger
repl = PythonREPL()
logger = logging.getLogger(__name__)

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code and do math. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    logger.info("Executing Python code")
    try:
        result = repl.run(code)
        logger.info("Code execution successful")
    except BaseException as e:
        error_msg = f"Failed to execute. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str 