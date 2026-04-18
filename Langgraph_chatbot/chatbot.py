from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import operator
import os

load_dotenv()

#define llm
llm = ChatOpenAI()


# define state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    
#define chat_node
def chat_node(state:ChatState):
    """This function provides response based on chat message"""
    response = llm.invoke(state['messages']).content
    return {'messages' : [AIMessage(content=response)]}

#create checkpoint object
checkpoint = MemorySaver()

#define greaph
graph=StateGraph(ChatState)

#add nodes and edges
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpoint)


while(True):
    user_message = input()
    #print('user: '+ user_message)

    if(user_message == 'exit'):
        break

    config = {'configurable' : {'thread_id':1}}
    response = chatbot.invoke({'messages':[HumanMessage(content=user_message)]}, config=config)
    
    print(response['messages'][-1].content)





