import logging
from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

from crawler import Crawler

logger = logging.getLogger(__name__)


@tool
def crawl_tool(
    url: Annotated[str, "The url to crawl."],
) -> ToolMessage:
    """Use this to crawl a url and get a readable content in markdown format."""
    try:
        crawler = Crawler()
        article = crawler.crawl(url)
        return article.to_tool_message(tool_name=crawl_tool.__name__)
    except BaseException as e:
        error_msg = f"Failed to crawl. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
