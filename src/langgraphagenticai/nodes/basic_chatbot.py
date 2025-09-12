from src.langgraphagenticai.state.state import State


class BasicChatBot:
    """
    Basic Chatbot implementation
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Process the input state message and generated the response.
        """

        return {"messages": self.llm.invoke(state['messages'])}