import streamlit as st
import tempfile
import os
from ui import load_page_style
import numpy as np
from chat_app_backend import chat, checkpointer_inMemory ,get_summary_for_chatHead, retrive_all_threads
from chat_app_backend_rag import rag_chat, list_indexed_docs, ingest_documents
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
import uuid

load_page_style()



# ****************************** Utility Functions ******************************
def generate_thread_id():
    id = uuid.uuid4()
    return id

def reset_chat():
    st.session_state['message'] = []

    new_id = generate_thread_id()
    st.session_state['thread_id'] = new_id
    add_thread(new_id)
    

def add_thread(thread_id):
    if thread_id not in st.session_state['thread_id_list']:
        st.session_state['thread_id_list'].append(thread_id)


def load_conversation(thread_id):
    conversation = chat.get_state({'configurable': {'thread_id': thread_id}}).values.get('message')
    return conversation



# ****************************** Session States ******************************
if 'message' not in st.session_state:
    st.session_state['message'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'thread_id_list' not in st.session_state:
    # if i want to use sqlite to store my conversations
    # st.session_state['thread_id_list'] = retrive_all_threads()
    st.session_state['thread_id_list'] = []

if 'indexed_docs' not in st.session_state:
    st.session_state['indexed_docs'] = list_indexed_docs()

if 'use_rag' not in st.session_state:
    st.session_state['use_rag'] = False


add_thread(st.session_state['thread_id'])



# ****************************** SideBar UI ******************************

with st.sidebar:
    st.title('AI Assistant')

    if st.button('New Chat', width='stretch', type='primary'):
        reset_chat()

    st.header('Chat history')

    for id in st.session_state.thread_id_list[::-1]:
        conversation = load_conversation(id)

        if conversation:
            user = conversation[0].content
            summery = get_summary_for_chatHead(user)

            if st.button(summery, width='stretch', key=id):
                response = load_conversation(id)
                temp_message = []

                for msg in response:
                    if isinstance(msg, HumanMessage):
                        role = 'user'
                    else:
                        role = 'assistant'

                    temp_message.append({'role': role, 'msg': msg.content})

                st.session_state['message'] = temp_message
            

# ******************************* RAG Features *******************************
    st.divider()
    st.header('Knowledge Base')

    uploaded_files = st.file_uploader(
        'Upload documents',
        type=['pdf', 'docx', 'txt', 'md'],
        accept_multiple_files=True,
    )

    if uploaded_files:
        saved_names = []
        with st.spinner('Loading embedder and indexing documents...'):
            paths = []
            tmpdir = tempfile.mkdtemp()
            try:
                for up in uploaded_files:
                    tmp_path = os.path.join(tmpdir, up.name)
                    with open(tmp_path, 'wb') as f:
                        f.write(up.getvalue())
                    paths.append(tmp_path)
                saved_names = ingest_documents(paths)
            finally:
                import shutil
                shutil.rmtree(tmpdir, ignore_errors=True)
        st.session_state['indexed_docs'] = list_indexed_docs()
        st.success(f'Indexed: {", ".join(saved_names)}')

    if st.session_state.indexed_docs:
        st.caption('Indexed documents')
        for name in st.session_state.indexed_docs:
            st.write(f"• {name}")

    if st.toggle('Use RAG (documents as knowledge base)'):
        st.session_state['use_rag'] = True
    else:
        st.session_state['use_rag'] = False
            


st.image("src/logo_green.svg", width=80)
st.markdown("""# <h1>Personal AI Assistant</h1>""", unsafe_allow_html=True)

st.markdown('<p style="color: #6B8E55">Hi, Whats your agenda today?</p>', unsafe_allow_html=True)

for messages in st.session_state['message']:
    if messages["role"] == 'assistant':
        with st.chat_message('assistant' , avatar=":material/asterisk:"):
            st.write(messages['msg'])

    if messages["role"] == 'user':
         with st.chat_message('user'):
            st.write(messages['msg'])
         

user_input = st.chat_input("Type here")
CONFIG = {'configurable': {'thread_id': st.session_state.thread_id}}

if user_input:
    st.session_state.message.append({'role': 'user', 'msg': user_input})

    with st.chat_message('user'):
            st.write(user_input)
    
    with st.chat_message('assistant' , avatar=":material/asterisk:"):
        if st.session_state.use_rag and st.session_state.indexed_docs:
            final_state = rag_chat.invoke(
                {'message': [HumanMessage(user_input)],
                 'doc_paths': [], 'expanded_queries': [],
                 'context_chunks': [], 'source_docs': [],
                 'generated_queries': [], 'intermediate_steps': []},
                config=CONFIG,
            )
            response = final_state["message"][-1].content
            st.write(response)
        else:
            response = st.write_stream(
                message_chunk.content for message_chunk, metadata in chat.stream(
                    {'message': [HumanMessage(user_input)]},
                    config=CONFIG,
                    stream_mode='messages'
                ))
    st.session_state.message.append({'role': 'assistant', 'msg':  response})
    st.rerun()


# print()
# print(st.session_state)
# print(list(checkpointer.list(config={'thread_id': '1'})))