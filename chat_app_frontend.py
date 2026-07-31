import streamlit as st
import numpy as np
from chat_app_backend import chat
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

if 'message' not in st.session_state:
    st.session_state['message'] = []

st.title('Chat App', text_alignment='center')
st.subheader('Hi, Whats your agenda today?', text_alignment='center')

user_input = st.chat_input("Type here")

if user_input:
    st.session_state.message.append({'role': 'user', 'msg': user_input})

    config = {'configurable': {'thread_id': '1'}}
    response = chat.invoke({'message': [HumanMessage(user_input)]}, config=config)

    st.session_state.message.append({'role': 'assistant', 'msg':  response['message'][-1].content})


for messagees in st.session_state.message:
    with st.chat_message(messagees["role"]):
        st.write(messagees["msg"])

print()
print(st.session_state)