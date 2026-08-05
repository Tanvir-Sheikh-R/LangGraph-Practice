from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import RateLimitError, APIError, APIConnectionError
from langchain_core.messages import HumanMessage, AIMessage
import sqlite3


def get_summary_for_chatHead(user: str):
    prompt = f"""Generate a short, descriptive title for this conversation based on the user's message below. 
                Rules:
                - Maximum 5 words
                - No quotation marks, punctuation, or trailing periods
                - Capture the core topic or intent, not a generic summary
                - Do not include phrases like "Chat about" or "Conversation on"
                - Return ONLY the title text, nothing else
                User's message:{user}"""

    resposce = llm.invoke(prompt)
    return resposce.content


# if i want to use sqlite to store my conversations
def retrive_all_threads():
    all_thread = set()
    for id in checkpointer_sqlite.list(None):
        all_thread.add(id.config['configurable']['thread_id'])
    return list(all_thread)

    
class MessageState(TypedDict):
    message : Annotated[list[BaseMessage], add_messages]

load_dotenv()
llm = ChatGroq(model='llama-3.1-8b-instant', temperature=0.2)

def chat_message(state: MessageState):
    message = state['message']
    try:
        response = llm.invoke(message)
    except RateLimitError:
        response = AIMessage(
            content="I've hit the rate/token limit for this model right now. "
                    "Please wait a moment and try again."
        )
    except APIConnectionError:
        response = AIMessage(
            content="I'm having trouble connecting to the model service right now. "
                    "Please check your connection and try again."
        )
    except APIError as e:
        response = AIMessage(
            content=f"Something went wrong while generating a response: {e}"
        )
    except Exception as e:
        response = AIMessage(
            content=f"An unexpected error occurred: {e}"
        )
    return {'message': [response]}


graph = StateGraph(MessageState)
graph.add_node('chat_message', chat_message)
graph.add_edge(START, 'chat_message')
graph.add_edge('chat_message', END)



# if i want to use sqlite to store my conversations
connection = sqlite3.connect('chatbot.bd', check_same_thread=False)
checkpointer_sqlite = SqliteSaver(conn=connection)



checkpointer_inMemory = InMemorySaver()
chat = graph.compile(checkpointer=checkpointer_inMemory)

# responce = chat.invoke(
#             {'message': '2+2'}, 
#             config={'configurable': {'thread_id': '--1--'}}, 
#             )


# responce = chat.get_state({'configurable': {'thread_id': '--1--'}})

# print(responce.values.get('message')[1].content)
