from src.langgraphagenticai.state.state import State

class ChatbothWithTools:
    """
    Chatbot logic ehnaced with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    ## Without tools
    def process(self, state: State) -> dict:
        """
        Processes the user input and generates the response with the help of tools integrated.
        """

        user_input = state['messages'][-1] if state['messages'] else ""

        llm_response = self.llm.invoke({'role': 'user', 'content': user_input})

        tool_response = f"Tool Response for : '{user_input}'"

        return {'messages': [llm_response, tool_response]}
    
    ## Binded with tools
    def create_chatbot(self, tools):
        """
        Returns a chatbot node funtion.
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic is processing the input state and returning a response.
            """

            return {'messages': [llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node