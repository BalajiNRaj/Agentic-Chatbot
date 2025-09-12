from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot import BasicChatBot
from src.langgraphagenticai.nodes.chatbot_with_tools import ChatbothWithTools
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraphagenticai.nodes.ai_news import AiNews

class GraphBuilder:

    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def build_chatbot_graph(self):

        self.basic_chat_node = BasicChatBot(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chat_node.process)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    
    def build_chatbot_graph_with_tools(self):
        
        tools = get_tools()
        tool_node = create_tool_node(tools=tools)

        chatbot_with_tools = ChatbothWithTools(self.llm)
        self.chatbot_node = chatbot_with_tools.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", self.chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        # self.grapph_builder.add_edge("chatbot", END)

    def build_ai_news_graph(self):

        ai_news = AiNews(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news.fetch_news)
        self.graph_builder.add_node("summarizer", ai_news.summarize)
        # self.grapph_builder.add_node("save_result", ai_news.save_results)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarizer")
        # self.grapph_builder.add_edge("summarizer", "save_result")
        self.graph_builder.add_edge("summarizer", END)


    def setup_graph(self, usecase: str):
        """
        Set up the graph for the selected usecase
        """
        if usecase == "Basic Chatbot":
            self.build_chatbot_graph()
        if usecase == "Chatbot With Tools":
            self.build_chatbot_graph_with_tools()
        if usecase == "AI News":
            self.build_ai_news_graph()

        return self.graph_builder.compile()