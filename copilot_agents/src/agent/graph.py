from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
import asyncio
from langgraph.checkpoint.memory import InMemorySaver
from src.agent.dag_manager import create_dag_manager_agent
from typing import TypedDict, Annotated
from typing_extensions import TypedDict

# Define the state schema for our graph
class AgentState(TypedDict):
    messages: list[str]  # List of messages in the conversation
    current_step: str    # Current step in the workflow

async def create_graph():
    # Create the base graph with state schema
    workflow = StateGraph(
        state_schema=AgentState
    )
    
    # Create the DAG manager agent
    dag_manager = await create_dag_manager_agent()
    
    # Add the DAG manager node to the graph
    workflow.add_node("dag_manager", dag_manager)
    
    # Set the entry point
    workflow.set_entry_point("dag_manager")
    
    # Add edges (for now, just end after DAG manager)
    workflow.add_edge("dag_manager", END)
    
    # Compile the graph
    return workflow.compile()

async def main():
    global graph
    graph = await create_graph()

asyncio.run(main())