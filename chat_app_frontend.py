import streamlit as st
import numpy as np
from chat_app_backend import chat
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

if 'message' not in st.session_state:
    st.session_state['message'] = []

st.title('Chat App', text_alignment='center')
st.subheader('Hi, Whats your agenda today?', text_alignment='center')

for messagees in st.session_state.message:
    with st.chat_message(messagees["role"]):
        st.write(messagees['msg'])

user_input = st.chat_input("Type here")

if user_input:
    st.session_state.message.append({'role': 'user', 'msg': user_input})

    with st.chat_message('user'):
            st.write(user_input)
    
    with st.chat_message('assistant'):
        response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chat.stream(
                {'message': [HumanMessage(user_input)]}, 
                config={'configurable': {'thread_id': '1'}}, 
                stream_mode='messages'
            ))
    st.session_state.message.append({'role': 'assistant', 'msg':  response})
            

print()
print(st.session_state)