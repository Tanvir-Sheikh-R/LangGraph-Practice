from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

class MessageState(TypedDict):
    message : Annotated[list[BaseMessage], add_messages]

load_dotenv()
llm = ChatGroq(model='llama-3.1-8b-instant', temperature=0.2)

def chat_message(state: MessageState):
    message = state['message']
    response = llm.invoke(message)
    return {'message': [response]}

graph = StateGraph(MessageState)
graph.add_node('chat_message', chat_message)
graph.add_edge(START, 'chat_message')
graph.add_edge('chat_message', END)

checkpointer = InMemorySaver()
chat = graph.compile(checkpointer=checkpointer)