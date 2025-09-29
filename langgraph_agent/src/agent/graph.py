# from langgraph.prebuilt import create_react_agent  # Temporarily disabled due to import issue
from langgraph.graph import StateGraph, END
import asyncio
from src.agent.dag_manager import create_dag_manager_agent
from typing_extensions import Annotated, TypedDict
from langgraph.graph import add_messages
# Define the state schema for our graph
class State(TypedDict):
    # add_messages will default to upserting messages by ID to the existing list
    # if a RemoveMessage is returned, it will delete the message in the list by ID
    messages: Annotated[list, add_messages]


async def create_graph():
    # Create the base graph with state schema
    workflow = StateGraph(
        state_schema=State
    )
    
    # Create the DAG manager agent
    dag_manager = await create_dag_manager_agent()
    
    # Add the DAG manager node to the graph
    workflow.add_node("dag_manager", dag_manager)
    
    # Set the entry point
    workflow.set_entry_point("dag_manager")
    
    # Add edges (for now, just end after DAG manager)
    workflow.add_edge("dag_manager", END)
    
    
    compiled_graph = workflow.compile()
    
    # Compile the graph
    return compiled_graph

async def main():
    global graph
    graph = await create_graph()

asyncio.run(main())