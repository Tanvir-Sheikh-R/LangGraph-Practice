import streamlit as st
from ui import load_page_style
import numpy as np
from chat_app_backend import chat, checkpointer
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage


load_page_style()

if 'message' not in st.session_state:
    st.session_state['message'] = []

st.markdown("# <h1>:material/asterisk: </h1><h2> Personal AI Assistant</h2>", unsafe_allow_html=True)

st.set_page_config(page_title="Personal AI Assistant", page_icon=":material/asterisk:")


st.subheader('Hi, Whats your agenda today?', text_alignment='left')

with st.sidebar:
     st.title('Chat history')
     st.button('New Chat', width='stretch', type='primary')




for messagees in st.session_state.message:
    if messagees["role"] == 'assistant':
        with st.chat_message('assistant' , avatar=":material/asterisk:"):
            st.write(messagees['msg'])

    if messagees["role"] == 'user':
         with st.chat_message('user'):
            st.write(messagees['msg'])
         

user_input = st.chat_input("Type here")

if user_input:
    st.session_state.message.append({'role': 'user', 'msg': user_input})

    with st.chat_message('user'):
            st.write(user_input)
    
    with st.chat_message('assistant' , avatar=":material/asterisk:"):
        response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chat.stream(
                {'message': [HumanMessage(user_input)]}, 
                config={'configurable': {'thread_id': '1'}}, 
                stream_mode='messages'
            ))
    st.session_state.message.append({'role': 'assistant', 'msg':  response})
            


print()
print(st.session_state)
# print(list(checkpointer.list(config={'thread_id': '1'})))