import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

class DisplayStreamlitResults:

    def __init__(self, usecase, input_message, graph):
        self.usecase = usecase
        self.input_message = input_message
        self.graph = graph

    def display_results_on_ui(self):
        usecase = self.usecase
        input_message = self.input_message
        graph = self.graph

        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ('user', input_message)}):
                print(event.values())

                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(input_message)
                    with st.chat_message("assistant"):
                        st.write(value['messages'].content)


        elif usecase == "Chatbot With Tools":
            initial_stage = {'messages': [input_message]}
            res = graph.invoke(initial_stage)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                if type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call START")
                        st.write(message.content)
                        st.write("Tool call END")
                if type(message) == AIMessage:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News":
            freq = self.input_message
            with st.spinner("Fetching AI News and summarizing..."):
                result = graph.invoke({"messages": freq})
                try:
                    # print(result)
                    st.markdown(result['messages'][-1].content, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occured: {str(e)}")