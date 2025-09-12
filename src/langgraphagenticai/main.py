import streamlit as st

from src.langgraphagenticai.ui.streamlit_ui.load_ui import LoadStreamLitUI
from src.langgraphagenticai.llms.Ollama import OllamaLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder 
from src.langgraphagenticai.ui.streamlit_ui.display_results import DisplayStreamlitResults 

def load_langgraph_agenticai_app():
    """
    Loads and run the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM Model.
    sets ip the graph based on the selected usecase and displays the output while 
    implementing exception handling for robustness.
    """

    ui = LoadStreamLitUI()
    user_input = ui.load_strealit_ui()


    if not user_input:
        st.error("Error: Faileed to load the user input from UI")
        return
    

    if st.session_state['fetch_news'] == True:
        user_message = st.session_state['time_frame']
        st.session_state['fetch_news'] = False
    else:
        user_message = st.chat_input("Jot down your question")

    if user_message:
        try:
            llm = OllamaLLM(user_controls_input=user_input)
            model = llm.get_ollama_model()

            if not model:
                st.error("Error: LLM Model is not ready")

            usecase = user_input.get('selected_usecase')

            if not usecase:
                st.error("Error: Usecase is not set")

            graph_builder = GraphBuilder(model)

            graph = graph_builder.setup_graph(usecase)

            DisplayStreamlitResults(usecase, input_message=user_message, graph=graph).display_results_on_ui()

        except Exception as e:
            st.error(f"Error: Graph set up failed: {e}")
            return