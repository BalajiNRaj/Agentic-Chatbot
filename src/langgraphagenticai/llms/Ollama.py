import streamlit as st
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

class OllamaLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_ollama_model(self):
        try:
            selected_llm_model_options = self.user_controls_input["selected_llm_model_options"]

            # llm = ChatOllama(model = selected_llm_model_options)
            llm = ChatOpenAI(
                api_key="ollama",
                model=selected_llm_model_options,
                # model="llama2:7b-chat",
                base_url="http://localhost:11434/v1",
                temperature=0.4,
            )

        except Exception as e:
            raise ValueError(f"Error while initiating the model : {e}")
        
        return llm
    