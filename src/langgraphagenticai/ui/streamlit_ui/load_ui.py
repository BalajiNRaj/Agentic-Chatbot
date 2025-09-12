import os
import streamlit as st

from src.langgraphagenticai.ui.ui_config import Config

class LoadStreamLitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_strealit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state['fetch_news'] = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            llm_model_options = self.config.get_ollama_model_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)
            self.user_controls['selected_llm_model_options'] = st.selectbox("Select LLM Model", llm_model_options)
            self.user_controls['selected_usecase'] = st.selectbox("Usecase: ", usecase_options)

            if self.user_controls['selected_usecase'] == "Chatbot With Tools" or self.user_controls['selected_usecase'] == "AI News":
                os.environ['TAVILY_API_KEY'] = self.user_controls['TAVILY_API_KEY'] = st.session_state['TAVILY_API_KEY'] = st.text_input("Tavily API Key", type="password")

                if not self.user_controls['TAVILY_API_KEY']:
                    st.warning("Please enter you Tavily API Key to proceed.")

            if self.user_controls['selected_usecase'] == "AI News":
                st.subheader("AI News Explorer")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select your Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )

                    if st.button("Fetch AI News", use_container_width=True):
                        st.session_state['time_frame'] = time_frame
                        st.session_state['fetch_news'] = True

        # print(self.user_controls)

        return self.user_controls
    
