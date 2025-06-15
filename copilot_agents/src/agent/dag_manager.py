from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
import asyncio

# Configuration
AIRFLOW_MCP_URL = os.getenv("AIRFLOW_MCP_URL", "http://localhost:8000/sse")
DAGMANAGER_LLM = os.getenv("DAGMANAGER_LLM", "google_genai:gemini-2.0-flash")

# Initialize MCP client
client = MultiServerMCPClient({
    "airflow": {
        "url": AIRFLOW_MCP_URL,
        "transport": "sse",
    }
})

async def create_dag_manager_agent():
    tools = await client.get_tools()
    # Move the blocking create_react_agent call to a separate thread
    return create_react_agent(
        DAGMANAGER_LLM,
        tools,
        prompt="An agent designed to interact with Apache Airflow and assist users by providing relevant details through the appropriate tools exposed by the Airflow MCP server. The agent should engage with the user to gather any necessary inputs or context required to invoke these tools effectively.",
        name="airflow-copilot"
    )