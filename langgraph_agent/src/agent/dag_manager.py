from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent  # Temporarily disabled due to import issue
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
    """Temporary simple agent implementation to avoid import issues."""
    # Skip tools loading for now to avoid connection errors
    # tools = await client.get_tools()
    
    # Simple agent function that just returns a basic response
    async def simple_agent(state):
        messages = state.get("messages", [])
        # For now, just return a simple response
        return {
            "messages": messages + [{"role": "assistant", "content": "DAG Manager agent is ready (temporary implementation)"}]
        }
    
    return simple_agent