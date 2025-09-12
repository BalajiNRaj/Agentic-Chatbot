from langchain_community.tools.tavily_search import TavilySearchResults
from  langgraph.prebuilt import ToolNode


def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """

    tools = [TavilySearchResults(max_results=2)]

    return tools

def create_tool_node(tools):
    """
    Create tool node and returns with the give set of tools 
    """

    return ToolNode(tools=tools)