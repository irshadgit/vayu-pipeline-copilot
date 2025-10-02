import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams


# MCP server configuration
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "3000"))

# Create the Airflow management agent
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='airflow_management_agent',
    instruction="""You are an Airflow management assistant that helps users manage Apache Airflow workflows. 

You have access to the following capabilities through the Airflow MCP server:
- List and filter DAGs with various parameters
- Get detailed information about specific DAGs
- Retrieve DAG details including tasks and their configurations
- Access Airflow variables
- Perform health checks on the Airflow system

When helping users:
1. Use clear, concise language to explain Airflow concepts
2. Provide structured information about DAGs, tasks, and configurations
3. Help troubleshoot issues by examining DAG details and variables
4. Suggest best practices for Airflow workflow management
5. Format JSON responses in a readable way when presenting data

Always be helpful and provide actionable insights based on the Airflow data you can access.""",
    tools=[
        MCPToolset(
            connection_params=SseServerParams(
                url=f"http://{MCP_HOST}:{MCP_PORT}/sse"
            ),
            # Filter to only include the Airflow management tools
            tool_filter=[
                'get_dags',
                'get_dag',
                'health'
            ]
        )
    ],
)

if __name__ == "__main__":
    print("🚁 Airflow Management Agent initialized!")
    print(f"📡 Connecting to MCP server at {MCP_HOST}:{MCP_PORT}")
    print("🔧 Available tools: get_dags, get_dag, health")
    print("💬 Ready to help manage your Airflow workflows!")
