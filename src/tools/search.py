from langchain_community.tools.tavily_search import TavilySearchResults
from src.config import TAVILY_MAX_RESULTS

# Initialize Tavily search tool
tavily_tool = TavilySearchResults(max_results=TAVILY_MAX_RESULTS) 